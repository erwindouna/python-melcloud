"""Tests for the client module."""

from __future__ import annotations

import aiohttp
import pytest
from aioresponses import aioresponses
from syrupy import SnapshotAssertion

import pymelcloud
from pymelcloud.client import BASE_URL, Client
from tests import load_fixture


async def test_create_session(responses: aioresponses) -> None:
    """Test creating a session."""
    responses.post(
        f"{BASE_URL}/Login/ClientLogin", status=200, body=load_fixture("login.json")
    )
    async with aiohttp.ClientSession():
        token = await pymelcloud.login(email="username", password="password")
        assert token is not None

    # Test creating a session with a custom session
    responses.post(
        f"{BASE_URL}/Login/ClientLogin", status=200, body=load_fixture("login.json")
    )
    async with aiohttp.ClientSession():
        token = await pymelcloud.login(
            email="username", password="password", session=aiohttp.ClientSession()
        )
        assert token is not None


async def test_login_success(
    responses: aioresponses, snapshot: SnapshotAssertion
) -> None:
    """Test logging in with valid credentials."""
    responses.post(
        f"{BASE_URL}/Login/ClientLogin", status=200, body=load_fixture("login.json")
    )
    async with aiohttp.ClientSession() as session:
        client = await pymelcloud.client.login(
            email="username", password="password", session=session
        )

        # pylint: disable=protected-access
        assert client is not None
        assert isinstance(client, Client)
        assert client.token == "0-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        assert client._session == session
        assert client._managed_session is False
        assert client == snapshot


@pytest.mark.skip(
    reason="Skipping, can be implemented later when exceptions are in place."
)
async def test_login_failure(responses: aioresponses) -> None:
    """Test logging in with invalid credentials."""
    responses.post(
        f"{BASE_URL}/Login/ClientLogin",
        status=200,
        body=load_fixture("login_failure.json"),
    )
    async with aiohttp.ClientSession() as session:
        with pytest.raises(aiohttp.ClientResponseError):
            await pymelcloud.client.login(
                email="username", password="password", session=session
            )


async def test_update_confs(
    melcloud_client: Client, responses: aioresponses, snapshot: SnapshotAssertion
) -> None:
    """Test updating device configurations."""
    responses.get(
        f"{BASE_URL}/User/ListDevices",
        status=200,
        body=load_fixture("list_devices.json"),
    )
    responses.get(
        f"{BASE_URL}/User/GetUserDetails",
        status=200,
        body=load_fixture("user_details.json"),
    )

    # pylint: disable=protected-access
    await melcloud_client.update_confs()
    assert melcloud_client._device_confs == snapshot
    assert melcloud_client._account == snapshot
