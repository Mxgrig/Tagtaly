# news_collector.py
import feedparser
import sqlite3
from datetime import datetime
import hashlib

# UK News RSS Feeds
FEEDS = {
    'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
    'Guardian': 'https://www.theguardian.com/uk/rss',
    'Sky News': 'https://feeds.skynews.com/feeds/rss/uk.xml',
    'Independent': 'https://www.independent.co.uk/news/uk/rss',
}

def init_database():
    conn = sqlite3.connect('uk_news.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            headline TEXT,
            source TEXT,
            url TEXT,
            published_date TEXT,
            summary TEXT,
            fetched_at TEXT
        )
    ''')
    conn.commit()
    return conn

def fetch_news():
    conn = init_database()
    c = conn.cursor()

    for source, url in FEEDS.items():
        print(f"Fetching from {source}...")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            # Create unique ID from URL
            article_id = hashlib.md5(entry.link.encode()).hexdigest()

            try:
                c.execute('''
                    INSERT OR IGNORE INTO articles
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article_id,
                    entry.title,
                    source,
                    entry.link,
                    entry.get('published', ''),
                    entry.get('summary', ''),
                    datetime.now().isoformat()
                ))
            except Exception as e:
                print(f"Error inserting {entry.title}: {e}")

        conn.commit()
        print(f"✓ Fetched {len(feed.entries)} articles from {source}")

    conn.close()

if __name__ == "__main__":
    fetch_news()
