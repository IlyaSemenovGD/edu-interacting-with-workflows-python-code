import asyncio
from typing import List

from temporalio import activity, workflow
from temporalio.client import Client
from datetime import timedelta

class GreetingComposer:
    def __init__(self, client: Client) -> None:
        self.client = client

    @activity.defn
    async def compose_greeting(self):
        print("Completing activity asynchronously")
        # DONE Part A: Call `asyncio.create_task(self.complete_greeting())`.
        # Don't forget to pass `activity.info().task_token` to `complete_greeting()`.
        # DONE Part B: Call `activity.raise_complete_async()` at the end of this method.
        await asyncio.create_task(self.complete_greeting(activity.info().task_token))
        await activity.raise_complete_async()

    async def complete_greeting(self, task_token: bytes) -> None:
        handle = self.client.get_async_activity_handle(task_token=task_token)
        # TODO Part C: Make this Activity heartbeat once per second to avoid it failing
        # due to the `heartbeat_timeout` of 2 seconds configured below.
        # You can use `handle.heartbeat()` and `asyncio.sleep(1)`.
        # After a few heartbeats, call `handle.complete()`.
        n_loops = 4
        for i in range(n_loops):
            await handle.heartbeat()
            print(f'Waiting 1 second. Wait counter: {i} of {n_loops}')
            await asyncio.sleep(1)
        await handle.complete()
        print('Activity complete')

@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self):
        workflow.logger.info("Running workflow.")
        return await workflow.execute_activity_method(
            GreetingComposer.compose_greeting,
            start_to_close_timeout=timedelta(seconds=10),
            heartbeat_timeout=timedelta(seconds=2),
        )
