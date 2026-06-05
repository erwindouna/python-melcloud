"""Energy-Recovery-Ventilation device property tests."""

from typing import Any

import pytest
from syrupy.assertion import SnapshotAssertion

from pymelcloud import DEVICE_TYPE_ERV
from pymelcloud.erv_device import (
    VENTILATION_MODE_AUTO,
    VENTILATION_MODE_BYPASS,
    VENTILATION_MODE_RECOVERY,
    ErvDevice,
)


def test_erv_before_state(erv_device: ErvDevice) -> None:
    """Test ERV device properties before state is loaded."""
    assert erv_device.name == ""
    assert erv_device.device_type == DEVICE_TYPE_ERV
    assert erv_device.temperature_increment == 1.0
    assert erv_device.has_energy_consumed_meter is True
    assert erv_device.total_energy_consumed == 0.1
    assert erv_device.room_temperature is None
    assert erv_device.outside_temperature is None
    assert erv_device.room_co2_level is None
    assert erv_device.ventilation_mode is None
    assert erv_device.actual_ventilation_mode is None
    assert erv_device.fan_speed is None
    assert erv_device.fan_speeds is None
    assert erv_device.actual_supply_fan_speed is None
    assert erv_device.actual_exhaust_fan_speed is None
    assert erv_device.core_maintenance_required is False
    assert erv_device.filter_maintenance_required is False
    assert erv_device.night_purge_mode is False


def test_erv_ventilation_modes(
    erv_device: ErvDevice, snapshot: SnapshotAssertion
) -> None:
    """Test that available ventilation modes match snapshot."""
    assert erv_device.ventilation_modes == [
        VENTILATION_MODE_RECOVERY,
        VENTILATION_MODE_BYPASS,
        VENTILATION_MODE_AUTO,
    ]
    assert erv_device.ventilation_modes == snapshot


def test_erv_after_state(erv_device_with_state: ErvDevice) -> None:
    """Test ERV device properties after state is loaded."""
    device = erv_device_with_state
    assert device.room_temperature == 29.0
    assert device.outside_temperature == 28.0
    assert device.room_co2_level is None
    assert device.ventilation_mode == VENTILATION_MODE_RECOVERY
    assert device.actual_ventilation_mode == VENTILATION_MODE_RECOVERY
    assert device.fan_speed == "3"
    assert device.fan_speeds == ["1", "2", "3", "4"]
    assert device.actual_supply_fan_speed == "3"
    assert device.actual_exhaust_fan_speed == "3"
    assert device.core_maintenance_required is False
    assert device.filter_maintenance_required is False
    assert device.night_purge_mode is False
    assert device.wifi_signal == -65
    assert device.has_error is False
    assert device.error_code == 8000
    assert str(device.last_seen) == "2020-07-07 06:44:11.027000+00:00"


def test_erv_properties_snapshot(
    erv_device_with_state: ErvDevice,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot test for key ERV device state properties."""
    device = erv_device_with_state
    assert {
        "room_temperature": device.room_temperature,
        "outside_temperature": device.outside_temperature,
        "ventilation_mode": device.ventilation_mode,
        "fan_speed": device.fan_speed,
        "fan_speeds": device.fan_speeds,
        "has_error": device.has_error,
        "error_code": device.error_code,
        "wifi_signal": device.wifi_signal,
    } == snapshot


def test_erv_apply_write_ventilation_mode(erv_device_with_state: ErvDevice) -> None:
    """Test apply_write sets VentilationMode with correct flag."""
    state: dict[str, Any] = {"EffectiveFlags": 0}
    erv_device_with_state.apply_write(
        state, "ventilation_mode", VENTILATION_MODE_RECOVERY
    )
    assert state["VentilationMode"] == 0
    assert state["EffectiveFlags"] & 0x04 != 0


def test_erv_apply_write_fan_speed(erv_device_with_state: ErvDevice) -> None:
    """Test apply_write sets SetFanSpeed with correct flag."""
    state: dict[str, Any] = {"EffectiveFlags": 0}
    erv_device_with_state.apply_write(state, "fan_speed", "3")
    assert state["SetFanSpeed"] == 3
    assert state["EffectiveFlags"] & 0x08 != 0


def test_erv_apply_write_invalid_property(erv_device_with_state: ErvDevice) -> None:
    """Test apply_write raises ValueError for unknown property."""
    with pytest.raises(ValueError, match="Cannot set"):
        erv_device_with_state.apply_write({}, "invalid_prop", "value")


def test_erv_total_energy_consumed(erv_device: ErvDevice) -> None:
    """Test total_energy_consumed returns value in kWh."""
    erv_device._device_conf.get("Device", {})["CurrentEnergyConsumed"] = 3500.0
    erv_device._device_conf.get("Device", {})["HasEnergyConsumedMeter"] = True
    assert erv_device.total_energy_consumed == 3.5
    assert erv_device.has_energy_consumed_meter is True


def test_erv_total_energy_consumed_none(erv_device: ErvDevice) -> None:
    """Test total_energy_consumed returns None when no data."""
    erv_device._device_conf.get("Device", {}).pop("CurrentEnergyConsumed", None)
    assert erv_device.total_energy_consumed is None


def test_erv_presets(erv_device: ErvDevice) -> None:
    """Test presets property returns list from device_conf."""
    erv_device._device_conf["Presets"] = [
        {"name": "Sleep", "VentilationMode": 0},
        {"name": "Away", "VentilationMode": 1},
    ]
    presets = erv_device.presets
    assert len(presets) == 2
    assert presets[0]["name"] == "Sleep"


def test_erv_room_co2_level_without_sensor(erv_device_with_state: ErvDevice) -> None:
    """Test room_co2_level returns None when no CO2 sensor."""
    assert erv_device_with_state._state is not None
    erv_device_with_state._state["HasCO2Sensor"] = False
    assert erv_device_with_state.room_co2_level is None


def test_erv_room_co2_level_with_sensor(erv_device_with_state: ErvDevice) -> None:
    """Test room_co2_level returns value when CO2 sensor is present."""
    assert erv_device_with_state._state is not None
    erv_device_with_state._state["HasCO2Sensor"] = True
    erv_device_with_state._device_conf.get("Device", {})["RoomCO2Level"] = 850.0
    assert erv_device_with_state.room_co2_level == 850.0


def test_erv_ventilation_modes_auto_only(erv_device: ErvDevice) -> None:
    """Test ventilation_modes returns modes based on device capabilities."""
    device_conf = erv_device._device_conf.get("Device", {})
    device_conf["HasAutoVentilationMode"] = False
    device_conf["HasBypassVentilationMode"] = False
    modes = erv_device.ventilation_modes
    assert VENTILATION_MODE_RECOVERY in modes
    assert VENTILATION_MODE_BYPASS not in modes
    assert VENTILATION_MODE_AUTO not in modes
