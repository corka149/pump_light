""" Entry point for running the pump light. """
import asyncio
import logging
import os

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
    pass


asyncio.get_event_loop().run_until_complete(main())
