""" WS client for IOT server """
import logging
from collections import defaultdict
from datetime import datetime
from typing import Callable, Dict, Coroutine

import aiohttp
from aiohttp import ClientSession, WSMessage, ClientWebSocketResponse

from pump_light.exception import EndedTooEarlyException
from pump_light.infrastructure import config
from pump_light.model.message import MessageDTO

_LOG = logging.getLogger(__name__)


async def react(event_handler: Callable[[MessageDTO], None]):
    """ Waits for incoming WS message and applies event handler on them. """
    url = config.build_device_url() + '/exchange'
    handler = __build_handler(text_handler=event_handler)

    async with ClientSession() as session:
        async with session.ws_connect(url, headers=config.basic_auth()) as websocket:
            async for msg in websocket:
                # noinspection PyTypeChecker
                ws_msg: WSMessage = msg
                handler_func = handler[ws_msg.type]
                await handler_func(websocket, ws_msg)

    raise EndedTooEarlyException('Listener finished which should never happen.')


# ===== ===== ===== ======= ===== ===== =====
# ===== ===== ===== HANDLER ===== ===== =====
# ===== ===== ===== ======= ===== ===== =====


# noinspection PyTypeChecker
def __build_handler(
        text_handler: Callable[[MessageDTO], None]
) -> Dict[int, Callable[[ClientWebSocketResponse, WSMessage], Coroutine[None, None, None]]]:
    handler = defaultdict(__handle_message_default)
    handler[aiohttp.WSMsgType.TEXT] = __build_handle_text_message(text_handler)
    handler[aiohttp.WSMsgType.ERROR] = __handle_end_message
    handler[aiohttp.WSMsgType.CLOSE] = __handle_end_message
    handler[aiohttp.WSMsgType.CLOSED] = __handle_end_message
    handler[aiohttp.WSMsgType.CLOSING] = __handle_end_message

    return handler


def __build_handle_text_message(event_handler: Callable[[MessageDTO], None]):
    async def __handle_text_message(_websocket: ClientWebSocketResponse, msg: WSMessage) -> None:
        _LOG.debug('%s: Server sent "%s"', datetime.now(), msg.data)

        json_response = msg.json()
        if 'access_id' not in json_response:
            message = MessageDTO(**json_response)
            event_handler(message)
        elif isinstance(json_response, dict):
            _LOG.info(f'Got id {json_response.get("access_id")}')

    return __handle_text_message


async def __handle_end_message(websocket: ClientWebSocketResponse, msg: WSMessage) -> None:
    _LOG.info('Closing websocket because of message type "%s"', msg.type)
    await websocket.close()


async def __handle_message_default(_websocket: ClientWebSocketResponse, msg: WSMessage) -> None:
    _LOG.info(str(msg))
