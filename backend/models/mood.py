"""
Data models for mood points
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MoodPoint(BaseModel):
    """Represents a single mood/sentiment data point"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    lng: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")
    label: str = Field(..., description="Emotion label (e.g., 'joyful', 'anxious', 'neutral')")
    score: float = Field(..., ge=-1, le=1, description="Sentiment score (-1 to 1)")
    source: str = Field(..., description="Data source ('reddit' or 'twitter')")
    text: Optional[str] = Field(None, description="Original text snippet")
    city_name: Optional[str] = Field(None, description="Optional resolved city name")
    timestamp: Optional[datetime] = Field(None, description="When the data was collected")
    is_fallback: Optional[bool] = Field(False, description="Whether this text was generated or fallback instead of a real fetched post")
    country: Optional[str] = Field(None, description="Optional resolved country name")
    platform: Optional[str] = Field(None, description="Platform of the original post (e.g., 'reddit', 'twitter')")
    post_text: Optional[str] = Field(None, description="Text of the original post")
    post_url: Optional[str] = Field(None, description="URL of the original post")
    post_author: Optional[str] = Field(None, description="Author of the original post")
    post_id: Optional[str] = Field(None, description="ID of the original post")
    
    class Config:
        json_schema_extra = {
            "example": {
                "lat": 40.7128,
                "lng": -74.0060,
                "label": "anxious",
                "score": -0.6,
                "source": "reddit",
                "text": "Feeling stressed about work...",
                "city_name": "New York, USA",
                "is_fallback": False,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

