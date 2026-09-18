from __future__ import annotations

import json

import httpx

from src.config import get_settings
from src.models.schemas import ChatResponse


class LLMClient:
    """Optional OpenAI polish layer. System works fully without it."""

    def polish(self, draft: ChatResponse, user_message: str | None) -> str:
        settings = get_settings()
        if not settings.llm_enabled:
            return draft.answer

        system = (
            "You are an AI environmental scientist for Darukaa.Earth. "
            "Rewrite the provided structured draft into a clear, rigorous response. "
            "Do NOT invent new numerical claims or citations. Preserve recommendations, "
            "metrics, time horizons, confidence, and references. Keep multi-metric reasoning."
        )
        payload = {
            "model": settings.openai_model,
            "messages": [
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": (
                        f"User message: {user_message or ''}\n\n"
                        f"Structured draft JSON:\n{draft.model_dump_json()}"
                    ),
                },
            ],
            "temperature": 0.2,
        }
        try:
            with httpx.Client(timeout=45.0) as client:
                resp = client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    content=json.dumps(payload),
                )
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return draft.answer
