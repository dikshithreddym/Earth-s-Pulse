"""
Script to seed initial data for testing
Run this to populate the database with sample mood data
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.database import DatabaseService
from services.sentiment_analyzer import SentimentAnalyzer
from models.mood import MoodPoint
from datetime import datetime
import random

async def seed_data():
    """Seed database with sample mood data"""
    db = DatabaseService()
    analyzer = SentimentAnalyzer()
    
    await db.connect()
    
    # Sample texts with known sentiments
    sample_texts = [
        ("Feeling great about the new project! Excited to see where this goes.", 0.7),
        ("Stressed about the deadline tomorrow. Need to finish everything.", -0.6),
        ("Beautiful weather today. Perfect for a walk in the park.", 0.5),
        ("Anxious about the upcoming exam. Hope I studied enough.", -0.5),
        ("Just got promoted! This is amazing news!", 0.9),
        ("Traffic is terrible today. Going to be late for the meeting.", -0.4),
        ("Love spending time with family. These moments are precious.", 0.8),
        ("Worried about climate change. We need to act now.", -0.3),
        ("Grateful for all the support from friends and colleagues.", 0.6),
        ("Frustrated with the slow internet connection.", -0.5),
    ]
    
    # Major cities around the world
    cities = [
        (40.7128, -74.0060, "New York"),
        (34.0522, -118.2437, "Los Angeles"),
        (51.5074, -0.1278, "London"),
        (35.6762, 139.6503, "Tokyo"),
        (-33.8688, 151.2093, "Sydney"),
        (28.6139, 77.2090, "Delhi"),
        (-23.5505, -46.6333, "São Paulo"),
        (55.7558, 37.6173, "Moscow"),
        (48.8566, 2.3522, "Paris"),
        (39.9042, 116.4074, "Beijing"),
    ]
    
    mood_points = []
    
    for i in range(50):  # Create 50 sample points
        text, expected_score = random.choice(sample_texts)
        lat, lng, city = random.choice(cities)
        source = random.choice(["reddit", "twitter"])
        
        # Analyze sentiment
        result = analyzer.analyze(text)
        
        mood_point = MoodPoint(
            lat=lat + random.uniform(-5, 5),  # Add some variation
            lng=lng + random.uniform(-5, 5),
            label=result["label"],
            score=result["score"],
            source=source,
            text=text,
            timestamp=datetime.utcnow()
        )
        
        mood_points.append(mood_point)
    
    # Insert into database
    await db.insert_moods(mood_points)
    print(f"✅ Seeded {len(mood_points)} mood points")
    
    # Show statistics
    stats = await db.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"Total points: {stats['total_points']}")
    print(f"By source: {stats['by_source']}")
    print(f"By label: {stats['by_label']}")
    print(f"Average score: {stats['average_score']:.3f}")
    
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(seed_data())

