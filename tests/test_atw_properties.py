"""Ecodan tests."""

import pytest

from src.pymelcloud import DEVICE_TYPE_ATW
from src.pymelcloud.atw_device import (
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

from .util import build_device

pytestmark = [
    pytest.mark.filterwarnings("ignore:Zone.flow_temperature:DeprecationWarning"),
    pytest.mark.filterwarnings("ignore:Zone.return_temperature:DeprecationWarning"),
]


def _build_device(device_conf_name: str, device_state_name: str) -> AtwDevice:
    device_conf, client = build_device(device_conf_name, device_state_name)
    return AtwDevice(device_conf, client)


@pytest.mark.asyncio
async def test_1zone():
    device = _build_device("atw_1zone_listdevice.json", "atw_1zone_get.json")

    assert device.name == "Heater and Water"
    assert device.device_type == DEVICE_TYPE_ATW
    assert device.temperature_increment == 0.5

    assert device.operation_mode is None
    assert device.operation_modes == [
        OPERATION_MODE_AUTO,
        OPERATION_MODE_FORCE_HOT_WATER,
    ]
    assert device.tank_temperature is None
    assert device.status is STATUS_UNKNOWN
    assert device.target_tank_temperature is None
    assert device.target_tank_temperature_min == 40
    assert device.target_tank_temperature_max == 60
    assert device.flow_temperature == 57.5
    assert device.return_temperature == 53.0
    assert device.flow_temperature_boiler == 25
    assert device.return_temperature_boiler == 25
    assert device.mixing_tank_temperature == 0
    assert device.condensing_temperature == 0
    assert device.heat_pump_frequency == 50
    assert device.boiler_status is False
    assert device.booster_heater1_status is False
    assert device.booster_heater2_status is False
    assert device.booster_heater2plus_status is False
    assert device.immersion_heater_status is False
    assert device.water_pump1_status is True
    assert device.water_pump2_status is True
    assert device.water_pump3_status is False
    assert device.water_pump4_status is False
    assert device.valve_3way_status is False
    assert device.valve_2way_status is True
    assert device.demand_percentage is None
    assert device.daily_heating_energy_consumed is None
    assert device.daily_cooling_energy_consumed is None
    assert device.daily_hot_water_energy_consumed is None
    assert device.daily_heating_energy_produced is None
    assert device.daily_cooling_energy_produced is None
    assert device.daily_hot_water_energy_produced is None
    assert device.holiday_mode is None
    assert device.wifi_signal == -73
    assert device.has_error is False
    assert device.error_code is None

    zones = device.zones
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

    await device.update()

    assert device.operation_mode == OPERATION_MODE_AUTO
    assert device.status == STATUS_HEAT_ZONES
    assert device.tank_temperature == 52.0
    assert device.target_tank_temperature == 50.0
    assert device.flow_temperature == 57.5
    assert device.return_temperature == 53.0
    assert device.flow_temperature_boiler == 25
    assert device.return_temperature_boiler == 25
    assert device.mixing_tank_temperature == 0
    assert device.condensing_temperature == 0
    assert device.heat_pump_frequency == 50
    assert device.boiler_status is False
    assert device.water_pump1_status is True
    assert device.holiday_mode is False
    assert device.wifi_signal == -73
    assert device.has_error is False
    assert device.error_code == 8000

    assert zones[0].room_temperature == 27.0
    assert zones[0].target_temperature == 30
    assert zones[0].flow_temperature == 57.5
    assert zones[0].return_temperature == 53.0
    assert zones[0].zone_flow_temperature == 25.0
    assert zones[0].zone_return_temperature == 25.0
    assert zones[0].target_flow_temperature == 60.0
    assert zones[0].operation_mode == ZONE_OPERATION_MODE_HEAT_FLOW
    assert zones[0].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
    ]
    assert zones[0].status == ZONE_STATUS_HEAT


@pytest.mark.asyncio
async def test_2zone():
    device = _build_device("atw_2zone_listdevice.json", "atw_2zone_get.json")

    assert device.name == "Home"
    assert device.device_type == DEVICE_TYPE_ATW
    assert device.temperature_increment == 0.5

    assert device.operation_mode is None
    assert device.operation_modes == [
        OPERATION_MODE_AUTO,
        OPERATION_MODE_FORCE_HOT_WATER,
    ]
    assert device.tank_temperature is None
    assert device.status is STATUS_UNKNOWN
    assert device.target_tank_temperature is None
    assert device.target_tank_temperature_min == 40
    assert device.target_tank_temperature_max == 60
    assert device.flow_temperature == 36.0
    assert device.return_temperature == 30.0
    assert device.flow_temperature_boiler == 25
    assert device.return_temperature_boiler == 25
    assert device.mixing_tank_temperature == 0
    assert device.condensing_temperature == 0
    assert device.heat_pump_frequency == 30
    assert device.boiler_status is False
    assert device.booster_heater1_status is False
    assert device.booster_heater2_status is False
    assert device.booster_heater2plus_status is False
    assert device.immersion_heater_status is False
    assert device.water_pump1_status is True
    assert device.water_pump2_status is True
    assert device.water_pump3_status is False
    assert device.water_pump4_status is False
    assert device.valve_3way_status is False
    assert device.valve_2way_status is False
    assert device.demand_percentage is None
    assert device.daily_heating_energy_consumed == 5.2
    assert device.daily_cooling_energy_consumed == 0.0
    assert device.daily_hot_water_energy_consumed == 3.1
    assert device.daily_heating_energy_produced == 18.5
    assert device.daily_cooling_energy_produced == 0.0
    assert device.daily_hot_water_energy_produced == 11.0
    assert device.holiday_mode is None
    assert device.wifi_signal == -37
    assert device.has_error is False
    assert device.error_code is None

    zones = device.zones
    assert zones is not None

    assert len(zones) == 2
    assert zones[0].name == "Downstairs"
    assert zones[0].zone_index == 1
    assert zones[0].room_temperature is None
    assert zones[0].target_temperature is None
    assert zones[0].flow_temperature == 36.0
    assert zones[0].return_temperature == 30.0
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

    assert zones[1].name == "Upstairs"
    assert zones[1].zone_index == 2
    assert zones[1].room_temperature is None
    assert zones[1].target_temperature is None
    assert zones[1].flow_temperature == 36.0
    assert zones[1].return_temperature == 30.0
    assert zones[1].zone_flow_temperature == 25.0
    assert zones[1].zone_return_temperature == 25.0
    assert zones[1].target_flow_temperature is None
    assert zones[1].operation_mode is None
    assert zones[1].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
    ]
    assert zones[1].status == ZONE_STATUS_UNKNOWN

    await device.update()

    assert device.operation_mode == OPERATION_MODE_AUTO
    assert device.status == STATUS_HEAT_ZONES
    assert device.tank_temperature == 49.5
    assert device.target_tank_temperature == 50.0
    assert device.flow_temperature == 36.0
    assert device.return_temperature == 30.0
    assert device.flow_temperature_boiler == 25
    assert device.return_temperature_boiler == 25
    assert device.mixing_tank_temperature == 0
    assert device.demand_percentage == 75
    assert device.boiler_status is False
    assert device.water_pump1_status is True
    assert device.valve_3way_status is False
    assert device.daily_heating_energy_consumed == 5.2
    assert device.daily_hot_water_energy_produced == 11.0
    assert device.holiday_mode is False
    assert device.wifi_signal == -37
    assert device.has_error is False
    assert device.error_code == 8000

    assert zones[0].room_temperature == 20.5
    assert zones[0].target_temperature == 19.5
    assert zones[0].flow_temperature == 36.0
    assert zones[0].return_temperature == 30.0
    assert zones[0].zone_flow_temperature == 25.0
    assert zones[0].zone_return_temperature == 25.0
    assert zones[0].target_flow_temperature == 25.0
    assert zones[0].operation_mode == ZONE_OPERATION_MODE_HEAT_THERMOSTAT
    assert zones[0].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
    ]
    assert zones[0].status == ZONE_STATUS_HEAT

    assert zones[1].room_temperature == 19.5
    assert zones[1].target_temperature == 18
    assert zones[1].flow_temperature == 36.0
    assert zones[1].return_temperature == 30.0
    assert zones[1].zone_flow_temperature == 25.0
    assert zones[1].zone_return_temperature == 25.0
    assert zones[1].target_flow_temperature == 25.0
    assert zones[1].operation_mode == ZONE_OPERATION_MODE_HEAT_THERMOSTAT
    assert zones[1].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
    ]
    assert zones[1].status == ZONE_STATUS_HEAT


@pytest.mark.asyncio
async def test_2zone_cancool():
    device = _build_device(
        "atw_2zone_cancool_listdevice.json", "atw_2zone_cancool_get.json"
    )

    assert device.name == "Mitsubishi"
    assert device.device_type == DEVICE_TYPE_ATW
    assert device.temperature_increment == 0.5

    assert device.operation_mode is None
    assert device.operation_modes == [
        OPERATION_MODE_AUTO,
        OPERATION_MODE_FORCE_HOT_WATER,
    ]
    assert device.tank_temperature is None
    assert device.status is STATUS_UNKNOWN
    assert device.target_tank_temperature is None
    assert device.target_tank_temperature_min == 40
    assert device.target_tank_temperature_max == 60
    assert device.flow_temperature == 50.5
    assert device.return_temperature == 50.5
    assert device.flow_temperature_boiler == 25
    assert device.return_temperature_boiler == 25
    assert device.mixing_tank_temperature is None
    assert device.condensing_temperature is None
    assert device.heat_pump_frequency == 0
    assert device.boiler_status is False
    assert device.booster_heater1_status is False
    assert device.booster_heater2_status is False
    assert device.booster_heater2plus_status is False
    assert device.immersion_heater_status is False
    assert device.water_pump1_status is True
    assert device.water_pump2_status is False
    assert device.water_pump3_status is False
    assert device.water_pump4_status is True
    assert device.valve_3way_status is True
    assert device.valve_2way_status is False
    assert device.demand_percentage is None
    assert device.daily_heating_energy_consumed is None
    assert device.daily_cooling_energy_consumed is None
    assert device.daily_hot_water_energy_consumed is None
    assert device.daily_heating_energy_produced is None
    assert device.daily_cooling_energy_produced is None
    assert device.daily_hot_water_energy_produced is None
    assert device.holiday_mode is None
    assert device.wifi_signal == -82
    assert device.has_error is False
    assert device.error_code is None

    zones = device.zones
    assert zones is not None

    assert len(zones) == 2
    assert zones[0].name == "Zone 1"
    assert zones[0].zone_index == 1
    assert zones[0].room_temperature is None
    assert zones[0].target_temperature is None
    assert zones[0].flow_temperature == 50.5
    assert zones[0].return_temperature == 50.5
    assert zones[0].zone_flow_temperature == 22.0
    assert zones[0].zone_return_temperature == 21.0
    assert zones[0].target_flow_temperature is None
    assert zones[0].operation_mode is None
    assert zones[0].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
        ZONE_OPERATION_MODE_COOL_THERMOSTAT,
        ZONE_OPERATION_MODE_COOL_FLOW,
    ]
    assert zones[0].status == ZONE_STATUS_UNKNOWN

    assert zones[1].name == "Zone 2"
    assert zones[1].zone_index == 2
    assert zones[1].room_temperature is None
    assert zones[1].target_temperature is None
    assert zones[1].flow_temperature == 50.5
    assert zones[1].return_temperature == 50.5
    assert zones[1].zone_flow_temperature == 21.0
    assert zones[1].zone_return_temperature == 21.0
    assert zones[1].target_flow_temperature is None
    assert zones[1].operation_mode is None
    assert zones[1].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
        ZONE_OPERATION_MODE_COOL_THERMOSTAT,
        ZONE_OPERATION_MODE_COOL_FLOW,
    ]
    assert zones[1].status == ZONE_STATUS_UNKNOWN

    await device.update()

    assert device.operation_mode == OPERATION_MODE_AUTO
    assert device.status == STATUS_HEAT_WATER
    assert device.tank_temperature == 47.5
    assert device.target_tank_temperature == 52.0
    assert device.flow_temperature == 50.5
    assert device.return_temperature == 50.5
    assert device.flow_temperature_boiler == 25
    assert device.return_temperature_boiler == 25
    assert device.mixing_tank_temperature is None
    assert device.condensing_temperature is None
    assert device.heat_pump_frequency == 0
    assert device.boiler_status is False
    assert device.water_pump1_status is True
    assert device.valve_3way_status is True
    assert device.holiday_mode is False
    assert device.wifi_signal == -82
    assert device.has_error is False
    assert device.error_code == 8000

    assert zones[0].room_temperature == 21.5
    assert zones[0].target_temperature == 20.5
    assert zones[0].flow_temperature == 50.5
    assert zones[0].return_temperature == 50.5
    assert zones[0].zone_flow_temperature == 22.0
    assert zones[0].zone_return_temperature == 21.0
    assert zones[0].target_flow_temperature == 5.0
    assert zones[0].operation_mode == ZONE_OPERATION_MODE_CURVE
    assert zones[0].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
        ZONE_OPERATION_MODE_COOL_THERMOSTAT,
        ZONE_OPERATION_MODE_COOL_FLOW,
    ]
    assert zones[0].status == ZONE_STATUS_IDLE

    assert zones[1].room_temperature == 21.0
    assert zones[1].target_temperature == 21.0
    assert zones[1].flow_temperature == 50.5
    assert zones[1].return_temperature == 50.5
    assert zones[1].zone_flow_temperature == 21.0
    assert zones[1].zone_return_temperature == 21.0
    assert zones[1].target_flow_temperature == 5.0
    assert zones[1].operation_mode == ZONE_OPERATION_MODE_CURVE
    assert zones[1].operation_modes == [
        ZONE_OPERATION_MODE_HEAT_THERMOSTAT,
        ZONE_OPERATION_MODE_HEAT_FLOW,
        ZONE_OPERATION_MODE_CURVE,
        ZONE_OPERATION_MODE_COOL_THERMOSTAT,
        ZONE_OPERATION_MODE_COOL_FLOW,
    ]
    assert zones[1].status == ZONE_STATUS_IDLE


@pytest.mark.asyncio
async def test_apply_write_cool_flow_property_strings():
    device = _build_device(
        "atw_2zone_cancool_listdevice.json", "atw_2zone_cancool_get.json"
    )
    await device.update()

    # New property strings
    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_1_target_cool_flow_temperature", 20.0)
    assert state["SetCoolFlowTemperatureZone1"] == 20.0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_2_target_cool_flow_temperature", 21.0)
    assert state["SetCoolFlowTemperatureZone2"] == 21.0

    # Deprecated property strings (backwards compat)
    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_1_target_heat_cool_temperature", 20.0)
    assert state["SetCoolFlowTemperatureZone1"] == 20.0

    state = {"EffectiveFlags": 0}
    device.apply_write(state, "zone_2_target_heat_cool_temperature", 21.0)
    assert state["SetCoolFlowTemperatureZone2"] == 21.0


@pytest.mark.asyncio
async def test_zone_flow_return_temperature_deprecation():
    device = _build_device("atw_1zone_listdevice.json", "atw_1zone_get.json")
    zones = device.zones
    assert zones is not None

    with pytest.deprecated_call():
        _ = zones[0].flow_temperature

    with pytest.deprecated_call():
        _ = zones[0].return_temperature
