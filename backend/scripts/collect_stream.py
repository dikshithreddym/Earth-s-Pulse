"""
Collect streamed posts using the SocialMediaFetcher for a set number of posts and write to JSON.
Run: python scripts/collect_stream.py --count 100 --out streamed.json

This script uses the same streaming producers as the backend (PRAW/Tweepy).
Make sure env vars for Reddit/Twitter are configured in your .env.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.social_fetcher import SocialMediaFetcher

async def collect(count: int, out_path: str):
    fetcher = SocialMediaFetcher()
    q = asyncio.Queue()

    # start streams (runs threads)
    fetcher.start_streams(q, loop=asyncio.get_event_loop())

    collected = []
    print(f"Collecting up to {count} posts...")
    while len(collected) < count:
        post = await q.get()
        collected.append(post)
        print(f"Collected [{len(collected)}]: {post.get('source')} - {post.get('text')[:80]}")
        q.task_done()

    # write out
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(collected, f, default=str, indent=2)

    print(f"Wrote {len(collected)} posts to {out_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=50)
    parser.add_argument('--out', type=str, default='streamed_posts.json')
    args = parser.parse_args()

    asyncio.run(collect(args.count, args.out))
