import os
import json
import urllib.request
from typing import Optional

def send_discord_alert(message: str) -> bool:
    """
    Send a notification to Discord via webhook.
    Uses DISCORD_WEBHOOK_URL environment variable.
    
    Returns:
        bool: True if successful or skipped, False if it failed.
    """
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        # Fail gracefully if not set - we don't want to crash the tool
        # because a webhook is missing, but we log it to stderr.
        return True

    # Prepare the payload
    # We use a simple format, but could be expanded to use embeds
    payload = {
        "content": message,
        "username": "Scaffolding Watchdog",
        "avatar_url": "https://raw.githubusercontent.com/eriksjaastad/project-scaffolding/main/docs/assets/watchdog.png"
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            webhook_url, 
            data=data, 
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        )
        
        with urllib.request.urlopen(req) as response:
            if response.getcode() in [200, 204]:
                return True
            else:
                print(f"Warning: Discord webhook returned status {response.getcode()}")
                return False
                
    except Exception as e:
        print(f"Warning: Failed to send Discord alert: {e}")
        return False
