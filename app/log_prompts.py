# app/log_prompts.py

import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "blocked_prompts.log")

# Ensure log folder exists
os.makedirs(LOG_DIR, exist_ok=True)

def log_unsafe_prompt(prompt: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] 🚫 BLOCKED PROMPT: {prompt}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)
    print(log_line.strip())  # Also print to console
