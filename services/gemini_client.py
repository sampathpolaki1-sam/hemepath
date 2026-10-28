# services/gemini_client.py - High-Performance Native Gemini Client for HemePath
import os
import json
import urllib.request
import urllib.error

# API Key loaded from environment variable (set in .env locally or Vercel Environment Variables in production)
def get_api_key():
    return os.environ.get("GEMINI_API_KEY", "")
CANDIDATE_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-flash-latest"
]

def generate_medical_text(prompt, system_instruction=None, max_tokens=2500, temperature=0.6, timeout=25, response_mime_type=None):
    """
    Calls Gemini API with automatic model fallback and zero external dependencies.
    Supports markdown generation and structured JSON generation (response_mime_type='application/json').
    Returns generated text or None if all models fail.
    """
    key = get_api_key()
    if not key:
        return None

    full_prompt = prompt
    if system_instruction:
        full_prompt = f"System Instructions:\n{system_instruction}\n\nUser Request:\n{prompt}"

    gen_config = {
        "maxOutputTokens": max_tokens,
        "temperature": temperature
    }
    if response_mime_type:
        gen_config["responseMimeType"] = response_mime_type

    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }],
        "generationConfig": gen_config
    }
    encoded_payload = json.dumps(payload).encode("utf-8")

    for model_name in CANDIDATE_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
        req = urllib.request.Request(
            url,
            data=encoded_payload,
            headers={"Content-Type": "application/json"}
        )

        try:
            resp = urllib.request.urlopen(req, timeout=timeout)
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"]
        except urllib.error.HTTPError:
            # If 503 (high demand) or 404, fall through to next candidate model
            continue
        except Exception:
            continue

    return None
