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
from collections import deque

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
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
sentiment_analyzer = SentimentAnalyzer()
social_fetcher = SocialMediaFetcher()
db_service = DatabaseService()
summary_generator = SummaryGenerator()


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await db_service.connect()
    # Create a queue for streaming posts and start background consumers/producers
    app.state.post_queue = asyncio.Queue()
    # Keep a small history of raw posts for debugging
    app.state.recent_raw_posts = deque(maxlen=200)

    # Start streaming threads that push raw posts into the queue
    try:
        social_fetcher.start_streams(app.state.post_queue, loop=asyncio.get_event_loop())
    except Exception as e:
        print(f"⚠️ Could not start streams: {e}")

    # consumer task: analyze and insert into DB
    async def _consume_queue(q: asyncio.Queue):
        print("🔁 Starting post consumer task")
        while True:
            post = await q.get()
            try:
                # keep a recent raw copy for debug endpoint
                try:
                    app.state.recent_raw_posts.append(post)
                except Exception:
                    pass
                # Analyze sentiment (synchronous analyze)
                sentiment_result = sentiment_analyzer.analyze(post.get("text", ""))

                mood_point = MoodPoint(
                    lat=post.get("lat") if post.get("lat") is not None else 0.0,
                    lng=post.get("lng") if post.get("lng") is not None else 0.0,
                    label=sentiment_result.get("label", "neutral"),
                    score=sentiment_result.get("score", 0.0),
                    source=post.get("source", "unknown"),
                    text=post.get("text", "")[:200],
                    timestamp=post.get("timestamp") or datetime.utcnow()
                )

                # Insert to DB
                await db_service.insert_moods([mood_point])
            except Exception as e:
                print(f"Error consuming post: {e}")
            finally:
                q.task_done()

    app.state.consumer_task = asyncio.create_task(_consume_queue(app.state.post_queue))
    print("✅ Backend services initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    # Cancel consumer task if running
    try:
        if getattr(app.state, 'consumer_task', None):
            app.state.consumer_task.cancel()
            await app.state.consumer_task
    except Exception:
        pass

    await db_service.disconnect()
    print("✅ Backend services shut down")


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
    max_score: Optional[float] = None
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
        return moods
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching moods: {str(e)}")


@app.post("/api/moods/refresh")
async def refresh_moods():
    """
    Manually trigger data refresh from social media APIs
    Fetches new posts, analyzes sentiment, and stores in database
    """
    try:
        # Fetch posts from social media
        posts = await social_fetcher.fetch_recent_posts(limit=50)
        
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
                    source=post["source"],
                    text=post["text"][:200],  # Truncate for storage
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


@app.get("/api/debug/raw_posts")
async def debug_raw_posts(limit: Optional[int] = 20):
    """Return the most recent raw posts captured by the streaming producers (pre-analysis)."""
    try:
        recent = list(getattr(app.state, 'recent_raw_posts', []))
        return recent[-limit:]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error returning debug posts: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

