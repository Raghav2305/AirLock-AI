# app/safety_checker.py

BLOCKLIST = [
    "how to build a bomb",
    "kill",
    "explosives",
    "child abuse",
    "hack into",
    "terrorist",
    "buy drugs",
    "create virus",
    "necrophilia",
    "pedophilia"
]

def is_prompt_safe(prompt: str) -> bool:
    lowered_prompt = prompt.lower()
    for term in BLOCKLIST:
        if term in lowered_prompt:
            return False
    return True
