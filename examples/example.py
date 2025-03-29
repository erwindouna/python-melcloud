"""Asynchronous Python client for MELCloud. This is an example file."""

import asyncio
import logging

import aiohttp

import pymelcloud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Demonstrate the usage of pymelcloud.

    This function logs in to the MELCloud service, retrieves a list of devices,
    and performs operations on a specific device. It uses an asynchronous
    HTTP session for communication.

    Raises
    ------
        ValueError: If login fails due to invalid credentials or other issues.

    """
    async with aiohttp.ClientSession() as session:
        try:
            # Call the login method with the session
            token = await pymelcloud.login(
                email="my@example.com",
                password="mysecretpassword",  # noqa: S106
                session=session,
            )
            logger.info("Login successful, token: %s", token)
        except ValueError:
            logger.exception("Login failed")
            return

        # Lookup the device
        devices = await pymelcloud.get_devices(token, session=session)
        device = devices[pymelcloud.DEVICE_TYPE_ATW][0]

        # Perform logic on the device
        await device.update()

        logger.info("Device name: %s", device.name)
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
