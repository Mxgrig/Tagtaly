# news_collector.py
import feedparser
import sqlite3
from datetime import datetime
import hashlib
import sys
import os
import time
import requests

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.countries import get_active_countries, get_country_config

# Set User-Agent for feedparser to avoid rejection
feedparser.USER_AGENT = 'Tagtaly/1.0 (+http://tagtaly.com) news aggregator'

def init_database():
    """Initialize database with updated schema"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'tagtaly.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            headline TEXT,
            source TEXT,
            url TEXT,
            published_date TEXT,
            summary TEXT,
            fetched_at TEXT,
            country TEXT NOT NULL DEFAULT 'UK',
            scope TEXT,
            topic TEXT,
            sentiment TEXT,
            sentiment_score REAL,
            viral_score REAL DEFAULT 0
        )
    ''')

    # Create indexes
    c.execute('CREATE INDEX IF NOT EXISTS idx_country ON articles(country)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_scope ON articles(scope)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_viral_score ON articles(viral_score)')

    conn.commit()
    return conn

def fetch_feed_with_retry(url, source, max_retries=3, timeout=10):
    """
    Fetch RSS feed with retry logic and timeout handling

    Args:
        url: RSS feed URL
        source: Source name for logging
        max_retries: Number of retry attempts
        timeout: Request timeout in seconds

    Returns:
        feedparser result or None if failed
    """
    for attempt in range(max_retries):
        try:
            # Use timeout parameter
            feed = feedparser.parse(url, agent='Tagtaly/1.0 (+http://tagtaly.com)')

            # Check for HTTP errors
            if hasattr(feed, 'status'):
                if feed.status == 200:
                    return feed
                elif feed.status >= 500:
                    # Server error - retry
                    print(f"    Attempt {attempt + 1}/{max_retries}: Server error (HTTP {feed.status}), retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    print(f"    Error: HTTP {feed.status} - {feed.get('bozo_exception', 'Unknown error')}")
                    return None

            # If we got here, assume success
            return feed

        except Exception as e:
            print(f"    Attempt {attempt + 1}/{max_retries}: {type(e).__name__}: {str(e)[:80]}")

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"    Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"    ✗ Failed to fetch {source} after {max_retries} attempts")
                return None

    return None


def fetch_news_for_country(country_code, conn):
    """Fetch news for a specific country with improved error handling"""
    config = get_country_config(country_code)
    if not config:
        print(f"No configuration found for {country_code}")
        return 0

    c = conn.cursor()
    total_articles = 0
    successful_sources = 0
    failed_sources = 0

    print(f"\n{config['flag']} Fetching news for {config['name']}...")

    for source, url in config['feeds'].items():
        print(f"  🔄 {source}...", end='', flush=True)

        feed = fetch_feed_with_retry(url, source)

        if feed is None:
            failed_sources += 1
            print(f"  ✗ Failed")
            continue

        # Check for parsing errors
        if hasattr(feed, 'bozo') and feed.bozo:
            print(f"  ⚠️  Parse warning (but continuing): {feed.bozo_exception}")

        # Count successful fetches
        entry_count = len(feed.entries) if hasattr(feed, 'entries') else 0

        if entry_count == 0:
            print(f"  ⚠️  No articles found")
            continue

        for entry in feed.entries:
            try:
                # Create unique ID from country + URL
                article_id = hashlib.md5(f"{country_code}:{entry.link}".encode()).hexdigest()

                c.execute('''
                    INSERT OR IGNORE INTO articles
                    (id, headline, source, url, published_date, summary, fetched_at, country)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article_id,
                    entry.title,
                    source,
                    entry.link,
                    entry.get('published', ''),
                    entry.get('summary', ''),
                    datetime.now().isoformat(),
                    country_code
                ))
                total_articles += 1
            except Exception as e:
                print(f"\n      DB Error inserting article: {str(e)[:60]}")

        conn.commit()
        successful_sources += 1
        print(f"  ✓ {entry_count} articles")

    print(f"\n  Summary: {successful_sources} sources successful, {failed_sources} failed")
    return total_articles

def fetch_news():
    """Fetch news from all active countries"""
    conn = init_database()
    active_countries = get_active_countries()

    print(f"Active countries: {', '.join(active_countries)}")

    total_count = 0
    for country in active_countries:
        count = fetch_news_for_country(country, conn)
        total_count += count

    conn.close()
    print(f"\n✓ Total: {total_count} articles collected")
    return total_count

if __name__ == "__main__":
    fetch_news()
