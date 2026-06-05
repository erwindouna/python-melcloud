"""Air-to-Water device property tests."""

from typing import Any

import pytest
from syrupy.assertion import SnapshotAssertion

from pymelcloud import DEVICE_TYPE_ATW
from pymelcloud.atw_device import (
    OPERATION_MODE_AUTO,
    OPERATION_MODE_FORCE_HOT_WATER,
    STATUS_HEAT_WATER,
    STATUS_HEAT_ZONES,
    STATUS_UNKNOWN,
    ZONE_OPERATION_MODE_COOL_FLOW,
    ZONE_OPERATION_MODE_COOL_THERMOSTAT,
    ZONE_OPERATION_MODE_CURVE,
    ZONE_OPERATION_MODE_HEAT_FLOW,
    ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
    ZONE_STATUS_HEAT,
    ZONE_STATUS_IDLE,
    ZONE_STATUS_UNKNOWN,
    AtwDevice,
)

pytestmark = [
    pytest.mark.filterwarnings("ignore:Zone.flow_temperature:DeprecationWarning"),
    pytest.mark.filterwarnings("ignore:Zone.return_temperature:DeprecationWarning"),
]


def test_1zone_before_state(atw_1zone_device: AtwDevice) -> None:
    """Test 1-zone ATW device properties before state is loaded."""
    assert atw_1zone_device.name == "Heater and Water"
    assert atw_1zone_device.device_type == DEVICE_TYPE_ATW
    assert atw_1zone_device.temperature_increment == 0.5
    assert atw_1zone_device.operation_mode is None
    assert atw_1zone_device.operation_modes == [
        OPERATION_MODE_AUTO,
        OPERATION_MODE_FORCE_HOT_WATER,
    ]
    assert atw_1zone_device.tank_temperature is None
    assert atw_1zone_device.status is STATUS_UNKNOWN
    assert atw_1zone_device.target_tank_temperature is None
    assert atw_1zone_device.target_tank_temperature_min == 40
    assert atw_1zone_device.target_tank_temperature_max == 60
    assert atw_1zone_device.flow_temperature == 57.5
    assert atw_1zone_device.return_temperature == 53.0
    assert atw_1zone_device.flow_temperature_boiler == 25
    assert atw_1zone_device.return_temperature_boiler == 25
    assert atw_1zone_device.mixing_tank_temperature == 0
    assert atw_1zone_device.condensing_temperature == 0
    assert atw_1zone_device.heat_pump_frequency == 50
    assert atw_1zone_device.boiler_status is False
    assert atw_1zone_device.booster_heater1_status is False
    assert atw_1zone_device.booster_heater2_status is False
    assert atw_1zone_device.booster_heater2plus_status is False
    assert atw_1zone_device.immersion_heater_status is False
    assert atw_1zone_device.water_pump1_status is True
    assert atw_1zone_device.water_pump2_status is True
    assert atw_1zone_device.water_pump3_status is False
    assert atw_1zone_device.water_pump4_status is False
    assert atw_1zone_device.valve_3way_status is False
    assert atw_1zone_device.valve_2way_status is True
    assert atw_1zone_device.demand_percentage is None
    assert atw_1zone_device.daily_heating_energy_consumed is None
    assert atw_1zone_device.holiday_mode is None
    assert atw_1zone_device.wifi_signal == -73
    assert atw_1zone_device.has_error is False
    assert atw_1zone_device.error_code is None

    zones = atw_1zone_device.zones
    assert zones is not None
    assert len(zones) == 1
    assert zones[0].name == "Zone 1"
    assert zones[0].zone_index == 1
    assert zones[0].room_temperature is None
    assert zones[0].target_temperature is None
    assert zones[0].flow_temperature == 57.5
    assert zones[0].return_temperature == 53.0
    assert zones[0].zone_flow_temperature == 25.0
    assert zones[0].zone_return_temperature == 25.0
    assert zones[0].target_flow_temperature is None
    assert zones[0].operation_mode is None
    assert zones[0].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
    ]
    assert zones[0].status == ZONE_STATUS_UNKNOWN


def test_1zone_after_state(atw_1zone_device_with_state: AtwDevice) -> None:
    """Test 1-zone ATW device properties after state is loaded."""
    device = atw_1zone_device_with_state
    assert device.operation_mode == OPERATION_MODE_AUTO
    assert device.status == STATUS_HEAT_ZONES
    assert device.tank_temperature == 52.0
    assert device.target_tank_temperature == 50.0
    assert device.boiler_status is False
    assert device.water_pump1_status is True
    assert device.holiday_mode is False
    assert device.wifi_signal == -73
    assert device.has_error is False
    assert device.error_code == 8000

    zones = device.zones
    assert zones is not None
    assert zones[0].room_temperature == 27.0
    assert zones[0].target_temperature == 30
    assert zones[0].zone_flow_temperature == 25.0
    assert zones[0].zone_return_temperature == 25.0
    assert zones[0].target_flow_temperature == 60.0
    assert zones[0].operation_mode == ZONE_OPERATION_MODE_HEAT_FLOW
    assert zones[0].status == ZONE_STATUS_HEAT


def test_1zone_snapshot(
    atw_1zone_device_with_state: AtwDevice,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot test for 1-zone ATW device state properties."""
    device = atw_1zone_device_with_state
    zones = device.zones
    assert zones is not None
    assert {
        "operation_mode": device.operation_mode,
        "status": device.status,
        "tank_temperature": device.tank_temperature,
        "target_tank_temperature": device.target_tank_temperature,
        "zone_0_room_temp": zones[0].room_temperature,
        "zone_0_target_temp": zones[0].target_temperature,
        "zone_0_operation_mode": zones[0].operation_mode,
        "zone_0_status": zones[0].status,
    } == snapshot


def test_2zone_before_state(atw_2zone_device: AtwDevice) -> None:
    """Test 2-zone ATW device properties before state is loaded."""
    device = atw_2zone_device
    assert device.name == "Home"
    assert device.device_type == DEVICE_TYPE_ATW
    assert device.temperature_increment == 0.5
    assert device.daily_heating_energy_consumed == 5.2
    assert device.daily_cooling_energy_consumed == 0.0
    assert device.daily_hot_water_energy_consumed == 3.1
    assert device.daily_heating_energy_produced == 18.5
    assert device.daily_cooling_energy_produced == 0.0
    assert device.daily_hot_water_energy_produced == 11.0
    assert device.wifi_signal == -37

    zones = device.zones
    assert zones is not None
    assert len(zones) == 2
    assert zones[0].name == "Downstairs"
    assert zones[1].name == "Upstairs"


def test_2zone_after_state(atw_2zone_device_with_state: AtwDevice) -> None:
    """Test 2-zone ATW device properties after state is loaded."""
    device = atw_2zone_device_with_state
    assert device.operation_mode == OPERATION_MODE_AUTO
    assert device.status == STATUS_HEAT_ZONES
    assert device.tank_temperature == 49.5
    assert device.target_tank_temperature == 50.0
    assert device.demand_percentage == 75
    assert device.daily_heating_energy_consumed == 5.2
    assert device.daily_hot_water_energy_produced == 11.0
    assert device.holiday_mode is False
    assert device.has_error is False
    assert device.error_code == 8000

    zones = device.zones
    assert zones is not None
    assert zones[0].room_temperature == 20.5
    assert zones[0].target_temperature == 19.5
    assert zones[0].target_flow_temperature == 25.0
    assert zones[0].operation_mode == ZONE_OPERATION_MODE_HEAT_THERMOSTAT
    assert zones[0].status == ZONE_STATUS_HEAT

    assert zones[1].room_temperature == 19.5
    assert zones[1].target_temperature == 18
    assert zones[1].target_flow_temperature == 25.0
    assert zones[1].operation_mode == ZONE_OPERATION_MODE_HEAT_THERMOSTAT
    assert zones[1].status == ZONE_STATUS_HEAT


def test_2zone_cancool_before_state(
    atw_2zone_cancool_device_with_state: AtwDevice,
) -> None:
    """Test 2-zone ATW device (can-cool) before state is loaded."""
    # Since cancool fixture includes state, we just verify the conf-derived props
    device = atw_2zone_cancool_device_with_state
    assert device.name == "Mitsubishi"
    assert device.valve_3way_status is True

    zones = device.zones
    assert zones is not None
    assert len(zones) == 2
    assert zones[0].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
        ZONE_OPERATION_MODE_COOL_THERMOSTAT,
        ZONE_OPERATION_MODE_COOL_FLOW,
    ]


def test_2zone_cancool_after_state(
    atw_2zone_cancool_device_with_state: AtwDevice,
) -> None:
    """Test 2-zone ATW device (can-cool) after state is loaded."""
    device = atw_2zone_cancool_device_with_state
    assert device.operation_mode == OPERATION_MODE_AUTO
    assert device.status == STATUS_HEAT_WATER
    assert device.tank_temperature == 47.5
    assert device.target_tank_temperature == 52.0

    zones = device.zones
    assert zones is not None
    assert zones[0].room_temperature == 21.5
    assert zones[0].operation_mode == ZONE_OPERATION_MODE_CURVE
    assert zones[0].status == ZONE_STATUS_IDLE

    assert zones[1].room_temperature == 21.0
    assert zones[1].operation_mode == ZONE_OPERATION_MODE_CURVE
    assert zones[1].status == ZONE_STATUS_IDLE


def test_apply_write_cool_flow_property_strings(
    atw_2zone_cancool_device_with_state: AtwDevice,
) -> None:
    """Test that both new and deprecated cool flow property strings work correctly."""
    device = atw_2zone_cancool_device_with_state

    state: dict[str, Any] = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_1_target_cool_flow_temperature", 20.0)
    assert state["SetCoolFlowTemperatureZone1"] == 20.0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_2_target_cool_flow_temperature", 21.0)
    assert state["SetCoolFlowTemperatureZone2"] == 21.0

    # Deprecated backwards-compat aliases
    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_1_target_heat_cool_temperature", 20.0)
    assert state["SetCoolFlowTemperatureZone1"] == 20.0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_2_target_heat_cool_temperature", 21.0)
    assert state["SetCoolFlowTemperatureZone2"] == 21.0


def test_zone_flow_return_temperature_deprecation(atw_1zone_device: AtwDevice) -> None:
    """Test that flow_temperature and return_temperature raise DeprecationWarning."""
    zones = atw_1zone_device.zones
    assert zones is not None

    with pytest.deprecated_call():
        _ = zones[0].flow_temperature

    with pytest.deprecated_call():
        _ = zones[0].return_temperature


def test_apply_write_all_atw_properties(atw_2zone_device_with_state: AtwDevice) -> None:
    """Test apply_write for all AtwDevice property keys."""
    device = atw_2zone_device_with_state

    state: dict[str, Any] = {"EffectiveFlags": 0}
    device.apply_write(state, "target_tank_temperature", 50.0)
    assert state["SetTankWaterTemperature"] == 50.0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "operation_mode", OPERATION_MODE_AUTO)
    assert state["ForcedHotWaterMode"] is False

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "operation_mode", OPERATION_MODE_FORCE_HOT_WATER)
    assert state["ForcedHotWaterMode"] is True

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_1_target_temperature", 22.0)
    assert state["SetTemperatureZone1"] == 22.0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_2_target_temperature", 21.0)
    assert state["SetTemperatureZone2"] == 21.0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_1_target_heat_flow_temperature", 55.0)
    assert state["SetHeatFlowTemperatureZone1"] == 55.0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_2_target_heat_flow_temperature", 50.0)
    assert state["SetHeatFlowTemperatureZone2"] == 50.0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_1_operation_mode", 0)
    assert state["OperationModeZone1"] == 0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_2_operation_mode", 1)
    assert state["OperationModeZone2"] == 1


def test_apply_write_atw_invalid_property(
    atw_1zone_device_with_state: AtwDevice,
) -> None:
    """Test apply_write raises ValueError for unknown ATW property."""
    with pytest.raises(ValueError, match="Cannot set"):
        atw_1zone_device_with_state.apply_write({}, "invalid_property", "value")


def test_1zone_zone_prohibit(atw_1zone_device_with_state: AtwDevice) -> None:
    """Test zone prohibit property with state loaded."""
    zones = atw_1zone_device_with_state.zones
    assert zones is not None
    # prohibit may be None or a bool depending on fixture
    prohibit = zones[0].prohibit
    assert prohibit is None or isinstance(prohibit, bool)


def test_1zone_outside_temperature(atw_1zone_device_with_state: AtwDevice) -> None:
    """Test outside_temperature property when state is loaded."""
    temp = atw_1zone_device_with_state.outside_temperature
    assert temp is None or isinstance(temp, (int, float))


def test_2zone_zone_status_idle(atw_2zone_cancool_device_with_state: AtwDevice) -> None:
    """Test that zones report IDLE status correctly."""
    device = atw_2zone_cancool_device_with_state
    zones = device.zones
    assert zones is not None
    # Both zones are IDLE in the cancool fixture
    assert zones[0].status == ZONE_STATUS_IDLE
    assert zones[1].status == ZONE_STATUS_IDLE


@pytest.mark.asyncio
async def test_zone_set_target_temperature(
    atw_2zone_device_with_state: AtwDevice,
) -> None:
    """Test zone.set_target_temperature calls device.set with correct prop."""
    from unittest.mock import AsyncMock, patch

    device = atw_2zone_device_with_state
    zones = device.zones
    assert zones is not None

    with patch.object(device, "set", new_callable=AsyncMock) as mock_set:
        await zones[0].set_target_temperature(22.0)
        mock_set.assert_called_once_with({"zone_1_target_temperature": 22.0})

        mock_set.reset_mock()
        await zones[1].set_target_temperature(20.0)
        mock_set.assert_called_once_with({"zone_2_target_temperature": 20.0})


@pytest.mark.asyncio
async def test_zone_set_target_heat_flow_temperature(
    atw_2zone_device_with_state: AtwDevice,
) -> None:
    """Test zone.set_target_heat_flow_temperature calls device.set with correct prop."""
    from unittest.mock import AsyncMock, patch

    device = atw_2zone_device_with_state
    zones = device.zones
    assert zones is not None

    with patch.object(device, "set", new_callable=AsyncMock) as mock_set:
        await zones[0].set_target_heat_flow_temperature(55.0)
        mock_set.assert_called_once_with({"zone_1_target_heat_flow_temperature": 55.0})

        mock_set.reset_mock()
        await zones[1].set_target_heat_flow_temperature(50.0)
        mock_set.assert_called_once_with({"zone_2_target_heat_flow_temperature": 50.0})


@pytest.mark.asyncio
async def test_zone_set_target_cool_flow_temperature(
    atw_2zone_cancool_device_with_state: AtwDevice,
) -> None:
    """Test zone.set_target_cool_flow_temperature calls device.set with correct prop."""
    from unittest.mock import AsyncMock, patch

    device = atw_2zone_cancool_device_with_state
    zones = device.zones
    assert zones is not None

    with patch.object(device, "set", new_callable=AsyncMock) as mock_set:
        await zones[0].set_target_cool_flow_temperature(20.0)
        mock_set.assert_called_once_with({"zone_1_target_cool_flow_temperature": 20.0})

        mock_set.reset_mock()
        await zones[1].set_target_cool_flow_temperature(19.0)
        mock_set.assert_called_once_with({"zone_2_target_cool_flow_temperature": 19.0})


@pytest.mark.asyncio
async def test_zone_set_target_flow_temperature_heat_mode(
    atw_2zone_device_with_state: AtwDevice,
) -> None:
    """Test set_target_flow_temperature dispatches to heat or cool based on mode."""
    from unittest.mock import AsyncMock, patch

    device = atw_2zone_device_with_state
    zones = device.zones
    assert zones is not None
    # Zone is in heat mode for this fixture
    assert zones[0].operation_mode in [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
    ]

    with patch.object(
        zones[0], "set_target_heat_flow_temperature", new_callable=AsyncMock
    ) as mock_heat:
        await zones[0].set_target_flow_temperature(55.0)
        mock_heat.assert_called_once_with(55.0)


@pytest.mark.asyncio
async def test_zone_set_operation_mode(
    atw_2zone_device_with_state: AtwDevice,
) -> None:
    """Test zone.set_operation_mode calls device.set with correct prop."""
    from unittest.mock import AsyncMock, patch

    device = atw_2zone_device_with_state
    zones = device.zones
    assert zones is not None

    with patch.object(device, "set", new_callable=AsyncMock) as mock_set:
        await zones[0].set_operation_mode(ZONE_OPERATION_MODE_HEAT_THERMOSTAT)
        mock_set.assert_called_once_with({"zone_1_operation_mode": 0})

        mock_set.reset_mock()
        await zones[1].set_operation_mode(ZONE_OPERATION_MODE_HEAT_FLOW)
        mock_set.assert_called_once_with({"zone_2_operation_mode": 1})


@pytest.mark.asyncio
async def test_zone_set_operation_mode_invalid(
    atw_2zone_device_with_state: AtwDevice,
) -> None:
    """Test zone.set_operation_mode raises ValueError for invalid modes."""
    device = atw_2zone_device_with_state
    zones = device.zones
    assert zones is not None

    with pytest.raises(ValueError, match="Invalid mode"):
        await zones[0].set_operation_mode("invalid_mode")
