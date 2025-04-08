""" "Conftest for the tests package."""

from collections.abc import AsyncGenerator, Generator

import aiohttp
import pytest
from aioresponses import aioresponses
from syrupy import SnapshotAssertion

import pymelcloud
from pymelcloud.client import BASE_URL, Client
from tests import load_fixture
from tests.syrupy import MELCloudSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the MELCloud extension."""
    return snapshot.use_extension(MELCloudSnapshotExtension)


@pytest.fixture(name="melcloud_client")
async def client() -> AsyncGenerator[Client, None]:
    """Return a MELCloud client."""
    async with aiohttp.ClientSession() as session:
        token = await pymelcloud.login(
            email="username",
            password="password",
            session=session,
        )
        yield Client(token, session)


@pytest.fixture(autouse=True)
def _melcloud_oauth(responses: aioresponses) -> None:
    """Mock the Tado token URL."""
    responses.post(
        f"{BASE_URL}/Login/ClientLogin", status=200, body=load_fixture("login.json")
    )


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
