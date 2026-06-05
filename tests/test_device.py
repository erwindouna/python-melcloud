"""Base device tests."""

import pytest
from aresponses import ResponsesMockServer

from pymelcloud.ata_device import AtaDevice
from tests import load_fixture


@pytest.fixture(name="ata_device_energy")
def ata_device_energy_fixture(ata_device_with_state: AtaDevice) -> AtaDevice:
    """Return an ATA device with a non-trivial energy report."""
    ata_device_with_state._energy_report = {
        "Heating": [0.0, 0.0, 1.0],
        "Cooling": [0.0, 0.1, 10.0],
        "Dry": [0.2, 0.0, 100.0],
        "Fan": [0.3, 1000.0],
    }
    return ata_device_with_state


def test_round_temperature_half_degree(ata_device: AtaDevice) -> None:
    """Test temperature rounding for 0.5°C increment."""
    ata_device._device_conf["Device"]["TemperatureIncrement"] = 0.5

    assert ata_device.round_temperature(23.99999) == 24.0
    assert ata_device.round_temperature(24.0) == 24.0
    assert ata_device.round_temperature(24.00001) == 24.0
    assert ata_device.round_temperature(24.24999) == 24.0
    assert ata_device.round_temperature(24.25) == 24.5
    assert ata_device.round_temperature(24.25001) == 24.5
    assert ata_device.round_temperature(24.5) == 24.5
    assert ata_device.round_temperature(24.74999) == 24.5
    assert ata_device.round_temperature(24.75) == 25.0
    assert ata_device.round_temperature(24.75001) == 25.0


def test_round_temperature_one_degree(ata_device: AtaDevice) -> None:
    """Test temperature rounding for 1°C increment."""
    ata_device._device_conf["Device"]["TemperatureIncrement"] = 1

    assert ata_device.round_temperature(23.99999) == 24.0
    assert ata_device.round_temperature(24.0) == 24.0
    assert ata_device.round_temperature(24.00001) == 24.0
    assert ata_device.round_temperature(24.49999) == 24.0
    assert ata_device.round_temperature(24.5) == 25.0
    assert ata_device.round_temperature(24.50001) == 25.0
    assert ata_device.round_temperature(25.0) == 25.0
    assert ata_device.round_temperature(25.00001) == 25.0
    assert ata_device.round_temperature(25.49999) == 25.0
    assert ata_device.round_temperature(25.5) == 26.0


def test_energy_report_none_before_state(ata_device: AtaDevice) -> None:
    """daily_energy_consumed is None when no state has been loaded."""
    assert ata_device.daily_energy_consumed is None


def test_energy_report_none_when_no_report(ata_device_with_state: AtaDevice) -> None:
    """daily_energy_consumed is None when state is set but no energy report exists."""
    ata_device_with_state._energy_report = None
    assert ata_device_with_state.daily_energy_consumed is None


def test_energy_report_sums_last_values(ata_device_energy: AtaDevice) -> None:
    """daily_energy_consumed sums the last entry of each energy mode bucket."""
    assert ata_device_energy.daily_energy_consumed == 1111.0


def test_units_none_before_fetch(ata_device: AtaDevice) -> None:
    """Units property returns None when device units have not been fetched."""
    assert ata_device.units is None


def test_units_returns_model_info(ata_device: AtaDevice) -> None:
    """Units property returns model info from _device_units when loaded."""
    ata_device._device_units = [
        {"ModelNumber": "MSZ-AP20VGK", "Model": "AP20", "SerialNumber": "SN123"},
        {"ModelNumber": "MUZ-AP20VG", "Model": "AP20", "SerialNumber": "SN456"},
    ]
    units = ata_device.units
    assert units is not None
    assert len(units) == 2
    assert units[0]["model_number"] == "MSZ-AP20VGK"
    assert units[0]["model"] == "AP20"
    assert units[0]["serial_number"] == "SN123"
    assert units[1]["serial_number"] == "SN456"


def test_last_seen_none_before_state(ata_device: AtaDevice) -> None:
    """last_seen returns None when no state has been loaded."""
    assert ata_device.last_seen is None


def test_last_seen_with_state(ata_device_with_state: AtaDevice) -> None:
    """last_seen returns parsed UTC datetime when state is available."""
    last_seen = ata_device_with_state.last_seen
    assert last_seen is not None
    assert str(last_seen) == "2020-07-03 09:03:50.320000+00:00"


def test_temp_unit_celsius(ata_device: AtaDevice) -> None:
    """temp_unit returns Celsius when UseFahrenheit is False."""
    from pymelcloud.const import UNIT_TEMP_CELSIUS

    assert ata_device.temp_unit == UNIT_TEMP_CELSIUS


@pytest.mark.asyncio
async def test_update_fetches_state(
    aresponses: ResponsesMockServer,
    ata_device: AtaDevice,
) -> None:
    """update() fetches conf, state, energy report and device units."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/User/ListDevices",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("list_devices.json"),
        ),
    )
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/User/GetUserDetails",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("user_details.json"),
        ),
    )
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Device/Get",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("ata_get.json"),
        ),
    )
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/EnergyCost/Report",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"Heating": [1.0], "Cooling": [0.5]}',
        ),
    )
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Device/ListDeviceUnits",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=(
                '[{"ModelNumber": "MSZ-AP20VGK", "Model": "AP20",'
                ' "SerialNumber": "SN123"}]'
            ),
        ),
    )

    await ata_device.update()

    assert ata_device._state is not None
    assert ata_device.room_temperature == 28.0
    assert ata_device._energy_report is not None
    assert ata_device._device_units is not None


@pytest.mark.asyncio
async def test_set_writes_property(
    aresponses: ResponsesMockServer,
    ata_device_with_state: AtaDevice,
) -> None:
    """set() schedules and executes a state write immediately (debounce=0)."""
    from datetime import timedelta

    ata_device_with_state._set_debounce = timedelta(seconds=0)

    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Device/SetAta",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("ata_get.json"),
        ),
    )

    await ata_device_with_state.set({"target_temperature": 24.0})

    assert ata_device_with_state._state is not None
