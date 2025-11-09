from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PostItem(BaseModel):
    id: Optional[str] = None
    city_name: str
    country: Optional[str] = None
    platform: str  # "reddit" | "twitter" | "mock"
    text: str
    url: Optional[str] = None
    author: Optional[str] = None
    score: float
    label: str
    created_at: datetime = Field(default_factory=datetime.utcnow)