"""Fetches flight data from AirLabs and caches it."""

import asyncio
import logging
import os
from datetime import datetime, timezone
from typing import Any

import httpx

from data.aircraft_types import get_aircraft_name
from data.airline_names import get_airline_name
from data.airport_cities import get_city_name
from runway_service import estimate_visibility

logger = logging.getLogger(__name__)

AIRLABS_BASE = "https://airlabs.co/api/v9"
AIRPORT = "RDU"

# Fields we request from AirLabs to stay within response size limits
SCHEDULE_FIELDS = (
    "flight_iata,airline_iata,dep_iata,arr_iata,"
    "dep_time_utc,arr_time_utc,status,aircraft_icao,"
    "dep_delayed,arr_delayed,delayed,"
    "dep_actual_utc,arr_actual_utc,"
    "dep_estimated_utc,arr_estimated_utc"
)


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def _effective_time(flight: dict) -> str:
    """Best available time for sorting: actual → estimated → scheduled."""
    return flight["actual_time"] or flight["estimated_time"] or flight["scheduled_time"]


def _normalize_status(raw: str | None, delay_min: int) -> str:
    if not raw:
        return "scheduled"
    raw = raw.lower()
    if raw in ("cancelled", "cancel"):
        return "cancelled"
    if raw in ("landed", "arrived"):
        return "landed"
    if raw in ("departed", "diverted"):
        return "departed"
    if raw in ("active", "en-route", "en route"):
        return "en_route"
    if raw == "scheduled" and delay_min > 0:
        return "delayed"
    return raw


def _build_flight(raw: dict[str, Any], direction: str) -> dict[str, Any]:
    is_arrival = direction == "arrival"
    other_airport_iata = raw.get("dep_iata") if is_arrival else raw.get("arr_iata")

    sched_time_str = raw.get("arr_time_utc") if is_arrival else raw.get("dep_time_utc")
    estimated_str = raw.get("arr_estimated_utc") if is_arrival else raw.get("dep_estimated_utc")
    actual_str = raw.get("arr_actual_utc") if is_arrival else raw.get("dep_actual_utc")
    delay_min = int(raw.get("arr_delayed") or raw.get("delayed") or 0) if is_arrival else int(raw.get("dep_delayed") or raw.get("delayed") or 0)

    scheduled_time = _parse_time(sched_time_str)
    estimated_time = _parse_time(estimated_str)
    actual_time = _parse_time(actual_str)

    if scheduled_time is None:
        return None

    raw_status = raw.get("status", "scheduled")
    status = _normalize_status(raw_status, delay_min)

    aircraft_code = raw.get("aircraft_icao")
    aircraft_name = get_aircraft_name(aircraft_code)

    airline_iata = raw.get("airline_iata")

    return {
        "flight_number": raw.get("flight_iata") or raw.get("flight_icao") or "Unknown",
        "airline": get_airline_name(airline_iata),
        "airline_iata": airline_iata,
        "direction": direction,
        "other_airport_iata": other_airport_iata,
        "other_airport_city": get_city_name(other_airport_iata),
        "scheduled_time": scheduled_time.isoformat(),
        "estimated_time": estimated_time.isoformat() if estimated_time else None,
        "actual_time": actual_time.isoformat() if actual_time else None,
        "status": status,
        "delay_minutes": delay_min,
        "aircraft_code": aircraft_code,
        "aircraft_type": aircraft_name or (aircraft_code or None),
    }


class FlightCache:
    def __init__(self, ttl_seconds: int = 300):
        self._ttl = ttl_seconds
        self._data: list[dict] | None = None
        self._fetched_at: float = 0.0
        self._lock = asyncio.Lock()
        self._api_key: str | None = None

    def configure(self, api_key: str):
        self._api_key = api_key

    async def get_flights(self) -> list[dict]:
        async with self._lock:
            age = asyncio.get_event_loop().time() - self._fetched_at
            if self._data is not None and age < self._ttl:
                return self._data
            try:
                self._data = await self._fetch_all()
                self._fetched_at = asyncio.get_event_loop().time()
            except Exception:
                logger.exception("Failed to fetch flight data")
                if self._data is None:
                    raise
                # Return stale data rather than failing
            return self._data

    async def _fetch_all(self) -> list[dict]:
        if not self._api_key:
            raise RuntimeError("AIRLABS_API_KEY is not configured")
        params_base = {"api_key": self._api_key, "fields": SCHEDULE_FIELDS}
        async with httpx.AsyncClient(timeout=15) as client:
            arr_resp, dep_resp = await asyncio.gather(
                client.get(f"{AIRLABS_BASE}/schedules", params={**params_base, "arr_iata": AIRPORT}),
                client.get(f"{AIRLABS_BASE}/schedules", params={**params_base, "dep_iata": AIRPORT}),
            )
        arr_resp.raise_for_status()
        dep_resp.raise_for_status()

        arrivals_raw = arr_resp.json().get("response", [])
        departures_raw = dep_resp.json().get("response", [])

        flights: list[dict] = []
        for raw in arrivals_raw:
            flight = _build_flight(raw, "arrival")
            if flight:
                flights.append(flight)
        for raw in departures_raw:
            flight = _build_flight(raw, "departure")
            if flight:
                flights.append(flight)

        flights.sort(key=_effective_time)
        return flights


_cache = FlightCache(ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "300")))


def configure(api_key: str):
    _cache.configure(api_key)


async def get_flights() -> dict:
    now = datetime.now(timezone.utc)
    all_flights = await _cache.get_flights()

    # Only show flights whose effective time is in the future
    future = [
        f for f in all_flights
        if datetime.fromisoformat(_effective_time(f)).timestamp() >= now.timestamp()
    ]

    for flight in future:
        flight.update(estimate_visibility(flight.get("aircraft_code"), flight.get("airline_iata")))

    next_flight = future[0] if future else None
    upcoming = future[1:]

    return {
        "updated_at": now.isoformat(),
        "next_flight": next_flight,
        "upcoming": upcoming,
    }
