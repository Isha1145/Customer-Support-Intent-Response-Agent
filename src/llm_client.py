"""Thin wrapper around a local Ollama server so the rest of the code doesn't
care which local model is being used."""
import json
import requests
from src import config


def generate(prompt: str, system: str = None, temperature: float = 0.2) -> str:
    payload = {
        "model": config.OLLAMA_MODEL,
        "prompt": prompt,
        "system": system or "",
        "stream": False,
        "options": {"temperature": temperature},
    }
    try:
        resp = requests.post(
            f"{config.OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=config.OLLAMA_TIMEOUT_S,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not reach Ollama at "
            f"{config.OLLAMA_HOST}. Is `ollama serve` running, and did you "
            f"`ollama pull {config.OLLAMA_MODEL}`?"
        )


def generate_json(prompt: str, system: str = None) -> dict:
    """Ask the model for JSON and parse it, tolerating markdown code fences."""
    raw = generate(prompt, system=system, temperature=0.0)
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.split("\n", 1)[-1] if cleaned.lower().startswith("json") else cleaned
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # last resort: find the first {...} block
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start != -1 and end != -1:
            return json.loads(cleaned[start:end + 1])
        raise ValueError(f"Model did not return valid JSON:\n{raw}")
