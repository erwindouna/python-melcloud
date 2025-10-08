"""Device tests."""

from typing import Any

import pytest

from src.pymelcloud.ata_device import AtaDevice

from .util import build_device


def _build_device(
    device_conf_name: str,
    device_state_name: str,
    energy_report: dict[Any, Any] | None = None,
) -> AtaDevice:
    device_conf, client = build_device(
        device_conf_name, device_state_name, energy_report
    )
    return AtaDevice(device_conf, client)


@pytest.mark.asyncio
async def test_round_temperature() -> None:
    """Test temperature rounding functionality."""
    device = _build_device("ata_listdevice.json", "ata_get.json")
    device._device_conf.setdefault("Device", {})["TemperatureIncrement"] = 0.5  # noqa: SLF001

    assert device.round_temperature(23.99999) == 24.0
    assert device.round_temperature(24.0) == 24.0
    assert device.round_temperature(24.00001) == 24.0
    assert device.round_temperature(24.24999) == 24.0
    assert device.round_temperature(24.25) == 24.5
    assert device.round_temperature(24.25001) == 24.5
    assert device.round_temperature(24.5) == 24.5
    assert device.round_temperature(24.74999) == 24.5
    assert device.round_temperature(24.75) == 25.0
    assert device.round_temperature(24.75001) == 25.0

    device._device_conf.setdefault("Device", {})["TemperatureIncrement"] = 1  # noqa: SLF001

    assert device.round_temperature(23.99999) == 24.0
    assert device.round_temperature(24.0) == 24.0
    assert device.round_temperature(24.00001) == 24.0
    assert device.round_temperature(24.49999) == 24.0
    assert device.round_temperature(24.5) == 25.0
    assert device.round_temperature(24.50001) == 25.0
    assert device.round_temperature(25.0) == 25.0
    assert device.round_temperature(25.00001) == 25.0
    assert device.round_temperature(25.49999) == 25.0
    assert device.round_temperature(25.5) == 26.0


@pytest.mark.asyncio
async def test_energy_report_none_if_no_report() -> None:
    """Test energy report returns None when no report is available."""
    device = _build_device("ata_listdevice.json", "ata_get.json")

    await device.update()

    assert device.daily_energy_consumed is None


def test_energy_report_before_update() -> None:
    """Test energy report before device state update."""
    device = _build_device("ata_listdevice.json", "ata_get.json")

    assert device.daily_energy_consumed is None


@pytest.mark.asyncio
async def test_energy_report_with_report() -> None:
    """Test energy report with actual report data."""
    device = _build_device(
        "ata_listdevice.json",
        "ata_get.json",
        {
            "Heating": [0.0, 0.0, 1.0],
            "Cooling": [0.0, 0.1, 10.0],
            "Dry": [0.2, 0.0, 100.0],
            "Fan": [0.3, 1000.0],
        },
    )

    await device.update()

    assert device.daily_energy_consumed == 1111.0
