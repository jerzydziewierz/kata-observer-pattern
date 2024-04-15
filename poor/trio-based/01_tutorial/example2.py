import trio
import time


async def task_with_deadline(task_id):
    print(f"Task {task_id} started")
    try:
        # Simulating some work
        await trio.sleep(1.0*task_id)
        print(f"Task {task_id} completed")
    except trio.Cancelled:
        print(f"Task {task_id} cancelled")


async def main():
    async with trio.open_nursery() as nursery:
        # Inject tasks with deadlines
        print('Starting tasks')
        for idx in range(1, 11):
            nursery.start_soon(task_with_deadline, idx)
        print('Finished starting tasks soon...')

        # Continue with other work
        await trio.sleep(4)
        print("Main task completed")


trio.run(main)
