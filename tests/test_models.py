"""Tests for mashumaro device state models."""

import json

from syrupy.assertion import SnapshotAssertion

from pymelcloud.models import AtaDeviceState, AtwDeviceState, ErvDeviceState
from tests import load_fixture


def test_ata_device_state_from_dict() -> None:
    """Test AtaDeviceState can be parsed from ATA get fixture."""
    data = json.loads(load_fixture("ata_get.json"))
    model = AtaDeviceState.from_dict(data)

    assert model is not None
    assert model.room_temperature == 28.0
    assert model.set_temperature == 22.0
    assert model.power is False
    assert model.has_error is False
    assert model.error_code == 8000
    assert model.operation_mode == 3
    assert model.set_fan_speed == 3
    assert model.vane_horizontal == 3
    assert model.vane_vertical == 0


def test_ata_device_state_snapshot(snapshot: SnapshotAssertion) -> None:
    """Snapshot test for AtaDeviceState parsed from fixture."""
    assert (
        AtaDeviceState.from_dict(json.loads(load_fixture("ata_get.json"))) == snapshot
    )


def test_atw_device_state_from_dict() -> None:
    """Test AtwDeviceState can be parsed from ATW 1-zone get fixture."""
    data = json.loads(load_fixture("atw_1zone_get.json"))
    model = AtwDeviceState.from_dict(data)

    assert model is not None
    assert model.tank_water_temperature == 52.0
    assert model.set_tank_water_temperature == 50.0
    assert model.has_error is False


def test_atw_device_state_snapshot(snapshot: SnapshotAssertion) -> None:
    """Snapshot test for AtwDeviceState parsed from fixture."""
    assert (
        AtwDeviceState.from_dict(json.loads(load_fixture("atw_1zone_get.json")))
        == snapshot
    )


def test_erv_device_state_from_dict() -> None:
    """Test ErvDeviceState can be parsed from ERV get fixture."""
    data = json.loads(load_fixture("erv_get.json"))
    model = ErvDeviceState.from_dict(data)

    assert model is not None
    assert model.room_temperature == 29.0
    assert model.outdoor_temperature == 28.0
    assert model.has_error is False


def test_erv_device_state_snapshot(snapshot: SnapshotAssertion) -> None:
    """Snapshot test for ErvDeviceState parsed from fixture."""
    assert (
        ErvDeviceState.from_dict(json.loads(load_fixture("erv_get.json"))) == snapshot
    )
