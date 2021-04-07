""" WS client for IOT server """
import functools
import logging
from datetime import datetime
from typing import Callable, Dict, Coroutine

import aiohttp
from aiohttp import ClientSession, WSMessage, ClientWebSocketResponse

from pump_light.exception import EndedTooEarlyException
from pump_light.infrastructure import config
from pump_light.model.message import MessageDTO
from pump_light.observer import ObserverRegistry

_LOG = logging.getLogger(__name__)
_REG = ObserverRegistry()

WebsocketHandler = Dict[int, Callable[[ClientWebSocketResponse, WSMessage], Coroutine[None, None, None]]]


async def react(event_handler: Callable[[MessageDTO], None]):
    """ Waits for incoming WS message and applies event handler on them. """
    url = config.build_device_url() + '/exchange'
    handle_text_message = functools.partial(__handle_text_message, event_handler=event_handler)
    _REG.register_observer(aiohttp.WSMsgType.TEXT, handle_text_message)

    async with ClientSession() as session:
        async with session.ws_connect(url, headers=config.basic_auth()) as websocket:
            async for msg in websocket:
                # noinspection PyTypeChecker
                ws_msg: WSMessage = msg
                await _REG.notify(ws_msg.type, websocket, ws_msg)

    raise EndedTooEarlyException('Listener finished which should never happen.')


# ===== ===== ===== ======= ===== ===== =====
# ===== ===== ===== HANDLER ===== ===== =====
# ===== ===== ===== ======= ===== ===== =====


async def __handle_text_message(_websocket: ClientWebSocketResponse, msg: WSMessage,
                                event_handler: Callable[[MessageDTO], None]) -> None:
    _LOG.debug('%s: Server sent "%s"', datetime.now(), msg.data)

    json_response = msg.json()
    if 'access_id' not in json_response:
        message = MessageDTO(**json_response)
        event_handler(message)
    elif isinstance(json_response, dict):
        _LOG.info(f'Got id {json_response.get("access_id")}')


@_REG.observe(aiohttp.WSMsgType.ERROR)
@_REG.observe(aiohttp.WSMsgType.CLOSE)
@_REG.observe(aiohttp.WSMsgType.CLOSED)
@_REG.observe(aiohttp.WSMsgType.CLOSING)
async def __handle_end_message(websocket: ClientWebSocketResponse, msg: WSMessage) -> None:
    _LOG.info('Closing websocket because of message type "%s"', msg.type)
    await websocket.close()
