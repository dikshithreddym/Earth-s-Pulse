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
        # Try multiple working models in order
        default_model = os.getenv("OPENROUTER_MODEL", "").strip()
        if not default_model:
            # Fallback list of known working models (as of Nov 2025)
            default_model = "qwen/qwen-2-7b-instruct:free"
        self.model = default_model
        # Alternative models to try if primary fails
        self.fallback_models = [
            "google/gemma-7b-it:free",
            "mistralai/mistral-7b-instruct:free",
            "meta-llama/llama-3.1-8b-instruct",  # Paid but cheap fallback
        ]
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

    async def generate_summary(self, mood_points: List[Any], city_name: str | None = None) -> str:
        if not mood_points:
            return "No mood data available yet."
        cache_key = self._make_cache_key(mood_points, city_name)
        if self._cache_key == cache_key and (time.time() - self._cache_time) < CACHE_TTL_SECONDS and self._cache_text:
            return self._cache_text

        agg = self._aggregate(mood_points)

        if self.openrouter_api_key:
            # Use AI summary - raise error if it fails (no fallback for production)
            text = await self._generate_ai_summary(agg, city_name)
            self._store_cache(cache_key, text)
            return text
        else:
            # No API key configured - raise error
            raise Exception("OpenRouter API key not configured. Please set OPENROUTER_API_KEY in .env file.")

    def _store_cache(self, key: str, text: str):
        self._cache_key = key
        self._cache_text = text
        self._cache_time = time.time()

    def _make_cache_key(self, mood_points: List[Any], city_name: str | None = None) -> str:
        # Include flags so changing style/visibility busts cache
        first_ts = getattr(mood_points[0], "timestamp", None)
        last_ts = getattr(mood_points[-1], "timestamp", None)
        city_key = f":city={city_name}" if city_name else ""
        return f"{len(mood_points)}:{first_ts}:{last_ts}:cities={INCLUDE_CITIES}:style={SUMMARY_STYLE}{city_key}"

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

    def _generate_fallback_summary(self, agg: Dict[str, Any], city_name: str | None = None) -> str:
        total = agg["total"]
        if total == 0:
            return "No mood data available yet."
        pos, neu, neg = agg["positive"], agg["neutral"], agg["negative"]
        def pct(n): return round((n / total) * 100, 1)
        median_score = agg.get("median_score", 0.0)
        tone = "optimistic" if pos > neg else "concerned" if neg > pos else "balanced"

        if city_name:
            # City-specific summary
            return (
                f"Emotional overview for {city_name}: Analyzed {total} recent social media posts. "
                f"Sentiment distribution shows {pct(pos)}% positive, {pct(neu)}% neutral, and {pct(neg)}% negative expressions. "
                f"The median sentiment score is {median_score}, indicating the overall emotional climate in {city_name} appears {tone}. "
                f"This reflects the current mood based on recent online discussions from the city."
            )
        
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

    def _build_prompt(self, agg: Dict[str, Any], city_name: str | None = None) -> str:
        total = agg["total"]
        pos, neu, neg = agg["positive"], agg["neutral"], agg["negative"]
        def pct(n): return round((n / total) * 100, 1) if total else 0.0
        median_score = agg.get("median_score", 0.0)
        avg_score = agg.get("avg_score", 0.0)

        style_hint = STYLE_HINTS.get(SUMMARY_STYLE, STYLE_HINTS["concise"])
        
        if city_name:
            # Enhanced city-specific prompt for Reddit data
            return (
                f"Analyze sentiment from {total} recent Reddit posts discussing {city_name}. "
                f"Sentiment distribution: {pct(pos)}% positive, {pct(neu)}% neutral, {pct(neg)}% negative. "
                f"Average sentiment: {avg_score}, Median: {median_score}. "
                f"Based on these Reddit discussions, write a natural, human-readable summary about the emotional climate "
                f"and current mood in {city_name}. Focus on what people are experiencing and feeling in the city. "
                f"Mention key themes like social life, infrastructure, work/career, relationships, or community issues "
                f"if the sentiment suggests these. Write 4-6 sentences in a narrative style. "
                f"Don't just recite statistics - tell a story about the city's current mood."
            )
        else:
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

    async def _generate_ai_summary(self, agg: Dict[str, Any], city_name: str | None = None) -> str:
        """Generate AI-powered summary using OpenRouter API with enhanced prompts and fallback models"""
        prompt = self._build_prompt(agg, city_name)
        
        # Enhanced system prompt for city summaries
        system_prompt = (
            "You are an empathetic AI that analyzes social media sentiment to understand how people feel in different cities. "
            "Your summaries should be insightful, human, and narrative-driven. Focus on the lived experiences and emotions "
            "of city residents based on their Reddit posts. Avoid being overly statistical - instead, paint a picture of "
            "the city's emotional atmosphere. Be specific about what's making people happy, anxious, or neutral."
        )
        
        # Try primary model first, then fallbacks
        models_to_try = [self.model] + [m for m in self.fallback_models if m != self.model]
        last_error = None
        
        async with httpx.AsyncClient(timeout=30) as client:
            for model_name in models_to_try:
                try:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openrouter_api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "http://localhost:8000",
                            "X-Title": "Earth's Pulse - City Sentiment Analysis"
                        },
                        json={
                            "model": model_name,
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": prompt}
                            ],
                            "max_tokens": 300,  # More tokens for detailed city summaries
                            "temperature": 0.8,  # Higher creativity for narrative summaries
                            "stop": [
                                "</s>", "[/s]", "[/INST]", "[/B_INST]", 
                                "[B_Assitant]", "<|im_end|>", "\n\n\n"
                            ]
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        raw_text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
                        logger.info(f"Successfully generated summary using model: {model_name}")
                        return self._clean(raw_text)
                    else:
                        error_data = {}
                        try:
                            error_data = response.json()
                        except:
                            pass
                        error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                        last_error = f"Model {model_name} failed: {response.status_code} - {error_msg}"
                        logger.warning(last_error)
                        # Try next model
                        continue
                        
                except Exception as e:
                    last_error = f"Model {model_name} error: {str(e)}"
                    logger.warning(last_error)
                    continue
            
            # All models failed
            logger.error(f"All OpenRouter models failed. Last error: {last_error}")
            raise Exception(f"OpenRouter API error: All models failed. Last error: {last_error}")

    def _clean(self, text: str) -> str:
        """Clean AI-generated text from model artifacts and special tokens"""
        if not text:
            return ""
        
        # Remove common model instruction tokens
        tokens_to_remove = [
            "<s>", "</s>", 
            "[/s]", "[/S]",
            "[INST]", "[/INST]",
            "[B_INST]", "[/B_INST]",
            "[B_Assitant]", "[/B_Assitant]",
            "B_INST", "/B_INST",
            "<|im_start|>", "<|im_end|>",
            "<|assistant|>", "<|user|>",
        ]
        
        for token in tokens_to_remove:
            text = text.replace(token, "")
        
        # Remove any remaining bracket tokens (like [xxx])
        import re
        text = re.sub(r'\[/?[A-Z_]+\]', '', text)
        
        # Clean up extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()


summary_generator = SummaryGenerator()

