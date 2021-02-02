""" Entry point for running the pump light. """
import asyncio
import logging
import os

from pump_light import client, light_controller
from pump_light.infrastructure import config


async def main():
    """ Main that tires all logic together. """
    logger = logging.getLogger('pump_light')

    # Preparing config
    profile = os.getenv('IOT_SERVER_PROFILE', 'dev')
    logger.info('PROFILE: %s', profile)
    config.init(profile)

    # Observes the device
    await observe_and_shine()


async def observe_and_shine():
    """ Waits for incoming message and checks if it should turn on the light. """
    event_handler = light_controller.switch_light

    while True:
        # Throttle down
        await asyncio.sleep(20)

        exists = await client.check_existence()

        if exists:
            try:
                await client.react(event_handler)
            except Exception as ex:
                await client.send_exception(ex)


asyncio.get_event_loop().run_until_complete(main())
