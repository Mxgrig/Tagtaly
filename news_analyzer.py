# news_analyzer.py
import sqlite3
import pandas as pd
from textblob import TextBlob
import re

# Simple keyword-based topic classifier (fast, no ML needed initially)
TOPICS = {
    'Politics': ['government', 'minister', 'parliament', 'election', 'labour', 'conservative', 'policy', 'mp'],
    'Economy': ['economy', 'inflation', 'interest rate', 'gdp', 'bank', 'financial', 'business', 'market'],
    'Crime': ['police', 'crime', 'arrest', 'court', 'murder', 'theft', 'investigation'],
    'Health': ['nhs', 'hospital', 'health', 'covid', 'doctor', 'patient', 'care'],
    'Energy': ['energy', 'electricity', 'gas', 'oil', 'renewable', 'climate'],
}

def classify_topic(text):
    text_lower = text.lower()
    scores = {}

    for topic, keywords in TOPICS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        scores[topic] = score

    # Return topic with highest score, or 'Other'
    max_topic = max(scores, key=scores.get)
    return max_topic if scores[max_topic] > 0 else 'Other'

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1

    if polarity > 0.1:
        return 'positive', polarity
    elif polarity < -0.1:
        return 'negative', polarity
    else:
        return 'neutral', polarity

def analyze_articles():
    conn = sqlite3.connect('uk_news.db')

    # Add columns if they don't exist
    try:
        conn.execute('ALTER TABLE articles ADD COLUMN topic TEXT')
        conn.execute('ALTER TABLE articles ADD COLUMN sentiment TEXT')
        conn.execute('ALTER TABLE articles ADD COLUMN sentiment_score REAL')
    except:
        pass

    df = pd.read_sql_query("SELECT * FROM articles WHERE topic IS NULL", conn)

    print(f"Analyzing {len(df)} articles...")

    for idx, row in df.iterrows():
        text = f"{row['headline']} {row['summary']}"

        topic = classify_topic(text)
        sentiment, score = analyze_sentiment(text)

        conn.execute('''
            UPDATE articles
            SET topic = ?, sentiment = ?, sentiment_score = ?
            WHERE id = ?
        ''', (topic, sentiment, score, row['id']))

    conn.commit()
    conn.close()
    print("✓ Analysis complete!")

if __name__ == "__main__":
    analyze_articles()
