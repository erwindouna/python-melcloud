"""Test utilities for MELCloud device testing."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, Mock, patch


def build_device(
    device_conf_name: str,
    device_state_name: str,
    energy_report: dict[Any, Any] | None = None,
) -> Any:
    """Build a test device with mocked client and data from JSON files."""
    test_dir = Path(__file__).parent / "samples"
    device_conf_path = test_dir / device_conf_name
    with device_conf_path.open() as json_file:
        device_conf = json.load(json_file)

    device_state_path = test_dir / device_state_name
    with device_state_path.open() as json_file:
        device_state = json.load(json_file)

    with patch(
        "src.pymelcloud.client.Client"
    ) as _client:  # Ensure the patch path reflects the new location
        _client.update_confs = AsyncMock()
        _client.device_confs.__iter__ = Mock(return_value=[device_conf].__iter__())
        _client.fetch_device_units = AsyncMock(return_value=[])
        _client.fetch_device_state = AsyncMock(return_value=device_state)
        _client.fetch_energy_report = AsyncMock(return_value=energy_report)
        client = _client

    return device_conf, client
