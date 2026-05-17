"""Fetches RDU flight schedule from AeroDataBox (via RapidAPI) for aircraft type enrichment."""

import asyncio
import logging
import os
from datetime import datetime, timedelta, timezone

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://aerodatabox.p.rapidapi.com"
AIRPORT_IATA = "RDU"
# RDU is Eastern time; use EST offset (UTC-5) with a generous window so DST doesn't matter
AIRPORT_UTC_OFFSET_HOURS = -5


class AeroDataBoxCache:
    def __init__(self, ttl_seconds: int = 300):
        self._ttl = ttl_seconds
        self._data: dict[str, str] | None = None
        self._fetched_at: float = 0.0
        self._lock = asyncio.Lock()
        self._api_key: str | None = None

    def configure(self, api_key: str):
        self._api_key = api_key

    async def get_aircraft_lookup(self) -> dict[str, str]:
        """Returns a dict mapping flight_iata (e.g. 'UA1536') → aircraft model name."""
        async with self._lock:
            age = asyncio.get_event_loop().time() - self._fetched_at
            if self._data is not None and age < self._ttl:
                return self._data
            try:
                self._data = await self._fetch()
                self._fetched_at = asyncio.get_event_loop().time()
            except Exception:
                logger.exception("Failed to fetch AeroDataBox data")
                if self._data is None:
                    return {}
            return self._data

    async def _fetch(self) -> dict[str, str]:
        if not self._api_key:
            return {}

        now_utc = datetime.now(timezone.utc)
        offset = timedelta(hours=AIRPORT_UTC_OFFSET_HOURS)
        # Wide window: 2 hours ago to 14 hours ahead (local), so DST ±1h doesn't matter
        from_local = (now_utc + offset - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
        to_local = (now_utc + offset + timedelta(hours=14)).strftime("%Y-%m-%dT%H:%M")

        url = f"{BASE_URL}/flights/airports/iata/{AIRPORT_IATA}/{from_local}/{to_local}"
        params = {
            "withLeg": "true",
            "direction": "Both",
            "withCancelled": "true",
            "withCodeshared": "false",
            "withCargo": "false",
            "withPrivate": "false",
        }
        headers = {
            "x-rapidapi-host": "aerodatabox.p.rapidapi.com",
            "x-rapidapi-key": self._api_key,
        }

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params=params, headers=headers)
        resp.raise_for_status()

        lookup: dict[str, str] = {}
        data = resp.json()
        for flight in (*data.get("departures", []), *data.get("arrivals", [])):
            model = flight.get("aircraft", {}).get("model")
            number = flight.get("number", "").replace(" ", "")
            if number and model:
                lookup[number] = model

        logger.info("AeroDataBox: loaded %d aircraft mappings", len(lookup))
        return lookup


_cache = AeroDataBoxCache(ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "300")))


def configure(api_key: str):
    _cache.configure(api_key)


async def get_aircraft_lookup() -> dict[str, str]:
    return await _cache.get_aircraft_lookup()
