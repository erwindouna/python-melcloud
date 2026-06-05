"""Air-to-Air device property tests."""

from typing import Any

import pytest
from syrupy.assertion import SnapshotAssertion

from pymelcloud import DEVICE_TYPE_ATA
from pymelcloud.ata_device import (
    FAN_SPEED_AUTO,
    H_VANE_POSITION_3,
    H_VANE_POSITION_AUTO,
    H_VANE_POSITION_SPLIT,
    H_VANE_POSITION_SWING,
    H_VANE_POSITION_UNDEFINED,
    OPERATION_MODE_COOL,
    OPERATION_MODE_DRY,
    OPERATION_MODE_FAN_ONLY,
    OPERATION_MODE_HEAT,
    OPERATION_MODE_HEAT_COOL,
    OPERATION_MODE_UNDEFINED,
    V_VANE_POSITION_5,
    V_VANE_POSITION_AUTO,
    V_VANE_POSITION_SWING,
    V_VANE_POSITION_UNDEFINED,
    AtaDevice,
)
from pymelcloud.const import ACCESS_LEVEL


def test_ata_before_update(ata_device: AtaDevice) -> None:
    """Test ATA device properties before any state has been loaded."""
    assert ata_device.name == ""
    assert ata_device.device_type == DEVICE_TYPE_ATA
    assert ata_device.access_level == ACCESS_LEVEL["OWNER"]
    assert ata_device.temperature_increment == 0.5
    assert ata_device.has_energy_consumed_meter is False
    assert ata_device.room_temperature is None
    assert ata_device.fan_speed is None
    assert ata_device.fan_speeds is None
    assert ata_device.operation_mode == OPERATION_MODE_UNDEFINED
    assert ata_device.target_temperature is None
    assert ata_device.target_temperature_min is None
    assert ata_device.target_temperature_max is None
    assert ata_device.vane_horizontal is None
    assert ata_device.vane_vertical is None
    assert ata_device.power is None
    assert ata_device.has_error is False
    assert ata_device.error_code is None
    assert ata_device.last_seen is None


def test_ata_operation_modes(
    ata_device: AtaDevice, snapshot: SnapshotAssertion
) -> None:
    """Test that available operation modes match snapshot."""
    assert ata_device.operation_modes == [
        OPERATION_MODE_HEAT,
        OPERATION_MODE_DRY,
        OPERATION_MODE_COOL,
        OPERATION_MODE_FAN_ONLY,
        OPERATION_MODE_HEAT_COOL,
    ]
    assert ata_device.operation_modes == snapshot


def test_ata_after_state(ata_device_with_state: AtaDevice) -> None:
    """Test ATA device properties once state has been loaded."""
    assert ata_device_with_state.room_temperature == 28.0
    assert ata_device_with_state.target_temperature == 22.0
    assert ata_device_with_state.operation_mode == OPERATION_MODE_COOL
    assert ata_device_with_state.fan_speed == "3"
    assert ata_device_with_state.actual_fan_speed == "0"
    assert ata_device_with_state.fan_speeds == ["auto", "1", "2", "3", "4", "5"]
    assert ata_device_with_state.vane_vertical == V_VANE_POSITION_AUTO
    assert ata_device_with_state.vane_horizontal == H_VANE_POSITION_3
    assert ata_device_with_state.wifi_signal == -51
    assert ata_device_with_state.has_error is False
    assert ata_device_with_state.error_code == 8000
    assert ata_device_with_state.power is False


def test_ata_properties_snapshot(
    ata_device_with_state: AtaDevice,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot test for key ATA device state properties."""
    assert {
        "room_temperature": ata_device_with_state.room_temperature,
        "target_temperature": ata_device_with_state.target_temperature,
        "operation_mode": ata_device_with_state.operation_mode,
        "fan_speed": ata_device_with_state.fan_speed,
        "fan_speeds": ata_device_with_state.fan_speeds,
        "vane_vertical": ata_device_with_state.vane_vertical,
        "vane_horizontal": ata_device_with_state.vane_horizontal,
        "power": ata_device_with_state.power,
        "has_error": ata_device_with_state.has_error,
        "error_code": ata_device_with_state.error_code,
        "wifi_signal": ata_device_with_state.wifi_signal,
    } == snapshot


def test_ata_target_temperature_range(ata_device_with_state: AtaDevice) -> None:
    """Test temperature range properties."""
    assert ata_device_with_state.target_temperature_min is not None
    assert ata_device_with_state.target_temperature_max is not None
    assert ata_device_with_state.target_temperature_step == 0.5


def test_apply_write_target_temperature(ata_device_with_state: AtaDevice) -> None:
    """Test apply_write sets SetTemperature with correct flag."""
    state: dict[str, Any] = {"EffectiveFlags": 0}
    ata_device_with_state.apply_write(state, "target_temperature", 24.0)
    assert state["SetTemperature"] == 24.0
    assert state["EffectiveFlags"] & 0x04 != 0


def test_apply_write_operation_mode(ata_device_with_state: AtaDevice) -> None:
    """Test apply_write sets OperationMode with correct flag."""
    state: dict[str, Any] = {"EffectiveFlags": 0}
    ata_device_with_state.apply_write(state, "operation_mode", OPERATION_MODE_HEAT)
    assert state["OperationMode"] == 1
    assert state["EffectiveFlags"] & 0x02 != 0


def test_apply_write_fan_speed(ata_device_with_state: AtaDevice) -> None:
    """Test apply_write sets SetFanSpeed for 'auto'."""
    state: dict[str, Any] = {"EffectiveFlags": 0}
    ata_device_with_state.apply_write(state, "fan_speed", FAN_SPEED_AUTO)
    assert state["SetFanSpeed"] == 0
    assert state["EffectiveFlags"] & 0x08 != 0

    state = {"EffectiveFlags": 0}
    ata_device_with_state.apply_write(state, "fan_speed", "3")
    assert state["SetFanSpeed"] == 3


def test_apply_write_vane_horizontal(ata_device_with_state: AtaDevice) -> None:
    """Test apply_write sets VaneHorizontal with correct flag."""
    state: dict[str, Any] = {"EffectiveFlags": 0}
    ata_device_with_state.apply_write(state, "vane_horizontal", H_VANE_POSITION_3)
    assert state["VaneHorizontal"] == 3
    assert state["EffectiveFlags"] & 0x100 != 0


def test_apply_write_vane_vertical(ata_device_with_state: AtaDevice) -> None:
    """Test apply_write sets VaneVertical with correct flag."""
    state: dict[str, Any] = {"EffectiveFlags": 0}
    ata_device_with_state.apply_write(state, "vane_vertical", V_VANE_POSITION_AUTO)
    assert state["VaneVertical"] == 0
    assert state["EffectiveFlags"] & 0x10 != 0


def test_apply_write_invalid_property(ata_device_with_state: AtaDevice) -> None:
    """Test apply_write raises ValueError for unknown property."""
    with pytest.raises(ValueError, match="Cannot set unknown_prop"):
        ata_device_with_state.apply_write({}, "unknown_prop", "value")


def test_apply_write_invalid_vane_horizontal(ata_device_with_state: AtaDevice) -> None:
    """Test that _horizontal_vane_to raises ValueError for invalid position."""
    with pytest.raises(ValueError, match="Invalid horizontal vane position"):
        ata_device_with_state.apply_write({}, "vane_horizontal", "invalid_position")


def test_apply_write_invalid_vane_vertical(ata_device_with_state: AtaDevice) -> None:
    """Test that _vertical_vane_to raises ValueError for invalid position."""
    with pytest.raises(ValueError, match="Invalid vertical vane position"):
        ata_device_with_state.apply_write({}, "vane_vertical", "invalid_position")


def test_apply_write_invalid_operation_mode(ata_device_with_state: AtaDevice) -> None:
    """Test that _operation_mode_to raises ValueError for invalid mode."""
    with pytest.raises(ValueError, match="Invalid operation_mode"):
        ata_device_with_state.apply_write({}, "operation_mode", "invalid_mode")


def test_vane_horizontal_positions_with_swing(ata_device: AtaDevice) -> None:
    """Test vane_horizontal_positions returns all positions including swing."""
    device = ata_device._device_conf.get("Device", {})
    # Enable vane support and swing
    device["ModelSupportsVaneVertical"] = True
    device["SwingFunction"] = True
    ata_device._device_conf["HideVaneControls"] = False

    positions = ata_device.vane_horizontal_positions
    assert positions is not None
    assert H_VANE_POSITION_AUTO in positions
    assert H_VANE_POSITION_SWING in positions
    assert H_VANE_POSITION_SPLIT in positions


def test_vane_horizontal_positions_no_model_support(ata_device: AtaDevice) -> None:
    """Test vane_horizontal_positions returns [] when not supported."""
    ata_device._device_conf.get("Device", {})["ModelSupportsVaneVertical"] = False
    assert ata_device.vane_horizontal_positions == []


def test_vane_horizontal_positions_hidden(ata_device: AtaDevice) -> None:
    """Test vane_horizontal_positions returns [] when hidden."""
    ata_device._device_conf["HideVaneControls"] = True
    assert ata_device.vane_horizontal_positions == []


def test_vane_vertical_positions_with_swing(ata_device: AtaDevice) -> None:
    """Test vane_vertical_positions returns all positions including swing."""
    device = ata_device._device_conf.get("Device", {})
    device["ModelSupportsVaneHorizontal"] = True
    device["SwingFunction"] = True
    ata_device._device_conf["HideVaneControls"] = False

    positions = ata_device.vane_vertical_positions
    assert positions is not None
    assert V_VANE_POSITION_AUTO in positions
    assert V_VANE_POSITION_SWING in positions
    assert V_VANE_POSITION_5 in positions


def test_vane_vertical_positions_no_model_support(ata_device: AtaDevice) -> None:
    """Test vane_vertical_positions returns [] when not supported."""
    ata_device._device_conf.get("Device", {})["ModelSupportsVaneHorizontal"] = False
    assert ata_device.vane_vertical_positions == []


def test_vane_vertical_positions_hidden(ata_device: AtaDevice) -> None:
    """Test vane_vertical_positions returns [] when hidden."""
    ata_device._device_conf["HideVaneControls"] = True
    assert ata_device.vane_vertical_positions == []


def test_outdoor_temperature_hidden(ata_device: AtaDevice) -> None:
    """Test outdoor_temperature returns None when HideOutdoorTemperature is True."""
    ata_device._device_conf["HideOutdoorTemperature"] = True
    assert ata_device.outdoor_temperature is None
    assert ata_device.has_outdoor_temperature is False


def test_outdoor_temperature_no_sensor(ata_device: AtaDevice) -> None:
    """Test outdoor_temperature returns None when device has no outdoor sensor."""
    ata_device._device_conf["HideOutdoorTemperature"] = False
    ata_device._device_conf.get("Device", {})["HasOutdoorTemperature"] = False
    assert ata_device.outdoor_temperature is None
    assert ata_device.has_outdoor_temperature is False


def test_outdoor_temperature_available(ata_device: AtaDevice) -> None:
    """Test outdoor_temperature returns value when sensor is present."""
    ata_device._device_conf["HideOutdoorTemperature"] = False
    device = ata_device._device_conf.get("Device", {})
    device["HasOutdoorTemperature"] = True
    device["OutdoorTemperature"] = 25.5

    assert ata_device.has_outdoor_temperature is True
    assert ata_device.outdoor_temperature == 25.5


def test_total_energy_consumed_zero_returns_last(ata_device: AtaDevice) -> None:
    """Test total_energy_consumed returns last known value when current is 0.0."""
    device = ata_device._device_conf.get("Device", {})
    device["CurrentEnergyConsumed"] = 5000.0
    first = ata_device.total_energy_consumed
    assert first == 5.0

    device["CurrentEnergyConsumed"] = 0.0
    second = ata_device.total_energy_consumed
    assert second == 5.0  # Returns last_energy_value


def test_total_energy_consumed_none_when_no_value(ata_device: AtaDevice) -> None:
    """Test total_energy_consumed returns None when no current energy data."""
    device = ata_device._device_conf.get("Device", {})
    device.pop("CurrentEnergyConsumed", None)
    assert ata_device.total_energy_consumed is None


def test_fan_speed_auto_with_state(ata_device_with_state: AtaDevice) -> None:
    """Test fan_speed returns 'auto' when SetFanSpeed is 0."""
    assert ata_device_with_state._state is not None
    ata_device_with_state._state["SetFanSpeed"] = 0
    assert ata_device_with_state.fan_speed == FAN_SPEED_AUTO


def test_vane_horizontal_undefined(ata_device_with_state: AtaDevice) -> None:
    """Test vane_horizontal returns 'undefined' for unknown position codes."""
    assert ata_device_with_state._state is not None
    ata_device_with_state._state["VaneHorizontal"] = 99
    assert ata_device_with_state.vane_horizontal == H_VANE_POSITION_UNDEFINED


def test_vane_vertical_undefined(ata_device_with_state: AtaDevice) -> None:
    """Test vane_vertical returns 'undefined' for unknown position codes."""
    assert ata_device_with_state._state is not None
    ata_device_with_state._state["VaneVertical"] = 99
    assert ata_device_with_state.vane_vertical == V_VANE_POSITION_UNDEFINED
