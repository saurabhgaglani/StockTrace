import asyncio
import uuid
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from graph_service import get_dependency_path
from impact_scorer import score_impact
from minimax_service import generate_explanation
from photon_service import send_alert
from market_poller import market_poll_loop
from news_poller import news_poll_loop

# Shared state
watchlist: dict[str, list[str]] = {}  # user_id -> [symbols]
event_store: deque = deque(maxlen=50)

# Seed demo events so UI has content immediately
DEMO_EVENTS = [
    {"id": "demo-1", "type": "news_event", "symbol": "TSLA", "headline": "Mining disruption in Mali raises concerns over regional mineral supply", "source": "gdelt", "event_type": "geopolitical", "entities": ["Mali"], "timestamp": datetime.now(timezone.utc).isoformat()},
    {"id": "demo-2", "type": "news_event", "symbol": "NVDA", "headline": "New export controls could affect advanced chip shipments", "source": "newsapi", "event_type": "geopolitical", "entities": ["Taiwan"], "timestamp": datetime.now(timezone.utc).isoformat()},
    {"id": "demo-3", "type": "news_event", "symbol": "NVDA", "headline": "Taiwan earthquake raises supply chain questions for semiconductor firms", "source": "gdelt", "event_type": "geopolitical", "entities": ["Taiwan"], "timestamp": datetime.now(timezone.utc).isoformat()},
    {"id": "demo-4", "type": "news_event", "symbol": "XOM", "headline": "Shipping disruption near key trade route lifts oil market uncertainty", "source": "newsapi", "event_type": "supply_chain", "entities": ["Middle East"], "timestamp": datetime.now(timezone.utc).isoformat()},
    {"id": "demo-5", "type": "news_event", "symbol": "AAPL", "headline": "Manufacturing slowdown in key supplier region sparks delivery concerns", "source": "newsapi", "event_type": "supply_chain", "entities": ["Zhengzhou"], "timestamp": datetime.now(timezone.utc).isoformat()},
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    for e in reversed(DEMO_EVENTS):
        event_store.appendleft(e)
    # Default demo watchlist
    watchlist["demo-user"] = ["TSLA", "NVDA", "AAPL", "XOM"]
    t1 = asyncio.create_task(market_poll_loop(watchlist))
    t2 = asyncio.create_task(news_poll_loop(event_store, watchlist))
    yield
    t1.cancel()
    t2.cancel()

app = FastAPI(title="StockTrace", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- Models ---
class WatchlistAdd(BaseModel):
    user_id: str
    symbol: str

class TestEvent(BaseModel):
    headline: str
    source: str = "manual-demo"
    entities: list[str] = []
    event_type: str = "geopolitical"
    symbol: str = "TSLA"

# --- Endpoints ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/watchlist")
def add_to_watchlist(body: WatchlistAdd):
    watchlist.setdefault(body.user_id, [])
    if body.symbol not in watchlist[body.user_id]:
        watchlist[body.user_id].append(body.symbol)
    return {"user_id": body.user_id, "watchlist": watchlist[body.user_id]}

@app.get("/watchlist/{user_id}")
def get_watchlist(user_id: str):
    return {"user_id": user_id, "watchlist": watchlist.get(user_id, [])}

@app.get("/events")
def get_events(symbol: str = None):
    events = list(event_store)
    if symbol:
        events = [e for e in events if e.get("symbol") == symbol]
    return events

@app.get("/graph/path")
def graph_path(entity: str, ticker: str):
    path = get_dependency_path(entity, ticker)
    return {"entity": entity, "ticker": ticker, "path": path}

@app.get("/analysis")
async def get_analysis(symbol: str, event_id: str):
    event = next((e for e in event_store if e["id"] == event_id), None)
    if not event:
        raise HTTPException(404, "Event not found")
    return await _run_analysis(symbol, event)

@app.post("/events/test")
async def test_event(body: TestEvent):
    event = {
        "id": f"test-{uuid.uuid4().hex[:8]}",
        "type": "news_event",
        "symbol": body.symbol,
        "headline": body.headline,
        "source": body.source,
        "event_type": body.event_type,
        "entities": body.entities,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    event_store.appendleft(event)
    result = await _run_analysis(body.symbol, event)
    return result

async def _run_analysis(symbol: str, event: dict) -> dict:
    entities = event.get("entities", [])
    path = []
    for entity in entities:
        p = get_dependency_path(entity, symbol)
        if p:
            path = p
            break

    scoring = score_impact(event, path)
    explanation = await generate_explanation(
        symbol, event["headline"], path, scoring["impact_level"]
    )

    # Fire iMessage alert (non-blocking)
    if event.get("id") == "demo-1":
        print("[demo-test] Firing alert for Tesla + Mali event.")
    send_alert(symbol, event["headline"], explanation)

    return {
        "event": event,
        "path": path,
        "impact_score": scoring["impact_score"],
        "impact_level": scoring["impact_level"],
        "explanation": explanation,
    }
