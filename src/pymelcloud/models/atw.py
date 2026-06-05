"""Typed model for Air-To-Water (DeviceType=1) device state."""

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class AtwDeviceState(DataClassORJSONMixin):
    """Represents the state of an Air-to-Water device returned by the MELCloud API."""

    device_id: int = field(metadata=field_options(alias="DeviceID"))

    temperature_increment: float | None = field(
        default=None, metadata=field_options(alias="TemperatureIncrement")
    )
    defrost_mode: int | None = field(
        default=None, metadata=field_options(alias="DefrostMode")
    )
    heat_pump_frequency: int | None = field(
        default=None, metadata=field_options(alias="HeatPumpFrequency")
    )
    room_temperature_zone1: float | None = field(
        default=None, metadata=field_options(alias="RoomTemperatureZone1")
    )
    room_temperature_zone2: float | None = field(
        default=None, metadata=field_options(alias="RoomTemperatureZone2")
    )
    tank_water_temperature: float | None = field(
        default=None, metadata=field_options(alias="TankWaterTemperature")
    )
    unit_status: int | None = field(
        default=None, metadata=field_options(alias="UnitStatus")
    )
    mixing_tank_water_temperature: float | None = field(
        default=None, metadata=field_options(alias="MixingTankWaterTemperature")
    )
    condensing_temperature: float | None = field(
        default=None, metadata=field_options(alias="CondensingTemperature")
    )
    effective_flags: int = field(
        default=0, metadata=field_options(alias="EffectiveFlags")
    )
    last_effective_flags: int = field(
        default=0, metadata=field_options(alias="LastEffectiveFlags")
    )
    power: bool = field(default=False, metadata=field_options(alias="Power"))
    eco_hot_water: bool = field(
        default=False, metadata=field_options(alias="EcoHotWater")
    )
    operation_mode: int | None = field(
        default=None, metadata=field_options(alias="OperationMode")
    )
    operation_mode_zone1: int | None = field(
        default=None, metadata=field_options(alias="OperationModeZone1")
    )
    operation_mode_zone2: int | None = field(
        default=None, metadata=field_options(alias="OperationModeZone2")
    )
    set_temperature_zone1: float | None = field(
        default=None, metadata=field_options(alias="SetTemperatureZone1")
    )
    set_temperature_zone2: float | None = field(
        default=None, metadata=field_options(alias="SetTemperatureZone2")
    )
    set_tank_water_temperature: float | None = field(
        default=None, metadata=field_options(alias="SetTankWaterTemperature")
    )
    target_hc_temperature_zone1: float | None = field(
        default=None, metadata=field_options(alias="TargetHCTemperatureZone1")
    )
    target_hc_temperature_zone2: float | None = field(
        default=None, metadata=field_options(alias="TargetHCTemperatureZone2")
    )
    forced_hot_water_mode: bool = field(
        default=False, metadata=field_options(alias="ForcedHotWaterMode")
    )
    holiday_mode: bool = field(
        default=False, metadata=field_options(alias="HolidayMode")
    )
    prohibit_hot_water: bool = field(
        default=False, metadata=field_options(alias="ProhibitHotWater")
    )
    prohibit_heating_zone1: bool = field(
        default=False, metadata=field_options(alias="ProhibitHeatingZone1")
    )
    prohibit_heating_zone2: bool = field(
        default=False, metadata=field_options(alias="ProhibitHeatingZone2")
    )
    prohibit_cooling_zone1: bool = field(
        default=False, metadata=field_options(alias="ProhibitCoolingZone1")
    )
    prohibit_cooling_zone2: bool = field(
        default=False, metadata=field_options(alias="ProhibitCoolingZone2")
    )
    set_heat_flow_temperature_zone1: float | None = field(
        default=None, metadata=field_options(alias="SetHeatFlowTemperatureZone1")
    )
    set_heat_flow_temperature_zone2: float | None = field(
        default=None, metadata=field_options(alias="SetHeatFlowTemperatureZone2")
    )
    set_cool_flow_temperature_zone1: float | None = field(
        default=None, metadata=field_options(alias="SetCoolFlowTemperatureZone1")
    )
    set_cool_flow_temperature_zone2: float | None = field(
        default=None, metadata=field_options(alias="SetCoolFlowTemperatureZone2")
    )
    outdoor_temperature: float | None = field(
        default=None, metadata=field_options(alias="OutdoorTemperature")
    )
    demand_percentage: int | None = field(
        default=None, metadata=field_options(alias="DemandPercentage")
    )
    idle_zone1: bool = field(default=False, metadata=field_options(alias="IdleZone1"))
    idle_zone2: bool = field(default=False, metadata=field_options(alias="IdleZone2"))
    has_zone2: bool = field(default=False, metadata=field_options(alias="HasZone2"))
    daily_energy_consumed_date: str | None = field(
        default=None, metadata=field_options(alias="DailyEnergyConsumedDate")
    )
    daily_energy_produced_date: str | None = field(
        default=None, metadata=field_options(alias="DailyEnergyProducedDate")
    )
    current_energy_consumed: float | None = field(
        default=None, metadata=field_options(alias="CurrentEnergyConsumed")
    )
    current_energy_produced: float | None = field(
        default=None, metadata=field_options(alias="CurrentEnergyProduced")
    )
    error_code: int | None = field(
        default=None, metadata=field_options(alias="ErrorCode")
    )
    has_error: bool = field(default=False, metadata=field_options(alias="HasError"))
    offline: bool = field(default=False, metadata=field_options(alias="Offline"))
    wifi_signal_strength: int | None = field(
        default=None, metadata=field_options(alias="WifiSignalStrength")
    )
    last_communication: str | None = field(
        default=None, metadata=field_options(alias="LastCommunication")
    )
    has_pending_command: bool = field(
        default=False, metadata=field_options(alias="HasPendingCommand")
    )
    units: list[Any] | None = field(default=None, metadata=field_options(alias="Units"))
    # Fields not in all ATW models — included as optional
    max_set_temperature: float | None = field(
        default=None, metadata=field_options(alias="MaxSetTemperature")
    )
    min_set_temperature: float | None = field(
        default=None, metadata=field_options(alias="MinSetTemperature")
    )
    mac_address: str | None = field(
        default=None, metadata=field_options(alias="MacAddress")
    )
    serial_number: str | None = field(
        default=None, metadata=field_options(alias="SerialNumber")
    )
