"""ATA tests."""

import json
import os
from unittest.mock import AsyncMock, Mock, patch

import pytest
from aiohttp.web import HTTPForbidden

from src.pymelcloud import DEVICE_TYPE_ATA
from src.pymelcloud.ata_device import (
    H_VANE_POSITION_3,
    OPERATION_MODE_COOL,
    OPERATION_MODE_DRY,
    OPERATION_MODE_FAN_ONLY,
    OPERATION_MODE_HEAT,
    OPERATION_MODE_HEAT_COOL,
    V_VANE_POSITION_AUTO,
    AtaDevice,
)
from src.pymelcloud.const import ACCESS_LEVEL


def _build_device(device_conf_name: str, device_state_name: str) -> AtaDevice:
    test_dir = os.path.join(os.path.dirname(__file__), "samples")
    with open(os.path.join(test_dir, device_conf_name)) as json_file:
        device_conf = json.load(json_file)

    with open(os.path.join(test_dir, device_state_name)) as json_file:
        device_state = json.load(json_file)

    with patch("src.pymelcloud.client.Client") as _client:
        _client.update_confs = AsyncMock()
        _client.device_confs.__iter__ = Mock(return_value=[device_conf].__iter__())
        _client.fetch_device_units = AsyncMock(return_value=[])
        _client.fetch_device_state = AsyncMock(return_value=device_state)
        _client.fetch_energy_report = AsyncMock(return_value=None)
        client = _client

    return AtaDevice(device_conf, client)


@pytest.mark.asyncio
async def test_ata():
    device = _build_device("ata_listdevice.json", "ata_get.json")

    assert device.name == ""
    assert device.device_type == DEVICE_TYPE_ATA
    assert device.access_level == ACCESS_LEVEL["OWNER"]
    assert device.temperature_increment == 0.5
    assert device.has_energy_consumed_meter is False
    assert device.room_temperature is None

    assert device.operation_modes == [
        OPERATION_MODE_HEAT,
        OPERATION_MODE_DRY,
        OPERATION_MODE_COOL,
        OPERATION_MODE_FAN_ONLY,
        OPERATION_MODE_HEAT_COOL,
    ]
    assert device.fan_speed is None
    assert device.fan_speeds is None

    await device.update()

    assert device.room_temperature == 28.0
    assert device.target_temperature == 22.0

    assert device.operation_mode == OPERATION_MODE_COOL
    assert device.fan_speed == "3"
    assert device.actual_fan_speed == "0"
    assert device.fan_speeds == ["auto", "1", "2", "3", "4", "5"]

    assert device.vane_vertical == V_VANE_POSITION_AUTO
    assert device.vane_horizontal == H_VANE_POSITION_3

    assert device.wifi_signal == -51
    assert device.has_error is False
    assert device.error_code == 8000


@pytest.mark.asyncio
async def test_ata_guest():
    device = _build_device("ata_guest_listdevices.json", "ata_guest_get.json")
    device._client.fetch_device_units = AsyncMock(side_effect=HTTPForbidden)
    assert device.device_type == DEVICE_TYPE_ATA
    assert device.access_level == ACCESS_LEVEL["GUEST"]
    await device.update()
