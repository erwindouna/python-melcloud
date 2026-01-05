"""Client tests."""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from aiohttp import ClientResponseError, ClientSession
from pymelcloud.client import Client


@pytest.mark.asyncio
async def test_fetch_energy_report_ignores_403():
    session = Mock(spec=ClientSession)
    cm = AsyncMock()
    session.post.return_value = cm

    resp = Mock()
    cm.__aenter__.return_value = resp

    request_info = Mock()
    request_info.real_url = "https://example.test/EnergyCost/Report"

    resp.raise_for_status.side_effect = ClientResponseError(
        request_info=request_info,
        history=(),
        status=403,
        message="Forbidden",
    )

    client = Client(token="dummy", session=session)

    class DummyDevice:
        device_id = 123

    device = DummyDevice()
    result = await client.fetch_energy_report(device)
    assert result is None


@pytest.mark.asyncio
async def test_fetch_device_units_ignores_403():
    session = Mock(spec=ClientSession)
    cm = AsyncMock()
    session.post.return_value = cm

    resp = Mock()
    cm.__aenter__.return_value = resp

    request_info = Mock()
    request_info.real_url = "https://example.test/Device/ListDeviceUnits"

    resp.raise_for_status.side_effect = ClientResponseError(
        request_info=request_info,
        history=(),
        status=403,
        message="Forbidden",
    )

    client = Client(token="dummy", session=session)

    class DummyDevice:
        device_id = 123

    device = DummyDevice()
    result = await client.fetch_device_units(device)
    assert result is None
