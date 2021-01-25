""" Websocket and HTTP/S client for iot_server """
import logging
import socket
from datetime import datetime
from typing import Callable

import aiohttp
from aiohttp import ClientSession, WSMessage

from pump_light.exception import EndedTooEarlyException
from pump_light.infrastructure import config
from pump_light.model.exception import ExceptionSubmittal
from pump_light.model.message import MessageDTO

_LOG = logging.getLogger(__name__)


async def react(event_handler: Callable[[MessageDTO], None]):
    """ Waits for incoming WS message and applies event handler on them. """
    url = config.get_config('iot_server.address')
    device_name = config.get_config('device.name')
    url = url + f'/device/{device_name}/exchange'

    async with ClientSession() as session:
        async with session.ws_connect(url) as websocket:
            _LOG.info('Connected')
            async for msg in websocket:
                msg: WSMessage = msg
                if msg.type == aiohttp.WSMsgType.TEXT:
                    _LOG.debug('%s: Server sent "%s"', datetime.now(), msg.data)
                    message = MessageDTO(**msg.json())
                    event_handler(message)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    err = str(msg)
                    _LOG.error('ERROR: "%s"', err)
                    raise ValueError(err)

    raise EndedTooEarlyException('Listener finished which should never happen.')


async def send_exception(exception: Exception) -> None:
    """ Send a exception report to the iot server. """
    url = config.get_config('iot_server.address') + '/exception'

    async with ClientSession() as session:
        exception_dto = ExceptionSubmittal(
            hostname=socket.gethostname(),
            clazz=exception.__class__.__name__,
            message='Exception on listener side',
            description=str(exception)
        )

        async with session.post(url, data=exception_dto.json()) as response:
            msg = await response.text()
            _LOG.info('Response on error report: status=%s, message="%s"', response.status, msg)
