import functools, asyncio, pytest

def wrap_async_test(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        first_exception = None
        def exception_handler(loop, ctx):
            print(ctx)
            nonlocal first_exception
            if first_exception is None:
                first_exception = ctx.get('exception', Exception(ctx['message']))
        loop = asyncio.new_event_loop()
        loop.set_exception_handler(exception_handler)
        ret = loop.run_until_complete(f(*args, **kwargs))
        loop.close()
        if first_exception is not None:
            raise first_exception
        return ret
    return wrapped

async def expect_cancelled(coro):
    with pytest.raises(asyncio.CancelledError):
        return await coro
