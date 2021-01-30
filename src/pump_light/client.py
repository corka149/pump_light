""" Websocket and HTTP/S client for iot_server """
import base64
import logging
import socket
from datetime import datetime
from typing import Callable, Tuple, Dict

import aiohttp
from aiohttp import ClientSession, WSMessage

from pump_light.exception import EndedTooEarlyException
from pump_light.infrastructure import config
from pump_light.model.exception import ExceptionSubmittal
from pump_light.model.message import MessageDTO

_LOG = logging.getLogger(__name__)


async def react(event_handler: Callable[[MessageDTO], None]):
    """ Waits for incoming WS message and applies event handler on them. """
    url = __build_device_url() + '/exchange'

    async with ClientSession() as session:
        async with session.ws_connect(url, headers=__basic_auth(), heartbeat=5) as websocket:
            _LOG.info('Connected')
            async for msg in websocket:
                # noinspection PyTypeChecker
                ws_msg: WSMessage = msg
                if ws_msg.type == aiohttp.WSMsgType.TEXT:
                    _LOG.debug('%s: Server sent "%s"', datetime.now(), ws_msg.data)
                    message = MessageDTO(**ws_msg.json())
                    event_handler(message)
                elif ws_msg.type == aiohttp.WSMsgType.ERROR:
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

        async with session.post(url, data=exception_dto.json(), headers=__basic_auth()) as response:
            msg = await response.text()
            _LOG.info('Response on error report: status=%s, message="%s"', response.status, msg)


def check_existence():
    """ Checks if a device exists. """
    async with ClientSession() as session:
        async with session.get(__build_device_url(), headers=__basic_auth()) as response:
            _LOG.info('Response of checking existence: status=%s', response.status)
            return response.status == 200


def __build_device_url() -> str:
    url = config.get_config('iot_server.address')
    device_name = config.get_config('observers.device.name')
    return url + f'/device/{device_name}'


def __basic_auth() -> Dict[str, str]:
    username = config.get_config('security.basic.username')
    passwd = config.get_config('security.basic.password')
    b64 = base64.b64encode(bytes(f'{username}:{passwd}', 'ascii'))
    return {'Authorization': f'Basic {b64.decode("ascii")}'}
