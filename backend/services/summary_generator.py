"""
Generates an aggregated textual summary of current mood points.
Uses OpenRouter (LLM) if OPENROUTER_API_KEY is set; otherwise falls back
to deterministic rule-based summary. Includes simple time-based cache.
"""

from __future__ import annotations
import os
import time
import statistics
from typing import List, Dict, Any
import httpx
import logging

logger = logging.getLogger("summary")

# Use the same thresholds as the Map Legend; configurable via env if needed
POS_THRESHOLD = float(os.getenv("SENTIMENT_POS_THRESHOLD", "0.3"))
NEG_THRESHOLD = float(os.getenv("SENTIMENT_NEG_THRESHOLD", "-0.3"))

# New: control city mentions and summary style
INCLUDE_CITIES = os.getenv("SUMMARY_INCLUDE_CITIES", "false").strip().lower() == "true"
SUMMARY_STYLE = os.getenv("SUMMARY_STYLE", "concise").strip().lower()
STYLE_HINTS = {
    "concise": "Be succinct (3–5 sentences).",
    "trend": "Emphasize short-term movements, momentum, and balance shifts.",
    "narrative": "Use a calm, human tone; avoid statistics-heavy phrasing.",
}

CACHE_TTL_SECONDS = int(os.getenv("SUMMARY_CACHE_TTL", "45"))  # avoid regenerating too often

class SummaryGenerator:
    def __init__(self):
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "").strip() or "openrouter/llama-3.1-8b-instruct:free"
        self._cache_text: str | None = None
        self._cache_key: str | None = None
        self._cache_time: float = 0.0

    async def get_latest_summary(self, db_service) -> Dict[str, Any]:
        """
        Helper for /api/summary/audio to reuse existing summary if cached.
        """
        recent = await db_service.get_moods(limit=500)
        unique = {}
        for m in recent:
            city = getattr(m, "city_name", None)
            if city and city not in unique:
                unique[city] = m
        deduped = list(unique.values())
        summary_text = await self.generate_summary(deduped)
        return {"text": summary_text, "points": len(deduped)}

    async def generate_summary(self, mood_points: List[Any]) -> str:
        if not mood_points:
            return "No mood data available yet."
        cache_key = self._make_cache_key(mood_points)
        if self._cache_key == cache_key and (time.time() - self._cache_time) < CACHE_TTL_SECONDS and self._cache_text:
            return self._cache_text

        agg = self._aggregate(mood_points)

        if self.openrouter_api_key:
            try:
                text = await self._generate_ai_summary(agg)
                self._store_cache(cache_key, text)
                return text
            except Exception as e:
                logger.warning(f"AI summary failed, falling back: {e}")

        text = self._generate_fallback_summary(agg)
        self._store_cache(cache_key, text)
        return text

    def _store_cache(self, key: str, text: str):
        self._cache_key = key
        self._cache_text = text
        self._cache_time = time.time()

    def _make_cache_key(self, mood_points: List[Any]) -> str:
        # Include flags so changing style/visibility busts cache
        first_ts = getattr(mood_points[0], "timestamp", None)
        last_ts = getattr(mood_points[-1], "timestamp", None)
        return f"{len(mood_points)}:{first_ts}:{last_ts}:cities={INCLUDE_CITIES}:style={SUMMARY_STYLE}"

    def _aggregate(self, mood_points: List[Any]) -> Dict[str, Any]:
        # Extract fields
        scores = [getattr(m, "score", None) for m in mood_points]
        cities = [getattr(m, "city_name", None) for m in mood_points if getattr(m, "city_name", None)]

        # Distribution by score thresholds (match UI legend)
        total = len(mood_points)
        pos = sum(1 for s in scores if s is not None and s > POS_THRESHOLD)
        neg = sum(1 for s in scores if s is not None and s < NEG_THRESHOLD)
        neu = total - pos - neg

        # Aggregates
        valid_scores = [s for s in scores if s is not None]
        avg_score = round(sum(valid_scores) / len(valid_scores), 3) if valid_scores else 0.0
        median_score = round(statistics.median(valid_scores), 3) if valid_scores else 0.0

        return {
            "total": total,
            "positive": pos,
            "neutral": neu,
            "negative": neg,
            "scores": valid_scores,
            "avg_score": avg_score,
            "median_score": median_score,
            "cities": cities,  # kept for optional use
        }

    def _generate_fallback_summary(self, agg: Dict[str, Any]) -> str:
        total = agg["total"]
        if total == 0:
            return "No mood data available yet."
        pos, neu, neg = agg["positive"], agg["neutral"], agg["negative"]
        def pct(n): return round((n / total) * 100, 1)
        median_score = agg.get("median_score", 0.0)
        tone = "optimistic" if pos > neg else "concerned" if neg > pos else "balanced"

        if INCLUDE_CITIES:
            # Keep a short sample when enabled
            sample_cities = ", ".join(agg["cities"][:4]) if agg["cities"] else "various regions"
            where = f"across {sample_cities}"
        else:
            uniq_city_count = len(set(agg["cities"])) if agg["cities"] else 0
            where = f"across {uniq_city_count} cities worldwide" if uniq_city_count else "across multiple regions worldwide"

        return (
            f"Global emotional overview: {total} recent mood points {where}. "
            f"Positive {pct(pos)}%, Neutral {pct(neu)}%, Negative {pct(neg)}%. "
            f"Median sentiment score {median_score}. Emotional climate appears {tone}."
        )

    def _build_prompt(self, agg: Dict[str, Any]) -> str:
        total = agg["total"]
        pos, neu, neg = agg["positive"], agg["neutral"], agg["negative"]
        def pct(n): return round((n / total) * 100, 1) if total else 0.0
        median_score = agg.get("median_score", 0.0)

        style_hint = STYLE_HINTS.get(SUMMARY_STYLE, STYLE_HINTS["concise"])
        location_rule = (
            "Do not mention specific city or country names; speak at a global level."
            if not INCLUDE_CITIES else
            "You may mention at most 3 representative cities."
        )

        return (
            f"Data window: {total} mood points using score thresholds "
            f"(>{POS_THRESHOLD} positive, <{NEG_THRESHOLD} negative). "
            f"Distribution: Positive {pct(pos)}%, Neutral {pct(neu)}%, Negative {pct(neg)}%. "
            f"Median score: {median_score}. {location_rule} "
            f"{style_hint} Write one cohesive paragraph; no bullet lists."
        )

    def _clean(self, text: str) -> str:
        if not text:
            return ""
        for token in ["<s>", "</s>", "[/s]", "[/S]"]:
            text = text.replace(token, "")
        return text.strip()


summary_generator = SummaryGenerator()

