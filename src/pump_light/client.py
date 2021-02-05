""" Websocket and HTTP/S client for iot_server """
import logging
import socket

from aiohttp import ClientSession

from pump_light.infrastructure import config
from pump_light.model.exception import ExceptionSubmittal

_LOG = logging.getLogger(__name__)


async def send_exception(exception: Exception) -> None:
    """ Send a exception report to the iot server. """
    url = config.get_config('iot_server.address') + '/exception'

    async with ClientSession() as session:
        exception_dto = ExceptionSubmittal(
            hostname=socket.gethostname(),
            clazz=exception.__class__.__name__,
            message='Exception on listener side',
            stacktrace=str(exception)
        )

        async with session.post(url, data=exception_dto.json(), headers=config.basic_auth()) as response:
            msg = await response.text()
            _LOG.info('Response on error report: status=%s, message="%s"', response.status, msg)


async def check_existence() -> bool:
    """ Checks if a device exists. """
    async with ClientSession() as session:
        async with session.get(config.build_device_url(), headers=config.basic_auth()) as response:
            _LOG.info('Response of checking existence: status=%s', response.status)
            return response.status == 200
