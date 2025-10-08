"""Test module imports and basic functionality."""

import pytest
from aiohttp.client_exceptions import ClientResponseError

import pymelcloud
from pymelcloud import DEVICE_TYPE_ATA, DEVICE_TYPE_ATW, DEVICE_TYPE_ERV
from pymelcloud.ata_device import AtaDevice
from pymelcloud.atw_device import AtwDevice
from pymelcloud.client import Client
from pymelcloud.device import Device
from pymelcloud.erv_device import ErvDevice


def test_imports() -> None:
    """Test that all imports work correctly."""
    # Test constants are importable
    assert DEVICE_TYPE_ATA == "ata"
    assert DEVICE_TYPE_ATW == "atw"
    assert DEVICE_TYPE_ERV == "erv"

    # Test classes are importable
    assert AtaDevice is not None
    assert AtwDevice is not None
    assert Client is not None
    assert Device is not None
    assert ErvDevice is not None


def test_module_docstring() -> None:
    """Test that the module has a docstring."""
    assert pymelcloud.__doc__ == "MELCloud client library."


@pytest.mark.asyncio
async def test_login_function_exists() -> None:
    """Test that login function exists and has correct signature."""
    # Just test the function exists and is callable
    assert callable(pymelcloud.login)

    # Test it raises appropriate error with invalid credentials
    with pytest.raises(
        (ValueError, ConnectionError, RuntimeError, ClientResponseError)
    ):
        await pymelcloud.login("invalid", "credentials")


@pytest.mark.asyncio
async def test_get_devices_function_exists() -> None:
    """Test that get_devices function exists and has correct signature."""
    # Just test the function exists and is callable
    assert callable(pymelcloud.get_devices)

    # Test it raises appropriate error with invalid token
    with pytest.raises(
        (ValueError, ConnectionError, RuntimeError, ClientResponseError)
    ):
        await pymelcloud.get_devices("invalid_token")
