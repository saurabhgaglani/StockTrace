const API = "http://localhost:8000";

export const fetchWatchlist = (userId) =>
  fetch(`${API}/watchlist/${userId}`).then((r) => r.json());

export const addToWatchlist = (userId, symbol) =>
  fetch(`${API}/watchlist`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, symbol }),
  }).then((r) => r.json());

export const fetchEvents = (symbol) =>
  fetch(`${API}/events${symbol ? `?symbol=${symbol}` : ""}`).then((r) => r.json());

export const fetchAnalysis = (symbol, eventId) =>
  fetch(`${API}/analysis?symbol=${symbol}&event_id=${eventId}`).then((r) => r.json());

export const triggerTestEvent = (payload) =>
  fetch(`${API}/events/test`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).then((r) => r.json());
