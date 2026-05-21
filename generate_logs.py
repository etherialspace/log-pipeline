import json
import time
import random
import requests
from datetime import datetime, timezone

LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
SERVICES = ["auth-service", "payment-gateway", "user-profile", "search-engine"]
MESSAGES = {
    "INFO": ["User logged in", "Payment processed", "Search query executed", "Profile updated", "Email sent"],
    "WARNING": ["High memory usage detected", "API rate limit approaching", "Slow database query", "Deprecated API used"],
    "ERROR": ["Database connection failed", "Payment declined", "Null pointer exception", "Timeout accessing external service"],
    "DEBUG": ["Cache miss", "User configuration loaded", "Session token validated", "Route calculated"]
}

def generate_log():
    level = random.choice(LEVELS)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": random.choice(SERVICES),
        "message": random.choice(MESSAGES[level]),
        "latency_ms": random.randint(10, 500) if level != "ERROR" else random.randint(500, 2000),
        "trace_id": f"trace-{random.randint(10000, 99999)}"
    }

API_URL = "http://127.0.0.1:8000/logs/"

if __name__ == "__main__":
    print(f"Starting fake log generator. Sending logs to {API_URL}. Press Ctrl+C to stop.")
    try:
        while True:
            log_entry = generate_log()
            try:
                response = requests.post(API_URL, json=log_entry)
                if response.status_code == 200:
                    print(f"[{log_entry['level']}] Successfully sent log: {log_entry['trace_id']}")
                else:
                    print(f"Failed to send log. Status: {response.status_code}, Response: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"API unreachable. Cannot send log: {e}")
            time.sleep(random.uniform(0.5, 2.0))
    except KeyboardInterrupt:
        print("\nLog generation stopped.")
