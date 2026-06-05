"""Shared pytest fixtures for python-melcloud tests."""

import json
from collections.abc import AsyncGenerator

import pytest
from aiohttp import ClientSession
from syrupy.assertion import SnapshotAssertion

from pymelcloud.ata_device import AtaDevice
from pymelcloud.atw_device import AtwDevice
from pymelcloud.client import Client
from pymelcloud.erv_device import ErvDevice
from tests import load_fixture
from tests.syrupy import MelCloudSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the MELCloud extension."""
    return snapshot.use_extension(MelCloudSnapshotExtension)


@pytest.fixture(name="melcloud_client")
async def melcloud_client_fixture() -> AsyncGenerator[Client, None]:
    """Return a MELCloud client with a real session."""
    async with ClientSession() as session:
        yield Client(token="test_token", session=session, max_retries=0)


@pytest.fixture(name="ata_device")
async def ata_device_fixture(melcloud_client: Client) -> AtaDevice:
    """Return an ATA device loaded from fixtures."""
    device_conf = json.loads(load_fixture("ata_listdevice.json"))
    return AtaDevice(device_conf, melcloud_client)


@pytest.fixture(name="ata_device_with_state")
async def ata_device_with_state_fixture(ata_device: AtaDevice) -> AtaDevice:
    """Return an ATA device with state pre-loaded from fixtures."""
    ata_device._state = json.loads(load_fixture("ata_get.json"))
    return ata_device


@pytest.fixture(name="atw_1zone_device")
async def atw_1zone_device_fixture(melcloud_client: Client) -> AtwDevice:
    """Return a 1-zone ATW device loaded from fixtures."""
    device_conf = json.loads(load_fixture("atw_1zone_listdevice.json"))
    return AtwDevice(device_conf, melcloud_client)


@pytest.fixture(name="atw_1zone_device_with_state")
async def atw_1zone_device_with_state_fixture(atw_1zone_device: AtwDevice) -> AtwDevice:
    """Return a 1-zone ATW device with state pre-loaded from fixtures."""
    atw_1zone_device._state = json.loads(load_fixture("atw_1zone_get.json"))
    return atw_1zone_device


@pytest.fixture(name="atw_2zone_device")
async def atw_2zone_device_fixture(melcloud_client: Client) -> AtwDevice:
    """Return a 2-zone ATW device loaded from fixtures."""
    device_conf = json.loads(load_fixture("atw_2zone_listdevice.json"))
    return AtwDevice(device_conf, melcloud_client)


@pytest.fixture(name="atw_2zone_device_with_state")
async def atw_2zone_device_with_state_fixture(atw_2zone_device: AtwDevice) -> AtwDevice:
    """Return a 2-zone ATW device with state pre-loaded from fixtures."""
    atw_2zone_device._state = json.loads(load_fixture("atw_2zone_get.json"))
    return atw_2zone_device


@pytest.fixture(name="atw_2zone_cancool_device_with_state")
async def atw_2zone_cancool_device_with_state_fixture(
    melcloud_client: Client,
) -> AtwDevice:
    """Return a 2-zone ATW device (with cool capability) with state pre-loaded."""
    device_conf = json.loads(load_fixture("atw_2zone_cancool_listdevice.json"))
    device = AtwDevice(device_conf, melcloud_client)
    device._state = json.loads(load_fixture("atw_2zone_cancool_get.json"))
    return device


@pytest.fixture(name="erv_device")
async def erv_device_fixture(melcloud_client: Client) -> ErvDevice:
    """Return an ERV device loaded from fixtures."""
    device_conf = json.loads(load_fixture("erv_listdevice.json"))
    return ErvDevice(device_conf, melcloud_client)


@pytest.fixture(name="erv_device_with_state")
async def erv_device_with_state_fixture(erv_device: ErvDevice) -> ErvDevice:
    """Return an ERV device with state pre-loaded from fixtures."""
    erv_device._state = json.loads(load_fixture("erv_get.json"))
    return erv_device
