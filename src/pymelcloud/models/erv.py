"""Typed model for Energy-Recovery-Ventilation (DeviceType=3) device state."""

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class ErvDeviceState(DataClassORJSONMixin):
    """Represents the state of an ERV device as returned by the MELCloud API."""

    device_id: int = field(metadata=field_options(alias="DeviceID"))
    device_type: int = field(metadata=field_options(alias="DeviceType"))

    effective_flags: int = field(
        default=0, metadata=field_options(alias="EffectiveFlags")
    )
    local_ip_address: str | None = field(
        default=None, metadata=field_options(alias="LocalIPAddress")
    )
    room_temperature: float | None = field(
        default=None, metadata=field_options(alias="RoomTemperature")
    )
    supply_temperature: float | None = field(
        default=None, metadata=field_options(alias="SupplyTemperature")
    )
    outdoor_temperature: float | None = field(
        default=None, metadata=field_options(alias="OutdoorTemperature")
    )
    room_co2_level: float | None = field(
        default=None, metadata=field_options(alias="RoomCO2Level")
    )
    night_purge_mode: bool = field(
        default=False, metadata=field_options(alias="NightPurgeMode")
    )
    core_maintenance_required: bool = field(
        default=False, metadata=field_options(alias="CoreMaintenanceRequired")
    )
    filter_maintenance_required: bool = field(
        default=False, metadata=field_options(alias="FilterMaintenanceRequired")
    )
    set_temperature: float | None = field(
        default=None, metadata=field_options(alias="SetTemperature")
    )
    set_fan_speed: int | None = field(
        default=None, metadata=field_options(alias="SetFanSpeed")
    )
    operation_mode: int | None = field(
        default=None, metadata=field_options(alias="OperationMode")
    )
    ventilation_mode: int | None = field(
        default=None, metadata=field_options(alias="VentilationMode")
    )
    name: str | None = field(default=None, metadata=field_options(alias="Name"))
    number_of_fan_speeds: int | None = field(
        default=None, metadata=field_options(alias="NumberOfFanSpeeds")
    )
    weather_observations: list[Any] = field(
        default_factory=list, metadata=field_options(alias="WeatherObservations")
    )
    error_message: str | None = field(
        default=None, metadata=field_options(alias="ErrorMessage")
    )
    error_code: int | None = field(
        default=None, metadata=field_options(alias="ErrorCode")
    )
    default_heating_set_temperature: float | None = field(
        default=None, metadata=field_options(alias="DefaultHeatingSetTemperature")
    )
    default_cooling_set_temperature: float | None = field(
        default=None, metadata=field_options(alias="DefaultCoolingSetTemperature")
    )
    temperature_increment_override: int | None = field(
        default=None, metadata=field_options(alias="TemperatureIncrementOverride")
    )
    hide_room_temperature: bool = field(
        default=False, metadata=field_options(alias="HideRoomTemperature")
    )
    hide_supply_temperature: bool = field(
        default=False, metadata=field_options(alias="HideSupplyTemperature")
    )
    hide_outdoor_temperature: bool = field(
        default=False, metadata=field_options(alias="HideOutdoorTemperature")
    )
    last_communication: str | None = field(
        default=None, metadata=field_options(alias="LastCommunication")
    )
    next_communication: str | None = field(
        default=None, metadata=field_options(alias="NextCommunication")
    )
    power: bool = field(default=False, metadata=field_options(alias="Power"))
    has_pending_command: bool = field(
        default=False, metadata=field_options(alias="HasPendingCommand")
    )
    offline: bool = field(default=False, metadata=field_options(alias="Offline"))
    scene: Any | None = field(default=None, metadata=field_options(alias="Scene"))
    scene_owner: Any | None = field(
        default=None, metadata=field_options(alias="SceneOwner")
    )
    has_co2_sensor: bool = field(
        default=False, metadata=field_options(alias="HasCO2Sensor")
    )
    has_error: bool = field(default=False, metadata=field_options(alias="HasError"))
