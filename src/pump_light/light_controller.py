""" Controls the light and turns it off or on """
import logging

from gpiozero import LED

from pump_light.model.message import MessageDTO

_LOG = logging.getLogger(__name__)


def switch_light(message: MessageDTO, led: LED):
    """ Turns off or on the lights and acts as event handler """
    _LOG.info('Received message: "%s"', message)

    if message.type == 'ACTIVITY' and message.content == '1':
        _turn_on(led)
    elif message.type == 'ACTIVITY' and message.content == '0':
        _turn_off(led)
    else:
        _LOG.info('Unknown message')


def _turn_on(led: LED):
    led.on()
    _LOG.info('light on')


def _turn_off(led: LED):
    led.off()
    _LOG.info('light off')
