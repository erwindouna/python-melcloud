"""Test utilities for pymelcloud."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, Mock, patch


def build_device(
    device_conf_name: str,
    device_state_name: str,
    energy_report: dict[Any, Any] | None = None,
) -> tuple[dict[str, Any], Mock]:
    """Build a device mock for testing."""
    test_dir = Path(__file__).parent / "samples"
    with (test_dir / device_conf_name).open() as json_file:
        device_conf = json.load(json_file)

    with (test_dir / device_state_name).open() as json_file:
        device_state = json.load(json_file)

    with patch("src.pymelcloud.client.Client") as _client:
        _client.update_confs = AsyncMock()
        _client.device_confs.__iter__ = Mock(return_value=[device_conf].__iter__())
        _client.fetch_device_units = AsyncMock(return_value=[])
        _client.fetch_device_state = AsyncMock(return_value=device_state)
        _client.fetch_energy_report = AsyncMock(return_value=energy_report)
        client = _client

    return device_conf, client
