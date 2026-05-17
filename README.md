# RDU Observation Deck

Mobile-friendly flight board for the RDU observation deck. Shows the next arriving/departing flight prominently with a live countdown, followed by upcoming flights.

## Quick start

### 1. Get an AirLabs API key

Sign up at https://airlabs.co — the free trial includes 1,000 API calls (enough for testing). For continuous use, paid plans start at ~$9/month.

### 2. Create your `.env`

```bash
cp backend/.env.example backend/.env
# Edit backend/.env and paste your API key
```

### 3. Run with Docker Compose

```bash
docker compose up --build -d
```

Both containers bind to `127.0.0.1` only — they're not reachable from outside the host.

### 4. Install the nginx site config

Edit `rdu-obs.nginx.conf` to set your domain/IP, then install it:

```bash
sudo cp rdu-obs.nginx.conf /etc/nginx/sites-available/rdu-obs
sudo ln -s /etc/nginx/sites-available/rdu-obs /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

For HTTPS: `sudo certbot --nginx -d yourdomain.com`

---

## Local development (without Docker)

**Backend:**
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend** (in a separate terminal):
```bash
cd frontend
npm install
npm run dev        # http://localhost:5173 — proxies /api to :8000
```

---

## How it works

- **Backend** fetches arrivals and departures from AirLabs every 5 minutes (configurable via `CACHE_TTL_SECONDS` in `.env`) and caches the result. The frontend polls this cached endpoint every 30 seconds — so API quota usage stays low.
- **Aircraft type** is resolved from AirLabs' ICAO type codes (e.g. `B738` → "Boeing 737-800") using a built-in lookup table — no extra API calls.
- **Airport cities** are resolved from a built-in lookup table covering ~150 common airports.
- In Docker, nginx serves the built React app and proxies `/api/*` to the Python backend container.

## API quota

With default 5-minute caching and the app in use from 8 AM–6 PM:
- 2 AirLabs calls × 12/hr × 10 hrs = **240 calls/day ≈ 7,200/month**
- Fits comfortably within the $9/month plan (10,000 calls/month)
