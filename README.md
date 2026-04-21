
# StockTrace

**From headline to context in seconds — we trace the impact so you don't have to.**

StockTrace is an AI-powered stock signal tracker that connects real-world news events to the stocks they affect. Instead of drowning in headlines, you get instant, structured context on how breaking news impacts your watchlist — delivered in the app and straight to your phone via SMS.

---

## Screenshots

### Dashboard — Live Signals & Stock Chart
![Dashboard](./assets/screenshot1.png)


### SMS Alerts — AI Context Delivered to Your Phone
![SMS Alerts](./assets/screenshot2.png)

---

## Features

- **Watchlist** — Track a curated set of stocks (e.g. Tesla, NVIDIA, Apple, ExxonMobil, Boeing) with live price and daily change.
- **Live Signals** — Real-time and 24h digest signals tagged by category (supply chain, geopolitics, earnings, etc.) and impact level (high/medium/low).
- **Agent Insight** — Click any signal to get AI-generated context on how the news connects to a specific stock's fundamentals, supply chain, or market position.
- **Stock Chart** — Interactive price chart with 1D / 1W / 1M / 3M / 1Y views.
- **SMS Alerts** — The AI agent pushes investment context summaries directly to your phone when high-impact signals are detected.
- **Scenario Explorer** — Pre-built scenario chips (e.g. "Tesla + Mali", "NVIDIA + Export Controls") to explore cross-asset event impacts instantly.

---

## How It Works

1. News and market signals are ingested and tagged with relevant tickers.
2. The AI agent analyzes each signal and generates a plain-English impact summary for each affected stock.
3. High-priority signals trigger SMS notifications with the context summary and a disclaimer.
4. Users can click into any signal in the dashboard to read the full agent insight.

---

## Tech Stack

> Update this section with your actual stack.

- **Frontend**: React, running on `localhost:3000`
- **AI Agent**: Claude (Anthropic) for signal analysis and impact summaries
- **SMS**: Twilio (or similar) for push notifications
- **Data**: Live market feed + news aggregation

---

## Getting Started
```bash
# Install dependencies
npm install

# Start the dev server
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000).

---

## Disclaimer

StockTrace provides market context only — **not financial advice**. Always do your own research before making investment decisions.

