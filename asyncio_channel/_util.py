__all__ = ('wait_all', 'wait_first')

from asyncio import FIRST_COMPLETED, CancelledError, Task, create_task, wait, get_running_loop
import functools

async def cancel_and_wait(task,
    get_running_loop=get_running_loop):
    """Cancel the task and wait until it completes.
    Based on asyncio._cancel_and_wait.
    """
    loop = get_running_loop()
    waiter = loop.create_future()
    # Use a done callback instead of await, because otherwise we would be
    # unable to distinguish the CancelledError from the task from a
    # CancelledError we might receive due to being cancelled ourselves.
    def release(_):
        if not waiter.done():
            waiter.set_result(None)
    task.add_done_callback(release)

    try:
        task.cancel()
        await waiter
    finally:
        task.remove_done_callback(release)

async def wait_all(
        *coros_or_tasks,
        timeout=None,
        create_task=create_task,
        wait=wait,
        cancel_and_wait=cancel_and_wait):
    """Wait for all tasks to complete.

    Returns two tuples: completed tasks, pending tasks.  If timeout is
    provided then completed tasks set may be empty.
    """
    if not coros_or_tasks:
        return (), ()
    tasks = tuple(
        ct if isinstance(ct, Task) else create_task(ct)
        for ct in coros_or_tasks)

    try:
        done, pending = await wait(tasks, timeout=timeout)
    except CancelledError:
        for task in tasks:
            if not task.done():
                await cancel_and_wait(task)

        raise
    else:
        for task in pending:
            await cancel_and_wait(task)

        return done, pending


async def wait_first(
        *coros_or_tasks,
        timeout=None,
        wait=wait,
        return_when=FIRST_COMPLETED,
        CancelledError=CancelledError,
        cancel_and_wait=cancel_and_wait):
    """Wait for first task to complete.

    Returns two tuples: completed tasks, pending tasks.  If timeout is
    provided then completed tasks set may be empty.
    """
    if not coros_or_tasks:
        return (), ()
    tasks = tuple(
        ct if isinstance(ct, Task) else create_task(ct)
        for ct in coros_or_tasks)

    try:
        done, pending = await wait(
            tasks,
            timeout=timeout,
            return_when=return_when)
    except CancelledError:
        for task in tasks:
            if not task.done():
                task.cancel()

        raise
    else:
        for task in pending:
            await cancel_and_wait(task)

        return done, pending
