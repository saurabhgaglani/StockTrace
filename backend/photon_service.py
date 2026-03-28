import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ALERT_PHONE = os.getenv("ALERT_PHONE_NUMBER", "")
NOTIFY_SCRIPT = Path(__file__).parent / "notify" / "notify.js"

def send_alert(symbol: str, headline: str, explanation: str):
    """Send iMessage alert via Node.js bridge (fire-and-forget)."""
    if not ALERT_PHONE:
        return
    message = f"[{symbol}] {headline}\n\n{explanation}\n\nContext only — not financial advice."
    try:
        subprocess.Popen(
            ["node", str(NOTIFY_SCRIPT)],
            env={**os.environ, "TO": ALERT_PHONE, "MESSAGE": message},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"[photon] iMessage send failed: {e}")
