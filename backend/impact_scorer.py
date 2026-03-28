def score_impact(event: dict, path: list[str]) -> dict:
    """Simple deterministic impact scoring."""
    score = 0.0

    # Graph match weight
    if path:
        score += 0.4
        # Shorter path = more direct = higher impact
        score += max(0, 0.2 - len(path) * 0.02)

    # Event type weight
    event_type = event.get("event_type", "")
    if event_type == "geopolitical":
        score += 0.25
    elif event_type == "supply_chain":
        score += 0.2
    elif event_type == "market_anomaly":
        change = abs(event.get("change_percent", 0))
        score += min(0.3, change * 0.05)

    # News source urgency
    if event.get("source") in ("gdelt", "manual-demo"):
        score += 0.1

    score = round(min(score, 1.0), 2)
    level = "high" if score >= 0.75 else "moderate" if score >= 0.35 else "low"
    return {"impact_score": score, "impact_level": level}
