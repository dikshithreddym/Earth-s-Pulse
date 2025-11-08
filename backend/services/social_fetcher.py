"""
Social Media Data Fetcher
Fetches posts from Reddit and Twitter with location data
"""

import os
import praw
import random
import asyncio
import threading
import time
import requests
from collections import deque
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class SocialMediaFetcher:
    """Fetches posts from social media platforms"""
    
    def __init__(self):
        self.reddit_client = None
        self.twitter_client = None
        # Recent IDs for deduplication (in-memory)
        self._recent_ids = set()
        self._recent_ids_queue = deque(maxlen=5000)
        # Optional geocoder config
        self.geocoder_enabled = os.getenv("ENABLE_GEOCODER", "false").lower() in ("1", "true", "yes")
        self.geocoder_url = os.getenv("GEOCODER_URL", "https://nominatim.openstreetmap.org/search")
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize Reddit and Twitter API clients"""
        # Reddit (PRAW)
        reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        reddit_secret = os.getenv("REDDIT_CLIENT_SECRET")
        reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "EarthPulse/1.0")
        
        if reddit_client_id and reddit_secret:
            try:
                self.reddit_client = praw.Reddit(
                    client_id=reddit_client_id,
                    client_secret=reddit_secret,
                    user_agent=reddit_user_agent
                )
                print("✅ Reddit client initialized")
            except Exception as e:
                print(f"⚠️ Error initializing Reddit: {e}")
        
        # Twitter (Tweepy)
        twitter_bearer = os.getenv("TWITTER_BEARER_TOKEN")
        if twitter_bearer:
            try:
                self.twitter_client = tweepy.Client(bearer_token=twitter_bearer)
                print("✅ Twitter client initialized")
            except Exception as e:
                print(f"⚠️ Error initializing Twitter: {e}")
    
    def is_ready(self) -> bool:
        """Check if at least one social media client is ready"""
        return self.reddit_client is not None or self.twitter_client is not None

    # --- Streaming / polling helpers -------------------------------------------------
    def start_streams(self, queue: asyncio.Queue, loop: Optional[asyncio.AbstractEventLoop] = None,
                      subreddits: Optional[list] = None, twitter_rules: Optional[list] = None):
        """
        Start background threads to stream Reddit comments and Twitter tweets.

        - queue: asyncio.Queue used to push raw post dicts into the async consumer
        - loop: event loop used to schedule queue.put_nowait from threads; defaults to asyncio.get_event_loop()
        - subreddits: list of subreddit names to stream (default: ['news','worldnews'])
        - twitter_rules: list of streaming rules for Twitter (strings)
        """
        loop = loop or asyncio.get_event_loop()

        # Start Reddit stream thread
        if self.reddit_client:
            subs = subreddits or ["news", "worldnews"]
            t = threading.Thread(target=self._reddit_stream_thread, args=(subs, queue, loop), daemon=True)
            t.start()
            print(f"✅ Started Reddit stream thread for: {subs}")

        # Start Twitter stream thread
        if self.twitter_client:
            rules = twitter_rules or ["lang:en -is:retweet"]
            t2 = threading.Thread(target=self._twitter_stream_thread, args=(rules, queue, loop), daemon=True)
            t2.start()
            print(f"✅ Started Twitter stream thread with rules: {rules}")

    def _reddit_stream_thread(self, subreddits: list, queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
        """Background thread: stream new Reddit comments and push to asyncio queue."""
        try:
            # Combine subreddits
            sub_names = "+".join(subreddits)
            subreddit = self.reddit_client.subreddit(sub_names)
            for comment in subreddit.stream.comments(skip_existing=True):
                try:
                    post = {
                        "id": getattr(comment, 'id', None),
                        "text": getattr(comment, 'body', '')[:1000],
                        "lat": None,
                        "lng": None,
                        "source": "reddit",
                        "timestamp": datetime.utcfromtimestamp(getattr(comment, 'created_utc', time.time()))
                    }
                    # push into asyncio queue from thread
                    loop.call_soon_threadsafe(queue.put_nowait, post)
                except Exception as e:
                    print(f"Error processing reddit comment in stream: {e}")
        except Exception as e:
            print(f"Reddit stream thread crashed: {e}")

    def _twitter_stream_thread(self, rules: list, queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
        """Background thread: start Tweepy StreamingClient and push matched tweets to the queue."""
        try:
            # Create a local StreamingClient subclass to handle tweets
            bearer = os.getenv("TWITTER_BEARER_TOKEN")
            if not bearer:
                print("⚠️ No TWITTER_BEARER_TOKEN found, skipping twitter stream")
                return

            # Import inside thread to avoid issues if tweepy isn't available at module import
            import tweepy as _tweepy

            class _LocalStream(_tweepy.StreamingClient):
                def __init__(self, bearer_token, q, loop):
                    super().__init__(bearer_token)
                    self._q = q
                    self._loop = loop

                def on_connect(self):
                    print("✅ Connected to Twitter stream")

                def on_tweet(self, tweet):
                    try:
                        post = {
                            "id": getattr(tweet, 'id', None),
                            "text": getattr(tweet, 'text', '')[:1000],
                            "lat": None,
                            "lng": None,
                            "source": "twitter",
                            "timestamp": getattr(tweet, 'created_at', datetime.utcnow())
                        }
                        self._loop.call_soon_threadsafe(self._q.put_nowait, post)
                    except Exception as e:
                        print(f"Error in twitter on_tweet: {e}")

                def on_errors(self, errors):
                    print("Twitter stream error:", errors)

            stream = _LocalStream(bearer, queue, loop)

            # Delete old rules and set new ones
            try:
                existing = stream.get_rules()
                if existing and getattr(existing, 'data', None):
                    ids = [r.id for r in existing.data]
                    stream.delete_rules(ids)
            except Exception:
                pass

            for r in rules:
                try:
                    stream.add_rules(_tweepy.StreamRule(r))
                except Exception as e:
                    print(f"Could not add twitter rule {r}: {e}")

            # Start the stream (blocks inside thread)
            stream.filter(tweet_fields=["created_at", "geo", "text"], expansions=["geo.place_id"])
        except Exception as e:
            print(f"Twitter stream thread crashed: {e}")
    
    async def fetch_recent_posts(self, limit: int = 50) -> List[Dict]:
        """
        Fetch recent posts from all available social media platforms
        
        Args:
            limit: Maximum number of posts to fetch
            
        Returns:
            List of post dictionaries with text, location, and source
        """
        posts = []
        
        # Fetch from Reddit
        if self.reddit_client:
            try:
                reddit_posts = await self._fetch_reddit_posts(limit // 2)
                posts.extend(reddit_posts)
            except Exception as e:
                print(f"Error fetching Reddit posts: {e}")
        
        # Fetch from Twitter
        if self.twitter_client:
            try:
                twitter_posts = await self._fetch_twitter_posts(limit // 2)
                posts.extend(twitter_posts)
            except Exception as e:
                print(f"Error fetching Twitter posts: {e}")
        
        # If no API clients available, use mock data
        if not posts:
            posts = self._generate_mock_posts(limit)
        
        return posts[:limit]
    
    async def _fetch_reddit_posts(self, limit: int) -> List[Dict]:
        """Fetch posts from Reddit"""
        posts = []
        
        try:
            # Fetch from popular subreddits
            subreddits = ["worldnews", "news", "todayilearned", "mildlyinteresting", "Showerthoughts"]
            
            for subreddit_name in subreddits[:2]:  # Limit to avoid rate limits
                subreddit = self.reddit_client.subreddit(subreddit_name)
                
                for submission in subreddit.hot(limit=limit // len(subreddits[:2])):
                    # Extract text (title + selftext)
                    text = submission.title
                    if hasattr(submission, 'selftext') and submission.selftext:
                        text += " " + submission.selftext
                    
                    # Get location (mock for now - Reddit doesn't provide location)
                    # In production, you'd use geocoding or user profile data
                    lat, lng = self._get_random_location()
                    
                    posts.append({
                        "text": text[:500],  # Limit text length
                        "lat": lat,
                        "lng": lng,
                        "source": "reddit",
                        "timestamp": datetime.utcnow()
                    })
                    
                    if len(posts) >= limit:
                        break
                
                if len(posts) >= limit:
                    break
        except Exception as e:
            print(f"Error in Reddit fetch: {e}")
        
        return posts
    
    async def _fetch_twitter_posts(self, limit: int) -> List[Dict]:
        """Fetch posts from Twitter/X"""
        posts = []
        
        try:
            # Search for recent tweets (example query)
            query = "lang:en -is:retweet"  # English, not retweets
            
            tweets = self.twitter_client.search_recent_tweets(
                query=query,
                max_results=min(limit, 100),  # Twitter API limit
                tweet_fields=["created_at", "text", "geo"]
            )
            
            if tweets.data:
                for tweet in tweets.data:
                    text = tweet.text
                    
                    # Try to get location from tweet geo or use random
                    if tweet.geo:
                        # Extract from geo if available
                        lat, lng = self._get_random_location()  # Placeholder
                    else:
                        lat, lng = self._get_random_location()
                    
                    posts.append({
                        "text": text[:500],
                        "lat": lat,
                        "lng": lng,
                        "source": "twitter",
                        "timestamp": datetime.utcnow()
                    })
        except Exception as e:
            print(f"Error in Twitter fetch: {e}")
        
        return posts
    
    def _get_random_location(self) -> tuple:
        """
        Generate a random location (lat, lng)
        In production, use geocoding services or user location data
        """
        # Random locations weighted towards populated areas
        major_cities = [
            (40.7128, -74.0060),   # New York
            (34.0522, -118.2437),  # Los Angeles
            (51.5074, -0.1278),    # London
            (35.6762, 139.6503),   # Tokyo
            (-33.8688, 151.2093),  # Sydney
            (28.6139, 77.2090),    # Delhi
            (-23.5505, -46.6333),  # São Paulo
            (55.7558, 37.6173),    # Moscow
            (48.8566, 2.3522),     # Paris
            (39.9042, 116.4074),   # Beijing
        ]
        
        # 70% chance of major city, 30% random
        if random.random() < 0.7:
            return random.choice(major_cities)
        else:
            return (
                random.uniform(-90, 90),
                random.uniform(-180, 180)
            )

    # --- Deduplication helpers ------------------------------------------------------
    def _is_duplicate(self, _id: Optional[str]) -> bool:
        """Return True if id seen recently; track id otherwise."""
        if not _id:
            return False
        if _id in self._recent_ids:
            return True
        # record id
        self._recent_ids.add(_id)
        self._recent_ids_queue.append(_id)
        # keep set in sync with queue size
        if len(self._recent_ids_queue) > self._recent_ids_queue.maxlen:
            old = self._recent_ids_queue.popleft()
            self._recent_ids.discard(old)
        return False

    # --- Geocoding helper (simple, optional) ---------------------------------------
    def _geocode_text(self, text: str) -> Optional[tuple]:
        """Try to geocode a location string found in text using Nominatim.

        Returns (lat, lng) or None.
        """
        if not self.geocoder_enabled or not text or len(text) < 3:
            return None
        try:
            params = {"q": text, "format": "json", "limit": 1}
            headers = {"User-Agent": "EarthPulse/1.0 (email@example.com)"}
            resp = requests.get(self.geocoder_url, params=params, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    lat = float(data[0]["lat"])
                    lon = float(data[0]["lon"])
                    # Respect Nominatim usage policy: sleep briefly
                    time.sleep(1)
                    return (lat, lon)
        except Exception as e:
            print(f"Geocode error: {e}")
        return None
    
    def _generate_mock_posts(self, limit: int) -> List[Dict]:
        """Generate mock posts for demo/testing when APIs are not available"""
        mock_texts = [
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
            "Celebrating a small victory today. Every step counts!",
            "Feeling overwhelmed with all the tasks on my plate.",
            "Amazing sunset tonight. Nature never fails to amaze.",
            "Concerned about the future. Hoping for the best.",
            "Thrilled about the concert next week! Can't wait!",
        ]
        
        posts = []
        for i in range(limit):
            text = random.choice(mock_texts)
            lat, lng = self._get_random_location()
            source = random.choice(["reddit", "twitter"])
            
            posts.append({
                "text": text,
                "lat": lat,
                "lng": lng,
                "source": source,
                "timestamp": datetime.utcnow() - timedelta(minutes=random.randint(0, 60))
            })
        
        return posts

