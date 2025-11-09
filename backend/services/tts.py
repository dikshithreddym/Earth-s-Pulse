"""ElevenLabs Text-to-Speech service integration."""

from __future__ import annotations
import os
import httpx
from functools import lru_cache

class ElevenLabsError(Exception):
    def __init__(self, message: str, status_code: int | None = None, meta: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code or 500
        self.meta = meta or {}

    def to_dict(self):
        return {
            "error": self.message,
            "status_code": self.status_code,
            "meta": self.meta
        }

FALLBACK_MODELS = [
    "eleven_multilingual_v2",
    "eleven_monolingual_v2",
    "eleven_turbo_v2",
]

@lru_cache(maxsize=1)
def _preferred_models():
    env_model = os.getenv("ELEVENLABS_MODEL", "").strip()
    if env_model:
        return [env_model] + [m for m in FALLBACK_MODELS if m != env_model]
    return FALLBACK_MODELS

class TTSService:
    def __init__(self, api_key: str | None = None, default_voice: str | None = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        # Default to a known public voice ID if none provided
        self.default_voice = default_voice or os.getenv("ELEVENLABS_VOICE_ID") or "21m00Tcm4TlvDq8ikWAM"
        self._voice_cache: dict[str, str] = {}

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def _resolve_voice(self, voice: str, client: httpx.AsyncClient) -> str:
        # If it looks like a voice ID (24 chars, no underscore) use it directly
        if len(voice) == 24 and "_" not in voice:
            return voice
        if voice in self._voice_cache:
            return self._voice_cache[voice]
        # Requires Voices: Read permission
        r = await client.get("https://api.elevenlabs.io/v1/voices",
                             headers={"xi-api-key": self.api_key},
                             timeout=10)
        if r.status_code != 200:
            raise ElevenLabsError(
                f"Unable to list voices (status {r.status_code})",
                status_code=r.status_code,
                meta={"response": r.text}
            )
        data = r.json()
        for v in data.get("voices", []):
            if v.get("name") == voice:
                vid = v["voice_id"]
                self._voice_cache[voice] = vid
                return vid
        raise ElevenLabsError(f"Voice name '{voice}' not found; use a voice ID.",
                              status_code=404)

    async def synthesize(self, text: str, voice: str | None = None, model: str | None = None) -> bytes:
        if not self.api_key:
            raise ElevenLabsError("Missing ELEVENLABS_API_KEY", status_code=400)
        use_voice = voice or self.default_voice
        async with httpx.AsyncClient() as client:
            # Try to resolve a name to ID; if fails, fall back silently to default ID
            if not (len(use_voice) == 24 and "_" not in use_voice):
                try:
                    use_voice = await self._resolve_voice(use_voice, client)
                except ElevenLabsError:
                    use_voice = self.default_voice

            models_to_try = [model] + _preferred_models() if model else _preferred_models()
            tried: list[str] = []
            for m in models_to_try:
                if not m or m in tried:
                    continue
                tried.append(m)
                payload = {
                    "text": text,
                    "model_id": m,
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
                }
                r = await client.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{use_voice}",
                    headers={
                        "xi-api-key": self.api_key,
                        "Accept": "audio/mpeg",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=30
                )
                if r.status_code == 200:
                    return r.content
                # Parse error JSON if available
                err_json = {}
                try:
                    err_json = r.json()
                except Exception:
                    pass
                status_flag = err_json.get("detail", {}).get("status")
                # If model deprecated for free tier, continue to next
                if status_flag == "model_deprecated_free_tier":
                    continue
                raise ElevenLabsError(
                    f"TTS failed ({r.status_code}): {err_json or r.text}",
                    status_code=r.status_code,
                    meta={"model": m, "voice": use_voice}
                )
            raise ElevenLabsError(
                f"All models failed (tried: {tried})",
                status_code=500,
                meta={"tried_models": tried}
            )

tts_service = TTSService()
