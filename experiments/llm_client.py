"""Minimal LLM client for DeepSeek + OpenAI-compatible APIs."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-pro"
DEFAULT_DEEPSEEK_MODELS = ["deepseek-v4-flash", "deepseek-v4-pro"]

PROVIDERS = {
    "deepseek": {
        "url": "https://api.deepseek.com/chat/completions",
        "env": "DEEPSEEK_API_KEY",
    },
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "env": "OPENAI_API_KEY",
    },
}


def load_env() -> None:
    for p in (ROOT / ".env", ROOT / "experiments" / ".env"):
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def chat(
    system: str,
    user: str,
    model: str,
    *,
    provider: str = "deepseek",
    temperature: float = 0.4,
    timeout: int = 600,
) -> str:
    load_env()
    cfg = PROVIDERS.get(provider)
    if not cfg:
        raise ValueError(f"Unknown provider: {provider}")

    key = os.environ.get(cfg["env"])
    if not key:
        raise SystemExit(f"{cfg['env']} not set in .env")

    base_url = os.environ.get(f"{provider.upper()}_BASE_URL", cfg["url"])

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
    }
    req = urllib.request.Request(
        base_url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"API error {e.code}: {err}") from e

    return data["choices"][0]["message"]["content"]


def model_slug(model: str) -> str:
    return model.replace("/", "-").replace(":", "-")
