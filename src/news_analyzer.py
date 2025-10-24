# news_analyzer.py
import sqlite3
import pandas as pd
from textblob import TextBlob
import sys
import os

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.countries import get_country_config, get_global_topics, get_viral_people
from config.viral_topics import VIRAL_TOPICS, calculate_viral_score

def count_keyword_matches(text, keywords_dict):
    """Count how many keywords match in text"""
    text_lower = text.lower()
    matches = 0

    if isinstance(keywords_dict, dict):
        # Handle nested dictionaries
        for category, keywords in keywords_dict.items():
            if isinstance(keywords, list):
                matches += sum(1 for keyword in keywords if keyword in text_lower)
            elif isinstance(keywords, dict):
                # Handle nested categories (like VIRAL_TOPICS)
                for subcategory, subkeywords in keywords.items():
                    matches += sum(1 for keyword in subkeywords if keyword in text_lower)
    elif isinstance(keywords_dict, list):
        matches = sum(1 for keyword in keywords_dict if keyword in text_lower)

    return matches

def classify_article_scope(text):
    """Determine if article is LOCAL or GLOBAL"""
    global_topics = get_global_topics()
    global_matches = count_keyword_matches(text, global_topics)

    # If matches 2+ global topics, it's global
    if global_matches >= 2:
        return 'GLOBAL'
    else:
        return 'LOCAL'

def classify_topic(text, country_code):
    """Classify topic using country-specific OR global keywords"""
    text_lower = text.lower()
    scores = {}
    subcategory_scores = {}  # Track subcategories separately

    # Check global topics first
    global_topics = get_global_topics()
    for topic, keywords in global_topics.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        scores[topic] = score

    # Check country-specific topics
    config = get_country_config(country_code)
    if config and 'local_topics' in config:
        for topic, keywords in config['local_topics'].items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if topic in scores:
                scores[topic] += score
            else:
                scores[topic] = score

    # Check viral topics (engagement-focused)
    for topic_category, subcategories in VIRAL_TOPICS.items():
        for subcategory, keywords in subcategories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)

            # Track subcategories for "Other" category SEPARATELY
            if topic_category == 'Other':
                subcategory_scores[subcategory] = score
                # DON'T add to main scores for "Other" - only track main categories
                continue

            # Add to main category scores for non-"Other" topics
            if topic_category in scores:
                scores[topic_category] += score
            else:
                scores[topic_category] = score

    # Return topic with highest score (excluding "Other")
    if scores:
        # Remove "Other" temporarily to check other categories
        other_score = scores.pop('Other', 0)

        if scores:  # If there are non-"Other" topics with matches
            max_topic = max(scores, key=scores.get)
            if scores[max_topic] > 0:
                return max_topic

    # If no main category matched, return best subcategory from "Other"
    if subcategory_scores:
        best_subcategory = max(subcategory_scores, key=subcategory_scores.get)
        # Return the subcategory if it has at least 1 match
        if subcategory_scores[best_subcategory] >= 1:
            return best_subcategory

    return 'Other'

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1

    if polarity > 0.1:
        return 'positive', polarity
    elif polarity < -0.1:
        return 'negative', polarity
    else:
        return 'neutral', polarity

def analyze_articles():
    """Analyze all articles with updated logic"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'tagtaly.db')
    conn = sqlite3.connect(db_path)

    # Fetch unanalyzed articles
    df = pd.read_sql_query(
        "SELECT * FROM articles WHERE topic IS NULL OR viral_score IS NULL",
        conn
    )

    if len(df) == 0:
        print("No articles to analyze")
        conn.close()
        return

    print(f"Analyzing {len(df)} articles...")

    for idx, row in df.iterrows():
        text = f"{row['headline']} {row['summary']}"

        # Classify scope (LOCAL vs GLOBAL)
        scope = classify_article_scope(text)

        # Classify topic
        topic = classify_topic(text, row['country'])

        # Analyze sentiment
        sentiment, sentiment_score = analyze_sentiment(text)

        # Calculate viral score
        viral_score = calculate_viral_score(row['headline'], row['summary'])

        # Update database
        conn.execute('''
            UPDATE articles
            SET topic = ?, sentiment = ?, sentiment_score = ?, scope = ?, viral_score = ?
            WHERE id = ?
        ''', (topic, sentiment, sentiment_score, scope, viral_score, row['id']))

        if (idx + 1) % 50 == 0:
            print(f"  Processed {idx + 1}/{len(df)} articles...")
            conn.commit()

    conn.commit()
    conn.close()
    print("✓ Analysis complete!")

    # Print summary
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'tagtaly.db')
    conn = sqlite3.connect(db_path)
    summary = pd.read_sql_query('''
        SELECT
            country,
            scope,
            topic,
            COUNT(*) as count,
            AVG(viral_score) as avg_viral_score
        FROM articles
        WHERE viral_score IS NOT NULL
        GROUP BY country, scope, topic
        ORDER BY country, avg_viral_score DESC
    ''', conn)
    conn.close()

    print("\n📊 Analysis Summary:")
    print(summary.to_string())

if __name__ == "__main__":
    analyze_articles()
