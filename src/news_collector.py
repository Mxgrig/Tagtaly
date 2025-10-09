# news_collector.py
import feedparser
import sqlite3
from datetime import datetime
import hashlib
import sys
import os

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.countries import get_active_countries, get_country_config

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

def fetch_news_for_country(country_code, conn):
    """Fetch news for a specific country"""
    config = get_country_config(country_code)
    if not config:
        print(f"No configuration found for {country_code}")
        return 0

    c = conn.cursor()
    total_articles = 0

    print(f"\n{config['flag']} Fetching news for {config['name']}...")

    for source, url in config['feeds'].items():
        try:
            print(f"  Fetching from {source}...")
            feed = feedparser.parse(url)

            for entry in feed.entries:
                # Create unique ID from country + URL
                article_id = hashlib.md5(f"{country_code}:{entry.link}".encode()).hexdigest()

                try:
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
                    print(f"    Error inserting {entry.title[:50]}: {e}")

            conn.commit()
            print(f"  ✓ Fetched {len(feed.entries)} articles from {source}")

        except Exception as e:
            print(f"  ✗ Error fetching from {source}: {e}")
            continue

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
