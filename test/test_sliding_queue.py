from .helper import wrap_async_test
from asyncio_channel._sliding_queue import SlidingQueue

import asyncio
import pytest


def test_put_nowait():
    """
    GIVEN
        Queue is not full.
    WHEN
        Put an item.
    EXPECT
        Item is added.
    """
    q = asyncio.Queue(1)
    sb = SlidingQueue(q)
    a = 'a'
    sb.put_nowait(a)
    assert sb.get_nowait() == a

def test_put_nowait_full():
    """
    GIVEN
        Queue is full.
    WHEN
        Put an item.
    EXPECT
        Item is added.
    """
    q = asyncio.Queue(1)
    sb = SlidingQueue(q)
    a = 'a'
    sb.put_nowait(a)
    b = 'b'
    sb.put_nowait(b)
    assert sb.get_nowait() == b

@wrap_async_test
async def test_put():
    """
    GIVEN
        Queue is not full.
    WHEN
        Put an item.
    EXPECT
        Item is added.
    """
    q = asyncio.Queue(1)
    sb = SlidingQueue(q)
    a = 'a'
    await asyncio.wait_for(sb.put(a), timeout=0.05)
    assert sb.get_nowait() == a

@wrap_async_test
async def test_put_full():
    """
    GIVEN
        Queue is full.
    WHEN
        Put an item.
    EXPECT
        Item is added.
    """
    q = asyncio.Queue(1)
    sb = SlidingQueue(q)
    a = 'a'
    await asyncio.wait_for(sb.put(a), timeout=0.05)
    b = 'b'
    await asyncio.wait_for(sb.put(b), timeout=0.05)
    assert sb.get_nowait() == b
