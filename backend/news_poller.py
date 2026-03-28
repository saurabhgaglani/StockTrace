import os
import asyncio
from datetime import datetime, timezone
import httpx
from dotenv import load_dotenv

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_API_KEY")
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

SYMBOL_KEYWORDS = {
    "TSLA": "lithium OR cobalt OR battery supply chain OR Mali mining OR war sanctions minerals",
    "NVDA": "semiconductor export control OR Taiwan chip OR GPU supply OR Iran sanctions technology OR Trump chip ban",
    "AAPL": "Foxconn OR Apple supplier OR Zhengzhou manufacturing OR Trump tariff China",
    "XOM": "OPEC OR crude oil OR refinery OR oil supply disruption OR Iran oil sanctions OR Middle East war oil",
}

GEOPOLITICAL_QUERIES = [
    ("Iran war sanctions oil", "XOM", "geopolitical"),
    ("Trump Iran nuclear deal", "XOM", "geopolitical"),
    ("Middle East conflict oil", "XOM", "geopolitical"),
    ("Trump tariff China trade war", "AAPL", "geopolitical"),
    ("Russia Ukraine war sanctions", "XOM", "geopolitical"),
    ("war semiconductor export ban", "NVDA", "geopolitical"),
]

GDELT_QUERIES = [
    # Original
    ("Mali lithium mining", "TSLA", "geopolitical"),
    ("Taiwan semiconductor", "NVDA", "geopolitical"),
    ("Foxconn Apple", "AAPL", "supply_chain"),
    ("OPEC oil supply", "XOM", "supply_chain"),
    ("Iran war oil", "XOM", "geopolitical"),
    ("Trump tariff China", "AAPL", "geopolitical"),
    # Additional supply chain coverage
    ("cobalt Congo mining", "TSLA", "supply_chain"),
    ("lithium Chile Argentina", "TSLA", "supply_chain"),
    ("TSMC chip shortage", "NVDA", "supply_chain"),
    ("rare earth China export", "NVDA", "supply_chain"),
    ("Strait of Hormuz shipping", "XOM", "supply_chain"),
    ("Red Sea shipping disruption", "XOM", "supply_chain"),
    ("Apple China factory", "AAPL", "supply_chain"),
    ("semiconductor wafer supply", "NVDA", "supply_chain"),
    ("battery materials shortage", "TSLA", "supply_chain"),
    ("port strike logistics", "AAPL", "supply_chain"),
]


async def _auto_analyse_and_alert(event: dict):
    """Score a live event; if high impact, generate explanation and send alert."""
    from graph_service import get_dependency_path
    from impact_scorer import score_impact
    from minimax_service import generate_explanation
    from photon_service import send_alert

    symbol = event["symbol"]
    entities = event.get("entities", [])

    path = []
    for entity in entities:
        p = get_dependency_path(entity, symbol)
        if p:
            path = p
            break

    scoring = score_impact(event, path)
    event["impact_score"] = scoring["impact_score"]
    event["impact_level"] = scoring["impact_level"]
    event["path"] = path

    if scoring["impact_level"] == "high":
        try:
            explanation = await generate_explanation(
                symbol, event["headline"], path, scoring["impact_level"]
            )
            event["explanation"] = explanation
            send_alert(symbol, event["headline"], explanation)
            print(f"[auto-alert] HIGH impact → alerted for {symbol}: {event['headline'][:60]}")
        except Exception as e:
            print(f"[auto-alert] explanation/alert failed: {e}")


async def poll_newsapi(event_store, watchlist: dict):
    symbols = {s for items in watchlist.values() for s in items}
    async with httpx.AsyncClient(timeout=10) as client:
        for symbol in symbols:
            query = SYMBOL_KEYWORDS.get(symbol)
            if not query:
                continue
            try:
                r = await client.get(
                    "https://newsapi.org/v2/everything",
                    params={"q": query, "pageSize": 3, "sortBy": "publishedAt", "apiKey": NEWSAPI_KEY}
                )
                for article in r.json().get("articles", []):
                    event_store.appendleft({
                        "id": f"news-{symbol}-{hash(article['title']) & 0xFFFFFF}",
                        "type": "news_event",
                        "symbol": symbol,
                        "headline": article["title"],
                        "source": "newsapi",
                        "event_type": "supply_chain",
                        "entities": [symbol],
                        "timestamp": article.get("publishedAt", datetime.now(timezone.utc).isoformat()),
                        "url": article.get("url"),
                    })
            except Exception as e:
                print(f"[news_poller] newsapi {symbol}: {e}")


async def poll_gdelt(event_store):
    async with httpx.AsyncClient(timeout=10) as client:
        for (query, symbol, event_type) in GDELT_QUERIES:
            try:
                r = await client.get(
                    GDELT_URL,
                    params={
                        "query": query,
                        "mode": "artlist",
                        "maxrecords": 3,
                        "timespan": "2h",
                        "format": "json",
                    }
                )
                articles = r.json().get("articles", [])
                for article in articles:
                    raw_date = article.get("seendate")
                    try:
                        ts = datetime.strptime(raw_date, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).isoformat()
                    except Exception:
                        ts = datetime.now(timezone.utc).isoformat()

                    event_id = f"gdelt-{symbol}-{hash(article.get('title', '')) & 0xFFFFFF}"

                    # Skip if already in store
                    if any(e.get("id") == event_id for e in event_store):
                        continue

                    event = {
                        "id": event_id,
                        "type": "news_event",
                        "symbol": symbol,
                        "headline": article.get("title", query),
                        "source": "gdelt",
                        "event_type": event_type,
                        "entities": [query.split()[0]],
                        "timestamp": ts,
                        "url": article.get("url"),
                    }
                    event_store.appendleft(event)

                    # Auto-analyse in background (non-blocking)
                    asyncio.create_task(_auto_analyse_and_alert(event))

            except Exception as e:
                print(f"[news_poller] gdelt {query}: {e}")


async def news_poll_loop(event_store, watchlist: dict):
    tick = 0
    while True:
        await poll_gdelt(event_store)
        if tick % 3 == 0:
            await poll_newsapi(event_store, watchlist)
        tick += 1
        await asyncio.sleep(60)
