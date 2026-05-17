"""Fetches aircraft photos from Planespotters.net for display in the UI."""

import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://api.planespotters.net/pub/photos/reg"
USER_AGENT = "RDU-ObservationDeck/1.0 (+mailto:w.jacob.ward@gmail.com)"

HIT_TTL = 12 * 3600   # 12 hours — photos rarely change
MISS_TTL = 5 * 60     # 5 minutes — retry failed/empty lookups sooner


class PlanespottersCache:
    def __init__(self):
        self._data: dict[str, dict | None] = {}
        self._fetched_at: dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def get_photo(self, reg_number: str) -> dict | None:
        async with self._lock:
            age = asyncio.get_event_loop().time() - self._fetched_at.get(reg_number, 0.0)
            cached = self._data.get(reg_number, ...)
            ttl = HIT_TTL if cached else MISS_TTL
            if cached is not ... and age < ttl:
                return cached
            try:
                result = await self._fetch(reg_number)
            except Exception:
                logger.exception("Failed to fetch Planespotters photo for %s", reg_number)
                result = None
            self._data[reg_number] = result
            self._fetched_at[reg_number] = asyncio.get_event_loop().time()
            return result

    async def _fetch(self, reg_number: str) -> dict | None:
        async with httpx.AsyncClient(timeout=10, headers={"User-Agent": USER_AGENT}) as client:
            resp = await client.get(f"{BASE_URL}/{reg_number}")
        resp.raise_for_status()
        photos = resp.json().get("photos", [])
        if not photos:
            return None
        photo = photos[0]
        return {
            "photo_url": photo.get("thumbnail_large", {}).get("src") or photo.get("thumbnail", {}).get("src"),
            "photo_link": photo.get("link"),
            "photo_photographer": photo.get("photographer"),
        }


_cache = PlanespottersCache()


async def get_photo(reg_number: str) -> dict | None:
    return await _cache.get_photo(reg_number)
