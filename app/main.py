from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.safety_checker import is_prompt_safe
from app.log_prompts import log_unsafe_prompt
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"  # You can change this if needed

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask")
def ask(request: PromptRequest):
    print("✅ /ask endpoint hit")
    print("📩 Prompt received:", request.prompt)

    if not is_prompt_safe(request.prompt):
        print("🚫 Prompt blocked by safety checker")
        log_unsafe_prompt(request.prompt)
        return {"status": "blocked", "message": "Prompt blocked due to safety concerns."}

    try:
        print("📡 Sending request to Ollama API...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": request.prompt,
                "stream": False
            }
        )
        print("✅ Ollama responded:", response.status_code)
        data = response.json()
        return {"status": "success", "response": data.get("response", "")}
    except Exception as e:
        print("❌ Error talking to Ollama:", e)
        return {"status": "error", "message": str(e)}
