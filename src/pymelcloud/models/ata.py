"""Typed model for Air-To-Air (DeviceType=0) device state."""

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class AtaDeviceState(DataClassORJSONMixin):
    """Represents the state of an Air-to-Air device as returned by the MELCloud API."""

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
    set_temperature: float | None = field(
        default=None, metadata=field_options(alias="SetTemperature")
    )
    set_fan_speed: int | None = field(
        default=None, metadata=field_options(alias="SetFanSpeed")
    )
    operation_mode: int | None = field(
        default=None, metadata=field_options(alias="OperationMode")
    )
    vane_horizontal: int | None = field(
        default=None, metadata=field_options(alias="VaneHorizontal")
    )
    vane_vertical: int | None = field(
        default=None, metadata=field_options(alias="VaneVertical")
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
    hide_vane_controls: bool = field(
        default=False, metadata=field_options(alias="HideVaneControls")
    )
    hide_dry_mode_control: bool = field(
        default=False, metadata=field_options(alias="HideDryModeControl")
    )
    room_temperature_label: int | None = field(
        default=None, metadata=field_options(alias="RoomTemperatureLabel")
    )
    in_standby_mode: bool = field(
        default=False, metadata=field_options(alias="InStandbyMode")
    )
    temperature_increment_override: int | None = field(
        default=None, metadata=field_options(alias="TemperatureIncrementOverride")
    )
    prohibit_set_temperature: bool = field(
        default=False, metadata=field_options(alias="ProhibitSetTemperature")
    )
    prohibit_operation_mode: bool = field(
        default=False, metadata=field_options(alias="ProhibitOperationMode")
    )
    prohibit_power: bool = field(
        default=False, metadata=field_options(alias="ProhibitPower")
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
    has_error: bool = field(default=False, metadata=field_options(alias="HasError"))
