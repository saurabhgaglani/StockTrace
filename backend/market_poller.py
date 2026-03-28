import os
import asyncio
from collections import deque
from datetime import datetime, timezone
import httpx
from dotenv import load_dotenv

load_dotenv()

FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")
POLL_INTERVAL = 60  # seconds
_baselines: dict[str, float] = {}  # symbol -> prev_close volume baseline

event_store: deque = deque(maxlen=50)  # shared with main

SYMBOL_KEYWORDS = {
    "TSLA": ["lithium", "battery", "cobalt", "EV", "Tesla supply chain"],
    "NVDA": ["semiconductor", "chip", "GPU", "Taiwan", "export control"],
    "AAPL": ["Foxconn", "iPhone", "Apple supplier", "Zhengzhou"],
    "XOM": ["oil", "crude", "OPEC", "refinery", "energy"],
}

async def poll_market(watchlist: dict):
    """Poll Finnhub quotes for all watchlist symbols."""
    symbols = {s for items in watchlist.values() for s in items}
    if not symbols:
        return
    async with httpx.AsyncClient(timeout=10) as client:
        for symbol in symbols:
            try:
                r = await client.get(
                    f"https://finnhub.io/api/v1/quote",
                    params={"symbol": symbol, "token": FINNHUB_KEY}
                )
                data = r.json()
                price = data.get("c", 0)
                prev_close = data.get("pc", price) or price
                change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0
                volume = data.get("v", 0)
                baseline = _baselines.get(symbol, volume)
                volume_ratio = (volume / baseline) if baseline else 1.0
                _baselines[symbol] = baseline or volume

                if abs(change_pct) >= 2.0 or volume_ratio >= 2.5:
                    event_store.appendleft({
                        "id": f"market-{symbol}-{int(datetime.now(timezone.utc).timestamp())}",
                        "type": "market_anomaly",
                        "symbol": symbol,
                        "price": price,
                        "change_percent": round(change_pct, 2),
                        "volume_ratio": round(volume_ratio, 2),
                        "headline": f"{symbol} moved {change_pct:+.1f}% with {volume_ratio:.1f}x volume",
                        "source": "finnhub",
                        "event_type": "market_anomaly",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
            except Exception as e:
                print(f"[market_poller] {symbol}: {e}")

async def market_poll_loop(watchlist: dict):
    while True:
        await poll_market(watchlist)
        await asyncio.sleep(POLL_INTERVAL)
