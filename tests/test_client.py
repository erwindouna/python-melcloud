"""Client tests."""

import json

import pytest
from aiohttp import ClientSession
from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from pymelcloud import login as public_login
from pymelcloud.client import Client
from tests import load_fixture


@pytest.mark.asyncio
async def test_fetch_energy_report_ignores_403(
    aresponses: ResponsesMockServer,
    melcloud_client: Client,
) -> None:
    """Test that a 403 response on energy report returns None."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/EnergyCost/Report",
        "POST",
        aresponses.Response(status=403),
    )

    class DummyDevice:
        device_id = 123

    result = await melcloud_client.fetch_energy_report(DummyDevice())
    assert result is None


@pytest.mark.asyncio
async def test_fetch_device_units_ignores_403(
    aresponses: ResponsesMockServer,
    melcloud_client: Client,
) -> None:
    """Test that a 403 response on device units returns None."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Device/ListDeviceUnits",
        "POST",
        aresponses.Response(status=403),
    )

    class DummyDevice:
        device_id = 123

    result = await melcloud_client.fetch_device_units(DummyDevice())
    assert result is None


@pytest.mark.asyncio
async def test_fetch_device_state(
    aresponses: ResponsesMockServer,
    melcloud_client: Client,
    snapshot: SnapshotAssertion,
) -> None:
    """Test that device state is fetched and returned correctly."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Device/Get",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("ata_get.json"),
        ),
    )

    class DummyDevice:
        device_id = 222222
        building_id = 111111

    result = await melcloud_client.fetch_device_state(DummyDevice())
    assert result is not None
    assert result == snapshot


@pytest.mark.asyncio
async def test_login_returns_token(aresponses: ResponsesMockServer) -> None:
    """Test that login() returns the token from the API."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Login/ClientLogin",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("login_response.json"),
        ),
    )

    async with ClientSession() as session:
        token = await public_login("test@example.com", "password", session)

    assert token == "test-context-key-12345"


@pytest.mark.asyncio
async def test_login_without_session(aresponses: ResponsesMockServer) -> None:
    """Test that login() works without a pre-existing session."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Login/ClientLogin",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("login_response.json"),
        ),
    )

    token = await public_login("test@example.com", "password")
    assert token == "test-context-key-12345"


@pytest.mark.asyncio
async def test_update_confs(
    aresponses: ResponsesMockServer,
    melcloud_client: Client,
) -> None:
    """Test that update_confs fetches device list and user details."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/User/ListDevices",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("list_devices.json"),
        ),
    )
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/User/GetUserDetails",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("user_details.json"),
        ),
    )

    await melcloud_client.update_confs()

    assert len(melcloud_client.device_confs) == 1
    assert melcloud_client.device_confs[0]["DeviceID"] == 0
    assert melcloud_client.account is not None
    assert melcloud_client.account["UseFahrenheit"] is False


@pytest.mark.asyncio
async def test_update_confs_is_rate_limited(
    aresponses: ResponsesMockServer,
    melcloud_client: Client,
) -> None:
    """Test that update_confs does not re-fetch before the interval expires."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/User/ListDevices",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("list_devices.json"),
        ),
    )
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/User/GetUserDetails",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("user_details.json"),
        ),
    )

    await melcloud_client.update_confs()
    # Second call within rate-limit window should NOT make new HTTP requests.
    # If it did, aresponses would raise because there are no more mocked responses.
    await melcloud_client.update_confs()

    assert melcloud_client._last_conf_update is not None


@pytest.mark.asyncio
async def test_set_device_state_ata(
    aresponses: ResponsesMockServer,
    melcloud_client: Client,
) -> None:
    """Test that set_device_state posts to the correct endpoint for ATA devices."""
    expected_response = json.loads(load_fixture("ata_get.json"))
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Device/SetAta",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("ata_get.json"),
        ),
    )

    state = {"DeviceType": 0, "EffectiveFlags": 4, "SetTemperature": 24.0}
    result = await melcloud_client.set_device_state(state)
    assert result is not None
    assert result["DeviceType"] == expected_response["DeviceType"]


@pytest.mark.asyncio
async def test_set_device_state_atw(
    aresponses: ResponsesMockServer,
    melcloud_client: Client,
) -> None:
    """Test that set_device_state posts to the correct endpoint for ATW devices."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Device/SetAtw",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("atw_1zone_get.json"),
        ),
    )

    state = {"DeviceType": 1, "EffectiveFlags": 0x10000}
    result = await melcloud_client.set_device_state(state)
    assert result is not None


@pytest.mark.asyncio
async def test_set_device_state_erv(
    aresponses: ResponsesMockServer,
    melcloud_client: Client,
) -> None:
    """Test that set_device_state posts to the correct endpoint for ERV devices."""
    aresponses.add(
        "app.melcloud.com",
        "/Mitsubishi.Wifi.Client/Device/SetErv",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("erv_get.json"),
        ),
    )

    state = {"DeviceType": 3, "EffectiveFlags": 0}
    result = await melcloud_client.set_device_state(state)
    assert result is not None


@pytest.mark.asyncio
async def test_set_device_state_unsupported_type(
    melcloud_client: Client,
) -> None:
    """Test that set_device_state raises ValueError for unknown device types."""
    with pytest.raises(ValueError, match="Unsupported device type"):
        await melcloud_client.set_device_state({"DeviceType": 99})


@pytest.mark.asyncio
async def test_client_context_manager() -> None:
    """Test that Client works as an async context manager."""
    async with Client(token="test_token") as client:
        assert client.token == "test_token"


@pytest.mark.asyncio
async def test_client_close_managed_session() -> None:
    """Test that close() closes a managed session."""
    client = Client(token="test_token")
    await client.close()


@pytest.mark.asyncio
async def test_client_close_unmanaged_session() -> None:
    """Test that close() does not close an externally provided session."""
    async with ClientSession() as session:
        client = Client(token="test_token", session=session)
        await client.close()
        assert not session.closed
