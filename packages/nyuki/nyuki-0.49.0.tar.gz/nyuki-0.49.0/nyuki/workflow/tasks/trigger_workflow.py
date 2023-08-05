import json
import asyncio
import logging
import async_timeout
from uuid import uuid4
from enum import Enum
from aiohttp import ClientSession
from tukio.task import register
from tukio.task.holder import TaskHolder
from tukio.workflow import WorkflowExecState, Workflow

from .utils import runtime
from .utils.uri import URI


log = logging.getLogger(__name__)


class WorkflowStatus(Enum):

    PENDING = 'pending'
    RUNNING = 'running'
    TIMEOUT = 'timeout'
    DONE = 'done'


@register('trigger_workflow', 'execute')
class TriggerWorkflowTask(TaskHolder):

    __slots__ = (
        'template', 'blocking', 'task', '_engine',
        'status', 'triggered_id', 'async_future',
    )

    SCHEMA = {
        'type': 'object',
        'required': ['template'],
        'additionalProperties': False,
        'properties': {
            'template': {
                'type': 'object',
                'required': ['service', 'id'],
                'additionalProperties': False,
                'properties': {
                    'service': {'type': 'string', 'minLength': 1},
                    'id': {'type': 'string', 'minLength': 1},
                    'draft': {'type': 'boolean', 'default': False},
                },
            },
            'blocking': {
                'type': 'object',
                'required': ['timeout'],
                'additionalProperties': False,
                'properties': {
                    'timeout': {'type': 'integer', 'minimum': 1}
                },
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self.template = self.config['template']
        self.blocking = self.config.get('blocking', {})
        self.task = None
        self._engine = 'http://{}/{}/api/v1/workflow'.format(
            runtime.config.get('http_host', 'localhost'),
            self.template['service'],
        )

        # Reporting
        self.status = WorkflowStatus.PENDING.value
        self.triggered_id = None
        self.async_future = None

    def report(self):
        return {
            'exec_id': self.triggered_id,
            'status': self.status,
        }

    async def async_exec(self, topic, data):
        log.debug(
            "Received data for async trigger_workflow in '%s': %s",
            topic, data,
        )
        if not self.async_future.done():
            self.async_future.set_result(data)
        await runtime.bus.unsubscribe(topic)

    async def execute(self, event):
        """
        Entrypoint execution method.
        """
        data = event.data
        self.task = asyncio.Task.current_task()
        data['timeout'] = False
        is_draft = self.template.get('draft', False)

        # Send the HTTP request
        log.info('Triggering template %s%s on service %s', self.template['id'],
                 ' (draft)' if is_draft else '', self.template['service'])

        # Setup headers (set requester and exec-track to avoid workflow loops)
        workflow = runtime.workflows[Workflow.current_workflow().uid]
        parent = workflow.exec.get('requester')
        track = list(workflow.exec.get('track', []))
        if parent:
            track.append(parent)

        headers = {
            'Content-Type': 'application/json',
            'Referer': URI.instance(workflow.instance),
            'X-Surycat-Exec-Track': ','.join(track)
        }

        # Handle blocking trigger_workflow using mqtt
        if self.blocking:
            topic = '{}/async/{}'.format(runtime.bus.name, str(uuid4())[:8])
            headers['X-Surycat-Async-Topic'] = topic
            headers['X-Surycat-Async-Events'] = ','.join([
                WorkflowExecState.end.value,
                WorkflowExecState.error.value,
            ])
            self.async_future = asyncio.Future()
            await runtime.bus.subscribe(topic, self.async_exec)

            def _unsub(f):
                asyncio.ensure_future(runtime.bus.unsubscribe(topic))
            self.task.add_done_callback(_unsub)

        async with ClientSession() as session:
            # Compute data to send to sub-workflows
            url = '{}/vars/{}{}'.format(
                self._engine,
                self.template['id'],
                '/draft' if is_draft else '',
            )
            async with session.get(url) as response:
                if response.status != 200:
                    raise RuntimeError("Can't load template info")
                wf_vars = await response.json()
            lightened_data = {key: data[key] for key in wf_vars if key in data}

            params = {
                'url': f"{self._engine}/instances",
                'headers': headers,
                'data': json.dumps({
                    'id': self.template['id'],
                    'draft': is_draft,
                    'inputs': lightened_data,
                })
            }
            async with session.put(**params) as response:
                if response.status != 200:
                    msg = "Can't process workflow template {} on {}".format(
                        self.template, self.nyuki_api
                    )
                    if response.status % 400 < 100:
                        reason = await response.json()
                        msg = "{}, reason: {}".format(msg, reason['error'])
                    raise RuntimeError(msg)
                resp_body = await response.json()
                self.triggered_id = resp_body['exec']['id']

        wf_id = f"{self.triggered_id[:8]}@{self.template['service']}"
        self.status = WorkflowStatus.RUNNING.value
        log.info('Successfully started %s', wf_id)
        self.task.dispatch_progress(self.report())

        # Block until task completed
        if self.blocking:
            timeout = self.blocking['timeout']
            log.info(
                'Waiting %s seconds for workflow %s to complete',
                timeout, wf_id,
            )
            try:
                with async_timeout.timeout(timeout):
                    await self.async_future
            except asyncio.TimeoutError:
                data['timeout'] = True
                self.status = WorkflowStatus.TIMEOUT.value
                log.info('Workflow %s has timed out', wf_id)
            else:
                self.status = WorkflowStatus.DONE.value
                log.info('Workflow %s is done', wf_id)

            self.task.dispatch_progress({'status': self.status})

        return data

    async def teardown(self):
        """
        Called when this task is cancelled.
        """
        if not self.triggered_id:
            log.debug('No workflow to cancel')
            return

        wf_id = f"{self.triggered_id[:8]}@{self.template['service']}"
        async with ClientSession() as session:
            url = f'{self._engine}/instances/{self.triggered_id}'
            async with session.delete(url) as response:
                if response.status != 200:
                    log.warning('Failed to cancel workflow %s', wf_id)
                else:
                    log.info('Workflow %s has been cancelled', wf_id)
