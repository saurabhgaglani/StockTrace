# DESIGN_BACKEND.md

## Purpose

Backend design for a **hackathon MVP** of a messaging-based stock/watchlist agent that:

- monitors stocks using REST APIs
- detects meaningful events (market + news)
- maps events to a **Neo4j dependency graph**
- generates concise explanations using MiniMax
- sends alerts via Photon

This system is optimized for:
- demo reliability
- explainability
- fast implementation (24 hours)
- minimal infrastructure

---

# 1. Core Product Idea

A messaging agent that:

> Watches stocks for you and alerts you when something meaningful happens.

NOT:
- trading bot
- prediction engine
- alpha generator

YES:
- awareness tool
- decision-support system
- context provider

---

# 2. High-Level Flow

1. User adds stock to watchlist
2. Backend polls:
   - market data
   - news
3. Detect:
   - anomaly OR relevant news
4. Query Neo4j dependency graph
5. Score impact
6. Generate explanation (MiniMax)
7. Send alert (Photon)

---

# 3. APIs Used

## Market APIs (REST)

### Finnhub
Use:
- `/quote`
- `/stock/candle`
- `/company-news`
- `/news-sentiment`

Purpose:
- price + movement
- baseline comparison
- contextual headlines

---

### Twelve Data
Use:
- `/quote`
- `/time_series`
- `/market_movers` (optional)

Purpose:
- fallback + cleaner REST access

---

### Massive (optional)
Use:
- REST aggregates if needed

Avoid WebSockets for MVP.

---

## News APIs

### GDELT (Primary)
- keyword-based global event detection
- multi-language + translated

Use:
- keyword queries with event terms

---

### NewsAPI (Secondary)
- cleaner headlines
- easier filtering

Use:
- `/everything`

---

# 4. Polling Strategy

- Every 60s → GDELT
- Every 60–120s → market data
- Every 3–5 min → NewsAPI

---

# 5. Backend Modules

- API server
- market polling service
- news polling service
- anomaly detector
- Neo4j graph service
- impact scoring service
- MiniMax service
- Photon messaging service

---

# 6. API Endpoints

## Add to Watchlist

```json
POST /watchlist
{
  "user_id": "demo-user",
  "symbol": "TSLA"
}
```

---

## Manual Event Injection (for demo)

```json
POST /events/test
{
  "headline": "Conflict disrupts mining operations in Mali",
  "source": "manual-demo",
  "entities": ["Mali"],
  "event_type": "geopolitical"
}
```

---

## Get Watchlist

```
GET /watchlist/:user_id
```

---

## Health Check

```
GET /health
```

---

# 7. Event Formats

## Market Event

```json
{
  "type": "market_anomaly",
  "symbol": "TSLA",
  "price": 182.45,
  "change_percent": -3.8,
  "volume_ratio": 2.7,
  "timestamp": "2026-03-28T19:10:00Z"
}
```

---

## News Event

```json
{
  "type": "news_event",
  "headline": "Conflict disrupts mining operations in Mali",
  "source": "gdelt",
  "entities": ["Mali"],
  "event_type": "geopolitical"
}
```

---

# 8. Neo4j Graph Design

## Node Types
- Company
- Supplier
- Material
- Region
- Country

## Relationship Types
- DEPENDS_ON
- SUPPLIED_BY
- OPERATES_IN
- PARTNERED_WITH
- MINES_IN
- REFINES_IN

## Example Path
```
TSLA → battery → lithium → supplier → Mali
```

---

# 9. Neo4j Configuration

Fill this in your `.env`:

```env
NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=
NEO4J_DATABASE=
NEO4J_INSTANCE_ID=
NEO4J_INSTANCE_NAME=
```

---

## Instructions

1. Create Neo4j instance (AuraDB recommended)
2. Paste credentials above
3. Seed minimal graph:
   - TSLA
   - lithium supply chain
   - 1–2 suppliers
   - 1 region (Mali)

4. Test with Cypher before backend integration

---

# 10. API Keys Configuration

Add all keys to `.env`:

```env
# Market APIs
FINNHUB_API_KEY= d742eehr01qno4q06ob0d742eehr01qno4q06obg
TWELVEDATA_API_KEY= 9ec56807f7614a6d8bd7caed41749c534
MASSIVE_API_KEY= 1iLq_E70fARtYy8T7Zd8Sp_K_2vGOqbO

# News APIs
GDELT_API_KEY= no api key example req - URL: https://api.gdeltproject.org/api/v2/doc/doc?query=%22donald%20trump%22&mode=tonechart
NEWSAPI_API_KEY= 8305c5c7d69f4adba26ede04fd2f2641 

Search things directly relavant to the supply chains and find news directly relavant. 

# AI
MINIMAX_API_KEY= sk-api-o5OYj0UbPz8adc_5NbWZd9MQx3gp13VDmZLffy8NJzUw2hScZm_0IrSAOpUzWK9tziVU-N5CwQnrN2Uu-3rleDlDSTKySd7zLrfTvtvyxCn1YlPVsNoMIe0
MINIMAX_MODEL= MiniMax-M2.7



# Database
NEO4J_URI=neo4j+s://6fad9529.databases.neo4j.io
NEO4J_USERNAME=6fad9529
NEO4J_PASSWORD=VGyfnM2gOZvWVKUiXTVRyZUiTuP6vqVgOC33DiOyc3o
NEO4J_DATABASE=6fad9529
AURA_INSTANCEID=6fad9529
AURA_INSTANCENAME=Free instance

# App
APP_ENV=development
APP_PORT=8000
```

---

# 11. Anomaly Detection

Trigger when:

- price move ≥ 2%
- volume ≥ 2.5x baseline
- unusual candle movement

---

# 12. Impact Scoring (Simple)

Inputs:
- event severity
- graph match
- market anomaly

Output:

```json
{
  "impact_score": 0.78,
  "impact_level": "high"
}
```

---

# 13. MiniMax Prompt

```
You are generating a short neutral investment alert.

Rules:
- no financial advice
- no predictions
- explain why user got alert
- be concise

Input:
- stock
- headline
- graph path
- impact level

Output:
2–4 short sentences
```

---

# 14. Photon Alert Format

```json
{
  "symbol": "TSLA",
  "headline": "Conflict disrupts mining operations in Mali",
  "message": "TSLA may have upstream exposure to disruption in Mali."
}
```

---

# 15. Build Order

1. Setup `.env`
2. Watchlist API
3. News polling
4. Market polling
5. Neo4j integration
6. Impact scoring
7. MiniMax
8. Photon
9. Demo endpoint

---

# 16. Demo Plan

- Add TSLA
- Trigger event
- Show:
  - event
  - graph path
  - explanation
  - Photon message

---

# 17. Final Rule

Prefer:
- simple > complex
- deterministic > fancy
- explainable > magical

This is a hackathon MVP.

Make it work.