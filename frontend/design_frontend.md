# StockTrace — Frontend Design Plan (React + Tailwind)

## Overview

**StockTrace** should feel like a polished, demo-friendly AI agent product.

This is **not** a dense trading dashboard.
It is a **decision-support experience** that shows how an AI agent monitors what a user cares about, detects relevant events, reasons through connections, and returns clear context.

The design should feel:

- modern
- intelligent
- interactive
- slightly gamified
- clean enough for a live demo
- visually impressive without becoming cluttered

The UI should communicate:

> Add something you care about.  
> Watch the agent detect a signal.  
> See how it reasons.  
> Get context instantly.

---

## Product Positioning

StockTrace is an AI agent for everyday investors and curious users who want context, not noise.

Core idea:

> Track companies you care about, detect meaningful events, and understand why they matter before you make a decision.

Important tone:

- not financial advice
- not a trading terminal
- not an analytics platform
- not a chart-heavy Bloomberg clone

Instead:

> An AI agent that connects headlines, dependencies, and market context into short, understandable explanations.

---

## Design Direction

### High-Level Feel

The app should feel like a mix of:

- an elegant product demo
- a smart operations interface
- a lightweight intelligence console

### Visual Characteristics

- dark-ish or deep neutral UI is acceptable here because it helps the agent/demo feel alive
- strong card design
- layered panels
- subtle motion
- glowing active states
- clean typography
- spacious layout
- obvious focus on the active story

This should feel more cinematic than a normal SaaS app, but still usable.

---

## Tech / Styling Direction

### Stack

- React
- Tailwind CSS

### Tailwind Feel

Use Tailwind to create:

- rounded panels
- subtle borders
- layered surfaces
- hover states
- transitions
- controlled glow for active elements

Avoid over-styling.
The UI should feel premium because of:

- spacing
- hierarchy
- animation restraint
- contrast
- clarity

---

## Core UX Principle

The app should always answer:

1. What am I tracking?
2. What happened?
3. Why does it matter?
4. What did the agent infer?

That means every screen should have:

- tracked items
- a live signal or headline
- a reasoning path
- a final output

---

## Recommended Layout

### Desktop Layout

Use a 3-column structure for the main experience.

#### Left Column — Watchlist
Purpose:
- Show tracked companies/assets
- Let the user quickly select something
- Make the app feel personalized

#### Center Column — Signal Feed / News Cards
Purpose:
- Show recent relevant headlines
- Make the demo interactive
- Give the user something to click

#### Right Column — Agent Analysis
Purpose:
- Show the reasoning chain
- Show impact score
- Show the final explanation message

This is the best structure for a hackathon demo because it makes the flow obvious.

---

## Main Page Structure

### 1. Top Navbar

Include:

- app logo / name: **StockTrace**
- small tagline: `Signal-aware investing`
- optional right-side status indicator: `Agent online`
- optional button: `Add to watchlist`

Design:
- sticky or fixed top bar
- clean divider below
- subtle brand treatment

---

### 2. Hero / Intro Panel

A compact intro card near the top of the page can help frame the experience.

Example headline:

**Track what matters. Understand why.**

Example supporting text:

> StockTrace watches the companies you follow, detects relevant events, and explains why they may matter before you act.

CTA ideas:
- Add Tesla
- Try demo scenario

This can be a compact panel above the 3-column layout or integrated into the center column.

---

## Watchlist Section

### Purpose

The watchlist should feel alive and customizable.
It should not be just plain text.

### Design

Use stacked cards or pill-like rows.

Each watchlist item can show:

- company name
- ticker
- category / industry
- tiny status dot
- optional “active” highlight if selected

### Suggested Demo Watchlist Items

Use a few names that make cross-domain reasoning easy:

1. **Tesla (TSLA)**  
   Good for battery supply chain, energy, mining, China, EV demand

2. **NVIDIA (NVDA)**  
   Good for chips, AI demand, Taiwan, data centers, export controls

3. **Apple (AAPL)**  
   Good for supply chain, China, consumer demand, manufacturing

4. **ExxonMobil (XOM)**  
   Good for oil, geopolitics, shipping disruptions, energy markets

5. **Walmart (WMT)**  
   Good for logistics, consumer trends, shipping, retail demand

6. **Boeing (BA)**  
   Good for regulation, manufacturing issues, supply chains, global events

You do not need all of these visible at once.
For the demo, 3 to 5 is enough.

### Recommendation

Use these four for the strongest demo set:

- Tesla
- NVIDIA
- Apple
- ExxonMobil

This gives you:
- EV / battery story
- AI / chips story
- manufacturing / consumer story
- global commodities story

---

## News / Signal Cards

### Purpose

This section is where the demo becomes interactive.

The cards should feel clickable and meaningful.
They should look like events the agent has surfaced, not a generic RSS feed.

### Card Content

Each signal card can include:

- headline
- source
- timestamp
- related watchlist item(s)
- urgency / relevance badge
- one-line preview

### Example Demo Headlines

Use a mix of geopolitics, supply chain, and macro stories.

#### Tesla Headlines
- **Mining disruption in Mali raises concerns over regional mineral supply**
- **Battery metals surge after export restrictions tighten**
- **Port delays pressure EV manufacturing timelines**

#### NVIDIA Headlines
- **New export controls could affect advanced chip shipments**
- **Cloud providers accelerate GPU orders amid AI demand spike**
- **Taiwan earthquake raises supply chain questions for semiconductor firms**

#### Apple Headlines
- **Manufacturing slowdown in key supplier region sparks delivery concerns**
- **Consumer spending shifts pressure premium device outlook**
- **New regulatory scrutiny hits major mobile platform ecosystems**

#### ExxonMobil Headlines
- **Shipping disruption near key trade route lifts oil market uncertainty**
- **OPEC supply signals push energy stocks into focus**
- **Refinery outage reshapes short-term fuel expectations**

### Recommended Demo Cards to Start With

Use just 4–6 cards on screen.
Best starter set:

1. Mining disruption in Mali raises concerns over regional mineral supply
2. New export controls could affect advanced chip shipments
3. Taiwan earthquake raises supply chain questions for semiconductor firms
4. Shipping disruption near key trade route lifts oil market uncertainty
5. Manufacturing slowdown in key supplier region sparks delivery concerns

### Interaction

When a user clicks a card:

- it becomes active
- the right-side analysis updates
- the related watchlist item highlights
- optional reasoning animation plays

This click is one of the most important moments in the demo.

---

## Agent Analysis Panel

### Purpose

This is the “wow” section.

It should feel like the AI is doing real work.

### Recommended Subsections

#### A. Selected Event
Show the clicked headline again in a smaller focused card.

#### B. Dependency Chain
Show a readable chain like:

`Mali -> Mineral Supply -> Battery Inputs -> Tesla`

or

`Taiwan -> Chip Manufacturing -> GPU Supply -> NVIDIA`

Display this as connected pills, nodes, or a horizontal reasoning path.

#### C. Market Context
Keep it simple:
- current movement
- recent sentiment
- confidence / impact label

Example:
- Market move: `-1.8% today`
- Agent confidence: `Moderate`
- Estimated relevance: `High`

#### D. Explanation Output
This is the most important final card.

Example output:

> Tesla may be indirectly exposed because battery supply chains depend on mineral availability tied to the affected region. Combined with current market movement, this event could increase near-term sensitivity around production assumptions.

Important footer text:

> Context only — not financial advice.

### Design Notes

This panel should feel premium.
Use:

- stronger contrast
- nested cards
- subtle border glow on active output
- tiny animated state for “Analyzing...”

---

## Suggested Demo Flow

The UI should support this exact story:

1. User adds Tesla to watchlist
2. Tesla appears active on left
3. A headline card appears in the center:
   `Mining disruption in Mali raises concerns over regional mineral supply`
4. User clicks the card
5. The agent panel animates:
   - dependency chain appears
   - impact score updates
   - explanation is typed or revealed
6. User understands why it matters

This is your core demo loop.

---

## Card Design System

### Watchlist Card
Should include:
- ticker icon or initial
- company name
- ticker
- subtle hover
- active border or glow

### News Card
Should include:
- headline
- category badge
- related ticker badge
- compact metadata row
- hover lift
- active selected state

### Analysis Card
Should include:
- small section label
- bold value or explanation
- clear spacing
- optional icon

---

## Color / Visual Recommendation

You have more freedom here than on the consulting site.

Suggested direction:

- deep slate / graphite background
- elevated dark panels
- one bright accent color
- one softer secondary accent for states

Good accent directions:
- electric blue
- vivid cyan
- deep violet-blue

These help the app feel live and technical.

### Use color intentionally

Use accent color for:
- selected watchlist item
- active news card
- reasoning nodes
- CTA button
- “Agent online” indicator

Do not make everything glow.

---

## Typography

Use a crisp sans-serif that works well in product UIs.

Strong options:
- Inter
- Geist
- Plus Jakarta Sans

Recommended:
- **Inter** for safety and polish

Typography hierarchy:
- app title
- section title
- card title
- metadata
- reasoning output

The explanation output should be especially readable.

---

## Motion / Microinteractions

Because this is a demo-first product, subtle motion helps a lot.

Add:

- hover lift on cards
- smooth selection transitions
- typing/reveal effect for analysis output
- fade/slide for reasoning nodes
- pulsing status dot for `Agent online`
- slight active glow on selected event

Keep motion fast and confident.

---

## Demo-Friendly UI Features

### 1. Preset Demo Scenarios
Add buttons like:
- Tesla + Mali
- NVIDIA + Export Controls
- Apple + Supplier Slowdown

This makes the demo reliable.

### 2. Simulated Agent State
Useful states:
- Monitoring
- Processing
- Impact detected
- Context ready

### 3. Impact Score
A compact chip or mini-meter works well.

Examples:
- Low
- Moderate
- High

or numeric:
- `72 / 100`

### 4. Context Disclaimer
Keep this visible but small:

> Not a recommendation. Context for human decision-making.

This line is important to the product’s identity.

---

## Recommended Initial React Component Structure

```txt
App
 ├─ Navbar
 ├─ IntroPanel
 ├─ MainLayout
 │   ├─ WatchlistPanel
 │   │   └─ WatchlistItemCard
 │   ├─ SignalFeedPanel
 │   │   └─ NewsSignalCard
 │   └─ AnalysisPanel
 │       ├─ SelectedEventCard
 │       ├─ DependencyChain
 │       ├─ MarketContextCard
 │       └─ ExplanationCard
 └─ FooterNote
```

Keep state simple at first.
One selected watchlist item and one selected news event is enough to make the demo work.

---

## Tailwind Styling Guidance

Use utility classes to create:

- `rounded-2xl` or `rounded-3xl` for major cards
- subtle borders like `border border-white/10`
- layered surfaces with slight background differences
- `backdrop-blur` only if it genuinely improves polish
- `transition-all duration-200` for responsiveness
- spacing that feels deliberate

Avoid:
- overly bright gradients everywhere
- too many colors
- giant shadows
- tiny unreadable text

---

## Initial Placeholder Copy

### Navbar
- StockTrace
- Signal-aware investing

### Intro Panel
**Track what matters. Understand why.**  
StockTrace watches the companies you follow, detects meaningful events, and explains why they may matter before you act.

### Watchlist Section Label
**Your Watchlist**

### Signal Feed Label
**Live Signals**

### Analysis Label
**Agent Analysis**

### CTA Buttons
- Add to watchlist
- Try demo scenario
- Analyze event

### Disclaimer
**Context only — not financial advice.**

---

## Final Design Goal

StockTrace should feel like:

> a fast, intelligent AI agent experience that turns headlines into understandable context.

The judge should immediately understand:

- what the user tracks
- what happened
- how the agent reasons
- why the output is useful

If the UI makes that story obvious, the demo will feel strong even with a partially hardcoded backend.