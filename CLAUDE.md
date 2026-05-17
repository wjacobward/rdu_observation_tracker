# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A mobile-friendly flight status board for the RDU (Raleigh-Durham) airport observation deck. Displays real-time arrivals and departures fetched from the AirLabs API, with visibility indicators showing whether each flight will pass the observation deck's runway.

## Development Commands

### Backend (Python/FastAPI)
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then fill in AIRLABS_API_KEY
uvicorn main:app --reload --port 8000
```

### Frontend (React/Vite)
```bash
cd frontend
npm install
npm run dev        # dev server at http://localhost:5173, proxies /api → :8000
npm run build      # production build to dist/
```

### Docker (both services together)
```bash
docker compose up --build -d
# backend: 127.0.0.1:8001, frontend: 127.0.0.1:8082
```

There are no tests or linters configured.

## Architecture

### Backend (`/backend`)

`main.py` exposes two endpoints: `GET /api/flights` and `GET /api/health`. All logic lives in two services:

- **`flight_service.py`** — `FlightCache` class fetches RDU arrivals and departures from AirLabs `/schedules` asynchronously, normalizes flight data (parses times, resolves ICAO codes to aircraft names), filters out past flights, and sorts by effective time (actual > estimated > scheduled). Uses a 5-minute TTL cache (configurable via `CACHE_TTL_SECONDS`). Falls back to stale cache if the API call fails.

- **`runway_service.py`** — Determines whether a flight will be visible from the observation deck. RDU's runway 23R/5L serves mainline jets (visible); regional jets use 23L/5R (not visible). Resolution: check aircraft ICAO type first, then fall back to airline heuristic (mainline vs. regional carrier).

- **`data/`** — Three static lookup tables: `aircraft_types.py` (ICAO → name), `airline_names.py` (IATA → carrier name), `airport_cities.py` (IATA → city).

### Frontend (`/frontend/src`)

**Component tree:**
```
App
├── IdleOverlay       — "Are you there?" prompt after 1hr inactivity
├── NextFlight        — Large featured card for the next flight, refreshes countdown every 15s
└── FlightList
    └── FlightCard[]  — Compact cards; dimmed if not visible from deck
```

**`hooks/useFlights.js`** — Polls `/api/flights` every 30 seconds. Tracks user activity; shows idle prompt after 1 hour, auto-pauses after 5 more minutes. Freezes timers when the tab is backgrounded (`visibilitychange`) and resumes + refetches on return.

**`utils/formatters.js`** — All display formatting: `formatTime()` (local 12h), `formatCountdown()` (relative), `statusLabel()`, `statusColor()` (Tailwind classes).

### Production Deployment

`docker-compose.yml` runs both services. `rdu-obs.nginx.conf` is a host-level reverse proxy template — copy to `/etc/nginx/sites-available/` and set your domain. `frontend/nginx.conf` (inside the frontend container) serves the built React app and proxies `/api/*` to the backend.

## Key Design Decisions

- **API quota**: AirLabs free tier is limited. The 5-minute backend cache means ~240 API calls/day. The frontend's 30-second poll hits only the local backend, not AirLabs.
- **Visibility heuristic**: `deck_visible` can be `true`, `false`, or `null` (unknown). Unknown is treated as potentially visible in the UI.
- **Tailwind custom theme**: `surface` (#111827), `card` (#1f2937), arrivals use emerald, departures use amber.
- **Mobile-first**: Uses `pt-safe` (notch-aware padding), JetBrains Mono font, dark theme — designed for an always-on display at the airport.
