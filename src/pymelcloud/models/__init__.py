"""Typed models for MELCloud API responses."""

from pymelcloud.models.ata import AtaDeviceState
from pymelcloud.models.atw import AtwDeviceState
from pymelcloud.models.erv import ErvDeviceState

__all__ = [
    "AtaDeviceState",
    "AtwDeviceState",
    "ErvDeviceState",
]
