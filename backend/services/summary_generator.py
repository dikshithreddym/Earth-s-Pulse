"""
Summary Generator Service
Uses OpenRouter API to generate human-readable emotional summaries
"""

import os
import httpx
from typing import List
from dotenv import load_dotenv
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from models.mood import MoodPoint
from collections import Counter

load_dotenv()

class SummaryGenerator:
    """Generates AI summaries of global emotional state"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.enabled = bool(self.api_key)
    
    async def generate_summary(self, moods: List[MoodPoint]) -> str:
        """
        Generate a human-readable summary of global emotional state
        
        Args:
            moods: List of mood points to analyze
            
        Returns:
            String summary of global emotions
        """
        if not moods:
            return "No mood data available to analyze."
        
        # If OpenRouter is not configured, use rule-based summary
        if not self.enabled:
            return self._generate_rule_based_summary(moods)
        
        # Prepare data for LLM
        summary_data = self._prepare_summary_data(moods)
        
        # Call OpenRouter API
        try:
            prompt = self._create_prompt(summary_data)
            summary = await self._call_openrouter(prompt)
            return summary
        except Exception as e:
            print(f"Error calling OpenRouter: {e}")
            # Fallback to rule-based
            return self._generate_rule_based_summary(moods)
    
    def _prepare_summary_data(self, moods: List[MoodPoint]) -> dict:
        """Prepare mood data for summary generation"""
        # Count by label
        labels = [mood.label for mood in moods]
        label_counts = Counter(labels)
        
        # Count by region (simplified: by continent)
        regions = {}
        for mood in moods:
            region = self._get_region(mood.lat, mood.lng)
            if region not in regions:
                regions[region] = {"labels": [], "count": 0}
            regions[region]["labels"].append(mood.label)
            regions[region]["count"] += 1
        
        # Calculate average scores by region
        region_scores = {}
        for mood in moods:
            region = self._get_region(mood.lat, mood.lng)
            if region not in region_scores:
                region_scores[region] = []
            region_scores[region].append(mood.score)
        
        region_avg_scores = {
            region: sum(scores) / len(scores)
            for region, scores in region_scores.items()
        }
        
        return {
            "total_points": len(moods),
            "label_distribution": dict(label_counts),
            "regions": {k: v["count"] for k, v in regions.items()},
            "region_scores": region_avg_scores
        }
    
    def _get_region(self, lat: float, lng: float) -> str:
        """Get region/continent name from coordinates"""
        # Simple region mapping
        if -50 <= lat <= 50 and -180 <= lng <= -30:
            return "North America"
        elif -50 <= lat <= 15 and -80 <= lng <= -35:
            return "South America"
        elif 35 <= lat <= 70 and -10 <= lng <= 40:
            return "Europe"
        elif 10 <= lat <= 50 and 60 <= lng <= 150:
            return "Asia"
        elif -40 <= lat <= -10 and 110 <= lng <= 155:
            return "Australia"
        elif -35 <= lat <= 35 and -20 <= lng <= 50:
            return "Africa"
        else:
            return "Other"
    
    def _create_prompt(self, data: dict) -> str:
        """Create prompt for LLM"""
        prompt = f"""Analyze the following global emotional sentiment data and write a brief, engaging summary (2-3 sentences) about the world's emotional state.

Data:
- Total data points: {data['total_points']}
- Emotion distribution: {data['label_distribution']}
- Regional distribution: {data['regions']}
- Regional average sentiment scores: {data['region_scores']}

Write a natural, human-readable summary that highlights interesting patterns, regional differences, or overall emotional trends. Be concise and engaging."""
        
        return prompt
    
    async def _call_openrouter(self, prompt: str) -> str:
        """Call OpenRouter API to generate summary"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that analyzes emotional sentiment data and writes engaging, concise summaries."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 200
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                raise Exception(f"OpenRouter API error: {response.status_code}")
    
    def _generate_rule_based_summary(self, moods: List[MoodPoint]) -> str:
        """Generate summary using rule-based logic (fallback)"""
        if not moods:
            return "No mood data available."
        
        # Count emotions
        labels = [mood.label for mood in moods]
        label_counts = Counter(labels)
        
        # Find dominant emotion
        dominant = label_counts.most_common(1)[0][0] if label_counts else "neutral"
        
        # Calculate average score
        avg_score = sum(mood.score for mood in moods) / len(moods)
        
        # Generate simple summary
        if avg_score > 0.2:
            sentiment = "positive"
        elif avg_score < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        summary = f"Based on {len(moods)} data points, the global emotional state is {sentiment}. "
        summary += f"The most common emotion is {dominant}. "
        summary += f"Average sentiment score: {avg_score:.2f}."
        
        return summary

