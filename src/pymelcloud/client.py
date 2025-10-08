"""MEL API access."""

from datetime import UTC, datetime, timedelta
from typing import Any

from aiohttp import ClientSession

BASE_URL = "https://app.melcloud.com/Mitsubishi.Wifi.Client"


def _headers(token: str) -> dict[str, str]:
    return {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) "
        "Gecko/20100101 Firefox/73.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-MitsContextKey": token,
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "policyaccepted=true",
    }


async def _do_login(
    _session: ClientSession, email: str, password: str
) -> dict[str, Any]:
    body = {
        "Email": email,
        "Password": password,
        "Language": 0,
        "AppVersion": "1.19.1.1",
        "Persist": True,
        "CaptchaResponse": None,
    }

    async with _session.post(
        f"{BASE_URL}/Login/ClientLogin", json=body, raise_for_status=True
    ) as resp:
        result: dict[str, Any] = await resp.json()
        return result


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
    if session:
        response = await _do_login(session, email, password)
    else:
        async with ClientSession() as _session:
            response = await _do_login(_session, email, password)

    login_data = response.get("LoginData")
    if login_data is None:
        raise ValueError("No login data in response")

    context_key = login_data.get("ContextKey")
    if context_key is None:
        raise ValueError("No context key in login data")

    return Client(
        context_key,
        session,
        user_update_interval=user_update_interval or timedelta(minutes=5),
        conf_update_interval=conf_update_interval or timedelta(seconds=59),
        device_set_debounce=device_set_debounce or timedelta(seconds=1),
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
        user_update_interval: timedelta = timedelta(minutes=5),
        conf_update_interval: timedelta = timedelta(seconds=59),
        device_set_debounce: timedelta = timedelta(seconds=1),
    ) -> None:
        """Initialize MELCloud client."""
        self._token = token
        if session:
            self._session = session
            self._managed_session = False
        else:
            self._session = ClientSession()
            self._managed_session = True
        self._user_update_interval = user_update_interval
        self._conf_update_interval = conf_update_interval
        self._device_set_debounce = device_set_debounce

        self._last_user_update: datetime | None = None
        self._last_conf_update: datetime | None = None
        self._device_confs: list[dict[str, Any]] = []
        self._account: dict[str, Any] | None = None

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
        async with self._session.get(
            f"{BASE_URL}/User/GetUserDetails",
            headers=_headers(self._token),
            raise_for_status=True,
        ) as resp:
            self._account = await resp.json()

    async def _fetch_device_confs(self) -> None:
        """Fetch all configured devices."""
        url = f"{BASE_URL}/User/ListDevices"
        async with self._session.get(
            url, headers=_headers(self._token), raise_for_status=True
        ) as resp:
            entries = await resp.json()
            new_devices: list[dict[str, Any]] = []
            for entry in entries:
                new_devices = new_devices + entry["Structure"]["Devices"]

                for area in entry["Structure"]["Areas"]:
                    new_devices = new_devices + area["Devices"]

                for floor in entry["Structure"]["Floors"]:
                    new_devices = new_devices + floor["Devices"]

                    for area in floor["Areas"]:
                        new_devices = new_devices + area["Devices"]

            visited: set[Any] = set()
            filtered_devices = []
            for d in new_devices:
                device_id = d["DeviceID"]
                if device_id not in visited:
                    visited.add(device_id)
                    filtered_devices.append(d)
            self._device_confs = filtered_devices

    async def update_confs(self) -> None:
        """Update device_confs and account.

        Calls are rate limited to allow Device instances to freely poll their own
        state while refreshing the device_confs list and account.
        """
        now = datetime.now(tz=UTC)

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

    async def fetch_device_units(self, device: Any) -> dict[Any, Any] | None:
        """Fetch unit information for a device.

        User provided info such as indoor/outdoor unit model names and
        serial numbers.
        """
        async with self._session.post(
            f"{BASE_URL}/Device/ListDeviceUnits",
            headers=_headers(self._token),
            json={"deviceId": device.device_id},
            raise_for_status=True,
        ) as resp:
            result: dict[Any, Any] = await resp.json()
            return result

    async def fetch_device_state(self, device: Any) -> dict[Any, Any] | None:
        """Fetch state information of a device.

        This method should not be called more than once a minute. Rate
        limiting is left to the caller.
        """
        device_id = device.device_id
        building_id = device.building_id
        async with self._session.get(
            f"{BASE_URL}/Device/Get?id={device_id}&buildingID={building_id}",
            headers=_headers(self._token),
            raise_for_status=True,
        ) as resp:
            result: dict[Any, Any] = await resp.json()
            return result

    async def fetch_energy_report(self, device: Any) -> dict[Any, Any] | None:
        """Fetch energy report containing today and 1-2 days from the past."""
        device_id = device.device_id
        now = datetime.now(tz=UTC)
        from_str = (now - timedelta(days=2)).strftime("%Y-%m-%d")
        to_str = (now + timedelta(days=2)).strftime("%Y-%m-%d")

        async with self._session.post(
            f"{BASE_URL}/EnergyCost/Report",
            headers=_headers(self._token),
            json={
                "DeviceId": device_id,
                "UseCurrency": False,
                "FromDate": f"{from_str}T00:00:00",
                "ToDate": f"{to_str}T00:00:00",
            },
            raise_for_status=True,
        ) as resp:
            result: dict[Any, Any] = await resp.json()
            return result

    async def set_device_state(self, device: Any) -> None:
        """Update device state.

        This method is as dumb as it gets. Device is responsible for updating
        the state and managing EffectiveFlags.
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

        async with self._session.post(
            f"{BASE_URL}/Device/{setter}",
            headers=_headers(self._token),
            json=device,
            raise_for_status=True,
        ) as resp:
            # Read response but don't return it since method returns None
            await resp.json()
