from typing import TypeVar

from neovim.msgpack_rpc import MsgpackStream, AsyncSession, Session
from neovim.plugin import Host
from neovim.api import Nvim
from neovim.msgpack_rpc.event_loop.base import BaseEventLoop
from neovim.msgpack_rpc.event_loop.asyncio import AsyncioEventLoop
from neovim.msgpack_rpc.event_loop.uv import UvEventLoop

L = TypeVar('L', bound=BaseEventLoop)


def session(Loop: L, *args: str, transport_type='stdio', **kwargs: str):
    loop = Loop(transport_type, *args, **kwargs)
    msgpack_stream = MsgpackStream(loop)
    async_session = AsyncSession(msgpack_stream)
    session = Session(async_session)
    return session


def common(Loop: L, plug: str) -> None:
    sess = session(Loop)
    nvim = Nvim.from_session(sess)
    host = Host(nvim)
    host.start([plug])


def start_asyncio_host(plug: str) -> None:
    common(AsyncioEventLoop, plug)


def start_uv_host(plug: str) -> None:
    common(UvEventLoop, plug)


def start_host(plug: str, uv_loop: bool) -> None:
    (start_uv_host if uv_loop else start_asyncio_host)(plug)

__all__ = ('start_host',)
