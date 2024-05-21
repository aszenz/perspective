#  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#  ┃ ██████ ██████ ██████       █      █      █      █      █ █▄  ▀███ █       ┃
#  ┃ ▄▄▄▄▄█ █▄▄▄▄▄ ▄▄▄▄▄█  ▀▀▀▀▀█▀▀▀▀▀ █ ▀▀▀▀▀█ ████████▌▐███ ███▄  ▀█ █ ▀▀▀▀▀ ┃
#  ┃ █▀▀▀▀▀ █▀▀▀▀▀ █▀██▀▀ ▄▄▄▄▄ █ ▄▄▄▄▄█ ▄▄▄▄▄█ ████████▌▐███ █████▄   █ ▄▄▄▄▄ ┃
#  ┃ █      ██████ █  ▀█▄       █ ██████      █      ███▌▐███ ███████▄ █       ┃
#  ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
#  ┃ Copyright (c) 2017, the Perspective Authors.                              ┃
#  ┃ ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ ┃
#  ┃ This file is part of the Perspective library, distributed under the terms ┃
#  ┃ of the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). ┃
#  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

from typing import Awaitable, Callable, Dict
import perspective

_psp_server = perspective.PyAsyncServer()
_clients: Dict[str, Callable[[bytes], Awaitable[None]]] = {}
_session_id = 0

def make_session_id():
    global _session_id
    new_id = _session_id
    _session_id += 1
    return new_id

async def delegate_client(client_id: str, msg: bytes):
    if client_id in _clients:
        await _clients[client_id](msg)

def register_session(client_id: str, fn: Callable[[bytes], Awaitable[None]]):
    _clients[client_id] = fn

def unregister_session(client_id: str):
    del _clients[client_id]

# cid = _psp_server.register_session(lambda *args, **kwargs: print("shared_session", args, kwargs))
async def shared_client():
    return await perspective.create_async_client(_psp_server)

class Session:
    def __init__(self, fn: Callable[[bytes], Awaitable[None]]):
        self.client_id = _psp_server.register_session(fn)
    
    def __del__(self):
        _psp_server.unregister_session(self.client_id)

    async def handle_message(self, msg: bytes):
        await _psp_server.handle_message(self.client_id, msg)
        _psp_server.poll()
        # import asyncio
        # async def poll():
        #     await _psp_server.poll()
        # asyncio.get_event_loop().create_task(poll())
