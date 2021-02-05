""" Entry point for running the pump light. """
import asyncio
import logging
import os
from functools import partial

from pump_light import client, light_controller, ws_client
from pump_light.infrastructure import config

_LOG = logging.getLogger('pump_light')


async def main():
    """ Main that tires all logic together. """
    logging.basicConfig(level=logging.INFO)

    # Preparing config
    profile = os.getenv('IOT_SERVER_PROFILE', 'dev')
    _LOG.info('PROFILE: %s', profile)
    config.init(profile)

    # Observes the device
    await observe_and_shine()


async def observe_and_shine():
    """ Waits for incoming message and checks if it should turn on the light. """
    led = config.build_led()
    event_handler = partial(light_controller.switch_light, led=led)

    while True:
        try:
            # Throttle down
            await asyncio.sleep(20)

            exists = await client.check_existence()

            if exists:
                await ws_client.react(event_handler)
        except Exception as ex:
            _LOG.exception('Error while report', exc_info=ex)
            await client.send_exception(ex)


asyncio.get_event_loop().run_until_complete(main())
