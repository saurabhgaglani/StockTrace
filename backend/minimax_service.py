import os
import re
import httpx
from dotenv import load_dotenv

load_dotenv()

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", "MiniMax-M2.5")
API_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"

PROMPT_TEMPLATE = """Write a 1-2 sentence neutral investment alert explaining why {symbol} is affected by: "{headline}". Path: {path}. Impact: {impact_level}."""

async def generate_explanation(symbol: str, headline: str, path: list[str], impact_level: str) -> str:
    path_str = " → ".join(path) if path else "direct market exposure"
    prompt = PROMPT_TEMPLATE.format(
        symbol=symbol, headline=headline, path=path_str, impact_level=impact_level
    )
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            API_URL,
            headers={"Authorization": f"Bearer {MINIMAX_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": MINIMAX_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
            }
        )
        resp.raise_for_status()
        data = resp.json()
        try:
            message = data["choices"][0]["message"]
            # For reasoning models, content may be empty while reasoning_content has the output
            content = message.get("content") or message.get("reasoning_content") or message.get("text") or ""
            # Strip <think>...</think> blocks
            content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
            if not content:
                raise ValueError(f"Empty content in MiniMax response: {data}")
            return content
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected MiniMax response: {data}") from e
