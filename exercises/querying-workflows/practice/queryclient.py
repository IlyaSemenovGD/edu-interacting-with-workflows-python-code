import asyncio

from temporalio.client import Client
from workflow import MyWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle_for(MyWorkflow.run, "queries")
    # TODO Part B: Send a Query using `handle.query()`.
    # Note that `MyWorkflow` has been imported from `workflow.py` above.
    # You can use this to call the Query definition.
    result = await handle.query(MyWorkflow.current_state_query)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
