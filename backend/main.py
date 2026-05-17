import logging
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import flight_service

load_dotenv()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

api_key = os.getenv("AIRLABS_API_KEY")
if not api_key:
    logger.error("AIRLABS_API_KEY is not set. Copy .env.example to .env and add your key.")
    sys.exit(1)

flight_service.configure(api_key)

app = FastAPI(title="RDU Observation Deck")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/flights")
async def flights():
    try:
        return await flight_service.get_flights()
    except Exception as exc:
        logger.exception("Error fetching flights")
        raise HTTPException(status_code=503, detail="Flight data unavailable") from exc


@app.get("/api/health")
async def health():
    return {"status": "ok"}
