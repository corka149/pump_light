""" Controls the light and turns it off or on """
import logging

from pump_light.infrastructure import config
from pump_light.model.message import MessageDTO

_LOG = logging.getLogger(__name__)


def switch_light(message: MessageDTO):
    """ Turns off or on the lights and acts as event handler """
    _LOG.info('Received message: "%s"', message)

    if message.type == 'ACTIVITY' and message.content == '1':
        _turn_on()
    elif message.type == 'ACTIVITY' and message.content == '0':
        _turn_off()
    else:
        _LOG.info('Unknown message')


def _turn_on():
    dev_mode = config.get_config('dev_mode')

    if not dev_mode:
        pass
    else:
        _LOG.info('light on')


def _turn_off():
    dev_mode = config.get_config('dev_mode')

    if not dev_mode:
        pass
    else:
        _LOG.info('light off')
