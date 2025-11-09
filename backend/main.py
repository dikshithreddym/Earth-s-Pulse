"""
FastAPI Backend for Earth's Pulse
Main application entry point with API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Optional
import asyncio

from services.sentiment_analyzer import SentimentAnalyzer
from services.social_fetcher import SocialMediaFetcher
from services.database import DatabaseService
from services.summary_generator import SummaryGenerator
from models.mood import MoodPoint
from data.cities_200 import CITIES_200
import random

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Earth's Pulse API",
    description="Real-time emotional sentiment analysis from social media",
    version="1.0.0"
)

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
sentiment_analyzer = SentimentAnalyzer()
social_fetcher = SocialMediaFetcher()
db_service = DatabaseService()
summary_generator = SummaryGenerator()
background_task_handle = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await db_service.connect()
    print("✅ Backend services initialized")

    # Start background refresh task (Reddit-only, city-specific) if enabled
    try:
        enable_bg = os.getenv("ENABLE_BACKGROUND_REFRESH", "true").lower() == "true"
        interval_min = int(os.getenv("REFRESH_INTERVAL_MINUTES", "5"))
        if enable_bg and interval_min > 0:
            async def _background_refresh_loop():
                while True:
                    try:
                        # Fetch one post per city (Reddit-only)
                        posts = await social_fetcher.fetch_reddit_city_posts(CITIES_200, per_city=1)

                        mood_points = []
                        for post in posts:
                            try:
                                sentiment_result = sentiment_analyzer.analyze(post["text"])
                                mood = MoodPoint(
                                    lat=post["lat"],
                                    lng=post["lng"],
                                    label=sentiment_result["label"],
                                    score=sentiment_result["score"],
                                    source="reddit",
                                    text=post["text"][:200],
                                    city_name=post.get("city_name"),
                                    timestamp=datetime.utcnow(),
                                )
                                mood_points.append(mood)
                            except Exception as e:
                                print(f"Background analyze error: {e}")
                        if mood_points:
                            await db_service.insert_moods(mood_points)
                            print(f"🟢 Background refresh: inserted {len(mood_points)} points")
                    except Exception as e:
                        print(f"Background refresh error: {e}")

                    await asyncio.sleep(max(60, interval_min * 60))

            global background_task_handle
            background_task_handle = asyncio.create_task(_background_refresh_loop())
            print(f"🕒 Background refresh enabled (every {interval_min} min)")
    except Exception as e:
        print(f"Failed to start background refresh: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await db_service.disconnect()
    print("✅ Backend services shut down")
    global background_task_handle
    if background_task_handle:
        background_task_handle.cancel()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🌍 Earth's Pulse API",
        "version": "1.0.0",
        "endpoints": {
            "moods": "/api/moods",
            "summary": "/api/summary",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": await db_service.check_connection(),
            "sentiment_analyzer": sentiment_analyzer.is_ready(),
            "social_fetcher": social_fetcher.is_ready()
        }
    }


@app.get("/api/moods", response_model=List[MoodPoint])
async def get_moods(
    limit: Optional[int] = 100,
    source: Optional[str] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    only_city: Optional[bool] = False,
    unique_per_city: Optional[bool] = False
):
    """
    Get mood data points from database
    
    Query parameters:
    - limit: Maximum number of points to return (default: 100)
    - source: Filter by source ('reddit' or 'twitter')
    - min_score: Minimum sentiment score (-1 to 1)
    - max_score: Maximum sentiment score (-1 to 1)
    """
    try:
        moods = await db_service.get_moods(
            limit=limit,
            source=source,
            min_score=min_score,
            max_score=max_score
        )

        # Optionally filter to only records that have a city_name
        if only_city:
            moods = [m for m in moods if getattr(m, "city_name", None)]

        # Optionally dedupe so we return at most one (latest) per city
        if unique_per_city:
            seen = set()
            unique: List[MoodPoint] = []
            for m in moods:
                name = getattr(m, "city_name", None)
                if not name:
                    continue
                if name not in seen:
                    unique.append(m)
                    seen.add(name)
            moods = unique

        return moods
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching moods: {str(e)}")


@app.post("/api/moods/refresh")
async def refresh_moods(mode: Optional[str] = "city", reddit_only: bool = True):
    """
    Manually trigger data refresh from social media APIs
    Fetches new posts, analyzes sentiment, and stores in database
    """
    try:
        # Fetch posts from social media
        if mode == "city":
            # One post per curated city (Reddit-only)
            posts = await social_fetcher.fetch_reddit_city_posts(CITIES_200, per_city=1)
        else:
            posts = await social_fetcher.fetch_recent_posts(limit=50, reddit_only=reddit_only)
        
        if not posts:
            return {
                "message": "No new posts fetched",
                "count": 0
            }
        
        # Analyze sentiment for each post
        mood_points = []
        for post in posts:
            try:
                sentiment_result = sentiment_analyzer.analyze(post["text"])
                
                mood_point = MoodPoint(
                    lat=post["lat"],
                    lng=post["lng"],
                    label=sentiment_result["label"],
                    score=sentiment_result["score"],
                    source=post.get("source", "reddit"),
                    text=post["text"][:200],  # Truncate for storage
                    city_name=post.get("city_name"),
                    timestamp=datetime.utcnow()
                )
                
                mood_points.append(mood_point)
            except Exception as e:
                print(f"Error analyzing post: {e}")
                continue
        
        # Store in database
        if mood_points:
            await db_service.insert_moods(mood_points)
        
        return {
            "message": "Moods refreshed successfully",
            "count": len(mood_points),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing moods: {str(e)}")


@app.get("/api/summary")
async def get_summary():
    """
    Get AI-generated global emotional summary
    Analyzes recent mood data and generates a human-readable summary
    """
    try:
        # Get recent moods for analysis
        recent_moods = await db_service.get_moods(limit=500)
        
        if not recent_moods:
            return {
                "summary": "No mood data available yet. Please refresh the data.",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Generate summary using LLM
        summary = await summary_generator.generate_summary(recent_moods)
        
        return {
            "summary": summary,
            "timestamp": datetime.utcnow().isoformat(),
            "data_points": len(recent_moods)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@app.get("/api/stats")
async def get_stats():
    """Get statistics about mood data"""
    try:
        stats = await db_service.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")


@app.post("/api/dev/seed")
async def dev_seed(force_clear: bool = False):
    """Development helper: seed the curated cities into the running server's database.

    This endpoint is intentionally development-only. It will insert one MoodPoint per city
    from `backend/data/cities_100.py` using the server's `db_service` and `sentiment_analyzer`.
    """
    # Only allow in development environment for safety
    if os.getenv("ENVIRONMENT", "development") != "development":
        raise HTTPException(status_code=403, detail="Seeding only allowed in development environment")

    try:
        if force_clear:
            # Clear existing data
            if db_service.client and db_service.collection:
                await db_service.collection.delete_many({})
            else:
                db_service._in_memory_storage = []

        sample_texts = [
            "Feeling great about the new project! Excited to see where this goes.",
            "Stressed about the deadline tomorrow. Need to finish everything.",
            "Beautiful weather today. Perfect for a walk in the park.",
            "Anxious about the upcoming exam. Hope I studied enough.",
            "Just got promoted! This is amazing news!",
            "Traffic is terrible today. Going to be late for the meeting.",
            "Love spending time with family. These moments are precious.",
            "Worried about climate change. We need to act now.",
            "Grateful for all the support from friends and colleagues.",
            "Frustrated with the slow internet connection.",
        ]

        mood_points = []
        for city in CITIES_200:
            text = random.choice(sample_texts)
            source = random.choice(["reddit", "twitter"])
            result = sentiment_analyzer.analyze(text)

            mood = MoodPoint(
                lat=city["lat"],
                lng=city["lng"],
                label=result["label"],
                score=result["score"],
                source=source,
                text=f"{text} — seeded for {city['name']}",
                city_name=city["name"],
                timestamp=datetime.utcnow()
            )
            mood_points.append(mood)

        if mood_points:
            await db_service.insert_moods(mood_points)

        stats = await db_service.get_statistics()
        return {"message": "Seeded curated cities", "inserted": len(mood_points), "stats": stats}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error seeding data: {e}")


@app.post("/api/dev/clear")
async def dev_clear():
    """Development helper: clear all mood data from the server (DB or in-memory)."""
    if os.getenv("ENVIRONMENT", "development") != "development":
        raise HTTPException(status_code=403, detail="Clearing only allowed in development environment")

    try:
        if db_service.client and db_service.collection:
            await db_service.collection.delete_many({})
        else:
            db_service._in_memory_storage = []
        return {"message": "Cleared mood data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

