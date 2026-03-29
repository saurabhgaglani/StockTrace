import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ALERT_PHONE = os.getenv("ALERT_PHONE_NUMBER", "")
NOTIFY_SCRIPT = Path(__file__).parent / "notify" / "notify.js"

def send_alert(symbol: str, headline: str, explanation: str):
    """Send iMessage alert via Node.js bridge (fire-and-forget)."""
    print("HEREEE")
    if not ALERT_PHONE:
        return
    message = f"[{symbol}] {headline}\n\n{explanation}\n\nContext only — not financial advice."
    try:
        # Set the working directory to the location of the notify script
        # so that it can find its node_modules.
        script_dir = NOTIFY_SCRIPT.parent
        p = subprocess.Popen(
            ["node", str(NOTIFY_SCRIPT)],
            env={**os.environ, "TO": ALERT_PHONE, "MESSAGE": message},
            cwd=script_dir,  # <-- This is the critical fix
            stdout=subprocess.PIPE, # Capture output
            stderr=subprocess.PIPE, # Capture errors
        )
        # We use communicate() to wait for the process to finish and get the output.
        # In a fire-and-forget scenario, you could also just let it run.
        stdout, stderr = p.communicate()

        if p.returncode != 0:
            print(f"[photon] Node.js script failed with code {p.returncode}:")
            if stdout:
                print(f"--- STDOUT ---\n{stdout.decode().strip()}")
            if stderr:
                print(f"--- STDERR ---\n{stderr.decode().strip()}")

    except Exception as e:
        print(f"[photon] Failed to execute Node.js script: {e}")
