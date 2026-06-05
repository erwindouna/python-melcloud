"""MEL API access."""

import asyncio
import socket
from datetime import UTC, datetime, timedelta
from importlib import metadata
from typing import Any, Self, cast

from aiohttp import ClientError, ClientResponseError, ClientSession, ContentTypeError
from aiohttp.hdrs import METH_GET, METH_POST
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from yarl import URL

try:
    VERSION = metadata.version(__package__ or "python-melcloud")
except metadata.PackageNotFoundError:  # pragma: no cover
    VERSION = "DEV-0.0.0"

_API_SCHEME = "https"
_API_HOST = "app.melcloud.com"
_API_BASE = "/Mitsubishi.Wifi.Client"


def _headers(token: str) -> dict[str, str]:
    return {
        "User-Agent": f"python-melcloud/{VERSION}",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-MitsContextKey": token,
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "policyaccepted=true",
    }


async def login(
    email: str,
    password: str,
    session: ClientSession | None = None,
    *,
    user_update_interval: timedelta | None = None,
    conf_update_interval: timedelta | None = None,
    device_set_debounce: timedelta | None = None,
) -> "Client":
    """Login using email and password."""
    body = {
        "Email": email,
        "Password": password,
        "Language": 0,
        "AppVersion": "1.19.1.1",
        "Persist": True,
        "CaptchaResponse": None,
    }

    if session:
        async with session.post(
            str(
                URL.build(
                    scheme=_API_SCHEME,
                    host=_API_HOST,
                    path=f"{_API_BASE}/Login/ClientLogin",
                )
            ),
            json=body,
            raise_for_status=True,
        ) as resp:
            response = await resp.json()
    else:
        async with (
            ClientSession() as _session,
            _session.post(
                str(
                    URL.build(
                        scheme=_API_SCHEME,
                        host=_API_HOST,
                        path=f"{_API_BASE}/Login/ClientLogin",
                    )
                ),
                json=body,
                raise_for_status=True,
            ) as resp,
        ):
            response = await resp.json()

    return Client(
        response.get("LoginData").get("ContextKey"),
        session,
        user_update_interval=user_update_interval,
        conf_update_interval=conf_update_interval,
        device_set_debounce=device_set_debounce,
    )


class Client:
    """MELCloud client.

    Please do not use this class directly. It is better to use the get_devices
    method exposed by the __init__.py.
    """

    def __init__(
        self,
        token: str,
        session: ClientSession | None = None,
        *,
        request_timeout: float = 10.0,
        max_retries: int = 3,
        user_update_interval: timedelta | None = None,
        conf_update_interval: timedelta | None = None,
        device_set_debounce: timedelta | None = None,
    ) -> None:
        """Initialize MELCloud client."""
        self._token = token
        self._request_timeout = request_timeout
        self._max_retries = max_retries

        if session:
            self._session = session
            self._managed_session = False
        else:
            self._session = ClientSession()
            self._managed_session = True

        self._user_update_interval = user_update_interval or timedelta(minutes=5)
        self._conf_update_interval = conf_update_interval or timedelta(seconds=59)
        self._device_set_debounce = device_set_debounce or timedelta(seconds=1)

        self._last_user_update: datetime | None = None
        self._last_conf_update: datetime | None = None
        self._device_confs: list[dict[str, Any]] = []
        self._account: dict[str, Any] | None = None

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Perform an authenticated request against the MEL API."""
        url = URL.build(
            scheme=_API_SCHEME,
            host=_API_HOST,
            path=f"{_API_BASE}/{uri}",
        )

        async for attempt in AsyncRetrying(
            retry=retry_if_exception_type((ClientError, socket.gaierror)),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            stop=stop_after_attempt(self._max_retries + 1),
            reraise=True,
        ):
            with attempt:
                try:
                    async with asyncio.timeout(self._request_timeout):
                        async with self._session.request(
                            method,
                            url,
                            headers=_headers(self._token),
                            json=json_body,
                            params=params,
                            raise_for_status=True,
                        ) as resp:
                            try:
                                data = await resp.json()
                            except ContentTypeError:
                                return None
                            return data
                except ClientResponseError as err:
                    if err.status == 403:
                        return None
                    raise

        return None  # pragma: no cover

    @property
    def token(self) -> str:
        """Return currently used token."""
        return self._token

    @property
    def device_confs(self) -> list[dict[Any, Any]]:
        """Return device configurations."""
        return self._device_confs

    @property
    def account(self) -> dict[Any, Any] | None:
        """Return account."""
        return self._account

    async def _fetch_user_details(self) -> None:
        """Fetch user details."""
        self._account = await self._request("User/GetUserDetails")

    async def _fetch_device_confs(self) -> None:
        """Fetch all configured devices."""
        entries = await self._request("User/ListDevices")
        if not entries:
            return

        new_devices: list[dict[str, Any]] = []
        for entry in entries:
            new_devices = new_devices + entry["Structure"]["Devices"]

            for area in entry["Structure"]["Areas"]:
                new_devices = new_devices + area["Devices"]

            for floor in entry["Structure"]["Floors"]:
                new_devices = new_devices + floor["Devices"]

                for area in floor["Areas"]:
                    new_devices = new_devices + area["Devices"]

        visited: set[int] = set()
        self._device_confs = [
            d
            for d in new_devices
            if d["DeviceID"] not in visited and not visited.add(d["DeviceID"])  # type: ignore[func-returns-value]
        ]

    async def update_confs(self) -> None:
        """Update device_confs and account.

        Calls are rate limited to allow Device instances to freely poll their own
        state while refreshing the device_confs list and account.
        """
        now = datetime.now(UTC)

        if (
            self._last_conf_update is None
            or now - self._last_conf_update > self._conf_update_interval
        ):
            await self._fetch_device_confs()
            self._last_conf_update = now

        if (
            self._last_user_update is None
            or now - self._last_user_update > self._user_update_interval
        ):
            await self._fetch_user_details()
            self._last_user_update = now

    async def fetch_device_units(self, device: Any) -> list[dict[Any, Any]] | None:
        """Fetch unit information for a device.

        User provided info such as indoor/outdoor unit model names and serial numbers.
        Returns None for guest-level users (403 response).
        """
        return cast(
            "list[dict[Any, Any]] | None",
            await self._request(
                "Device/ListDeviceUnits",
                method=METH_POST,
                json_body={"deviceId": device.device_id},
            ),
        )

    async def fetch_device_state(self, device: Any) -> dict[Any, Any] | None:
        """Fetch state information of a device.

        This method should not be called more than once a minute. Rate
        limiting is left to the caller.
        """
        return cast(
            "dict[Any, Any] | None",
            await self._request(
                "Device/Get",
                params={"id": device.device_id, "buildingID": device.building_id},
            ),
        )

    async def fetch_energy_report(self, device: Any) -> dict[Any, Any] | None:
        """Fetch energy report containing today and 1-2 days from the past.

        Returns None for guest-level users (403 response).
        """
        from_str = (datetime.now(tz=UTC) - timedelta(days=2)).strftime("%Y-%m-%d")
        to_str = (datetime.now(tz=UTC) + timedelta(days=2)).strftime("%Y-%m-%d")

        return cast(
            "dict[Any, Any] | None",
            await self._request(
                "EnergyCost/Report",
                method=METH_POST,
                json_body={
                    "DeviceId": device.device_id,
                    "UseCurrency": False,
                    "FromDate": f"{from_str}T00:00:00",
                    "ToDate": f"{to_str}T00:00:00",
                },
            ),
        )

    async def set_device_state(self, device: dict[str, Any]) -> dict[str, Any] | None:
        """Update device state.

        Device is responsible for updating the state and managing EffectiveFlags.
        """
        device_type = device.get("DeviceType")
        if device_type == 0:
            setter = "SetAta"
        elif device_type == 1:
            setter = "SetAtw"
        elif device_type == 3:
            setter = "SetErv"
        else:
            raise ValueError(f"Unsupported device type [{device_type}]")

        return cast(
            "dict[str, Any] | None",
            await self._request(
                f"Device/{setter}",
                method=METH_POST,
                json_body=device,
            ),
        )

    async def close(self) -> None:
        """Close open client session."""
        if self._managed_session and self._session:
            await self._session.close()

    async def __aenter__(self) -> Self:
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit."""
        await self.close()
