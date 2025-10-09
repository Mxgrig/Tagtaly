# story_detector.py
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import re
import sys
import os

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.countries import get_country_config, get_viral_people
from config.viral_topics import should_post

class StoryDetector:
    def __init__(self, country=None, db_path=None):
        """
        Initialize story detector

        Args:
            country: 'UK', 'US', or None for global stories
            db_path: Path to database
        """
        self.country = country
        if db_path is None:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'tagtaly.db')
        self.conn = sqlite3.connect(db_path)
        self.config = get_country_config(country) if country else None

    def find_viral_angles(self):
        """Detect the most shareable story angles, filtered by viral score"""
        stories = []

        # 1. SURGE DETECTION - What exploded this week?
        stories.append(self.detect_topic_surge())

        # 2. POLITICIAN/CELEBRITY SCORECARD - Who's dominating the news?
        stories.append(self.track_viral_people_mentions())

        # 3. SENTIMENT SHIFT - Mood change detection
        stories.append(self.detect_sentiment_shift())

        # 4. RECORD BREAKING - New highs/lows
        stories.append(self.find_record_numbers())

        # 5. MEDIA BIAS TRACKER - Who covers what?
        stories.append(self.compare_outlet_focus())

        # Filter by viral score (must be >= 5)
        filtered_stories = [s for s in stories if s.get('virality_score', 0) >= 5]

        # Sort by viral score
        filtered_stories.sort(key=lambda x: x.get('virality_score', 0), reverse=True)

        return filtered_stories

    def detect_topic_surge(self):
        """Find topics that suddenly exploded in coverage"""

        # Build country filter
        country_filter = f"AND country = '{self.country}'" if self.country else ""

        # Compare this week vs last week
        this_week = pd.read_sql_query(f'''
            SELECT topic, COUNT(*) as count
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-7 days')
            AND viral_score >= 5
            {country_filter}
            GROUP BY topic
        ''', self.conn)

        last_week = pd.read_sql_query(f'''
            SELECT topic, COUNT(*) as count
            FROM articles
            WHERE DATE(fetched_at) BETWEEN DATE('now', '-14 days') AND DATE('now', '-7 days')
            {country_filter}
            GROUP BY topic
        ''', self.conn)

        if len(this_week) == 0 or len(last_week) == 0:
            return {'type': 'SURGE_ALERT', 'data': None, 'virality_score': 0}

        # Calculate % change
        merged = this_week.merge(last_week, on='topic', suffixes=('_now', '_before'), how='left')
        merged['count_before'] = merged['count_before'].fillna(1)  # Avoid division by zero
        merged['pct_change'] = ((merged['count_now'] - merged['count_before']) /
                                merged['count_before'] * 100)

        top_surge = merged.nlargest(1, 'pct_change').iloc[0]

        flag = self.config['flag'] if self.config else '🌍'

        return {
            'type': 'SURGE_ALERT',
            'headline': f"{flag} {top_surge['topic']} news UP {top_surge['pct_change']:.0f}% this week",
            'viz_type': 'comparison_bars',
            'data': merged,
            'virality_score': min(abs(top_surge['pct_change']) / 10, 20),
            'country': self.country
        }

    def track_viral_people_mentions(self):
        """Count mentions of viral people (politicians, tech CEOs, celebrities, etc.)"""

        # Get country-specific politicians
        people_to_track = {}

        if self.country and self.config:
            people_to_track.update(self.config.get('politicians', {}))

        # Add global viral people
        viral_people = get_viral_people()
        for category, people in viral_people.items():
            people_to_track.update(people)

        country_filter = f"AND country = '{self.country}'" if self.country else ""

        df = pd.read_sql_query(f'''
            SELECT headline, summary, fetched_at
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-7 days')
            AND viral_score >= 5
            {country_filter}
        ''', self.conn)

        if len(df) == 0:
            return {'type': 'VIRAL_PEOPLE_SCORECARD', 'data': None, 'virality_score': 0}

        mention_counts = {}
        for name, keywords in people_to_track.items():
            count = 0
            for _, row in df.iterrows():
                text = f"{row['headline']} {row['summary']}".lower()
                if any(keyword.lower() in text for keyword in keywords):
                    count += 1
            if count > 0:
                mention_counts[name] = count

        if len(mention_counts) < 2:
            return {'type': 'VIRAL_PEOPLE_SCORECARD', 'data': None, 'virality_score': 0}

        # Create dramatic headline
        sorted_counts = sorted(mention_counts.items(), key=lambda x: x[1], reverse=True)
        leader = sorted_counts[0]
        runner_up = sorted_counts[1]

        ratio = leader[1] / max(runner_up[1], 1)
        flag = self.config['flag'] if self.config else '🌍'

        return {
            'type': 'VIRAL_PEOPLE_SCORECARD',
            'headline': f"{flag} {leader[0]} mentioned {ratio:.1f}x more than {runner_up[0]} this week",
            'viz_type': 'race_chart',
            'data': mention_counts,
            'virality_score': min(ratio * 2, 20),
            'country': self.country
        }

    def detect_sentiment_shift(self):
        """Detect major mood changes in news coverage"""

        country_filter = f"AND country = '{self.country}'" if self.country else ""

        # Compare sentiment this week vs last week by topic
        this_week = pd.read_sql_query(f'''
            SELECT topic, AVG(sentiment_score) as avg_sentiment
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-7 days')
            AND sentiment_score IS NOT NULL
            {country_filter}
            GROUP BY topic
        ''', self.conn)

        last_week = pd.read_sql_query(f'''
            SELECT topic, AVG(sentiment_score) as avg_sentiment
            FROM articles
            WHERE DATE(fetched_at) BETWEEN DATE('now', '-14 days') AND DATE('now', '-7 days')
            AND sentiment_score IS NOT NULL
            {country_filter}
            GROUP BY topic
        ''', self.conn)

        if len(this_week) == 0 or len(last_week) == 0:
            return {'type': 'SENTIMENT_SHIFT', 'data': None, 'virality_score': 0}

        merged = this_week.merge(last_week, on='topic', suffixes=('_now', '_before'))
        merged['sentiment_change'] = merged['avg_sentiment_now'] - merged['avg_sentiment_before']

        # Find biggest shift (positive or negative)
        merged['abs_change'] = abs(merged['sentiment_change'])
        top_shift = merged.nlargest(1, 'abs_change').iloc[0]

        if abs(top_shift['sentiment_change']) < 0.1:
            return {'type': 'SENTIMENT_SHIFT', 'data': None, 'virality_score': 0}

        direction = "more negative" if top_shift['sentiment_change'] < 0 else "more positive"
        flag = self.config['flag'] if self.config else '🌍'

        return {
            'type': 'SENTIMENT_SHIFT',
            'headline': f"{flag} {top_shift['topic']} coverage turned {direction} this week",
            'viz_type': 'sentiment_chart',
            'data': merged,
            'virality_score': min(abs(top_shift['sentiment_change']) * 20, 20),
            'country': self.country
        }

    def find_record_numbers(self):
        """Extract numeric claims and flag records"""

        country_filter = f"AND country = '{self.country}'" if self.country else ""

        df = pd.read_sql_query(f'''
            SELECT headline, summary, source, fetched_at, viral_score
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-2 days')
            AND viral_score >= 10
            {country_filter}
        ''', self.conn)

        if len(df) == 0:
            return {'type': 'RECORD_ALERT', 'data': None, 'virality_score': 0}

        # Pattern matching for impactful numbers
        record_patterns = [
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(million|billion|thousand)?\s*(?:people|deaths|jobs|homes)',
            r'highest\s+(?:in|since)',
            r'lowest\s+(?:in|since)',
            r'record\s+(?:high|low)',
            r'(\d+)%\s+(?:increase|decrease|rise|fall)'
        ]

        records = []
        for _, row in df.iterrows():
            text = f"{row['headline']} {row['summary']}"
            for pattern in record_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    records.append({
                        'headline': row['headline'],
                        'source': row['source'],
                        'viral_score': row['viral_score'],
                        'text_snippet': text[:200]
                    })
                    break

        if len(records) == 0:
            return {'type': 'RECORD_ALERT', 'data': None, 'virality_score': 0}

        flag = self.config['flag'] if self.config else '🌍'

        return {
            'type': 'RECORD_ALERT',
            'headline': f"{flag} {len(records)} record-breaking stories this week",
            'viz_type': 'highlight_numbers',
            'data': records[:5],
            'virality_score': min(len(records) * 2, 20),
            'country': self.country
        }

    def compare_outlet_focus(self):
        """What's each outlet obsessed with?"""

        country_filter = f"AND country = '{self.country}'" if self.country else ""

        df = pd.read_sql_query(f'''
            SELECT source, topic, COUNT(*) as count
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-7 days')
            AND viral_score >= 5
            {country_filter}
            GROUP BY source, topic
        ''', self.conn)

        if len(df) == 0:
            return {'type': 'MEDIA_BIAS', 'data': None, 'virality_score': 0}

        # Find each outlet's top topic
        outlet_focus = df.loc[df.groupby('source')['count'].idxmax()]

        flag = self.config['flag'] if self.config else '🌍'
        country_name = self.config['name'] if self.config else 'Global'

        return {
            'type': 'MEDIA_BIAS',
            'headline': f"{flag} What {country_name} outlets are REALLY covering this week",
            'viz_type': 'source_comparison',
            'data': outlet_focus,
            'virality_score': 8,
            'country': self.country
        }

    def detect_global_stories(self):
        """Stories that work for BOTH UK and US audiences"""
        # Only run if this is a global detector (country=None)
        if self.country:
            return []

        df = pd.read_sql_query('''
            SELECT topic, COUNT(DISTINCT country) as country_count, COUNT(*) as total_count
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-7 days')
            AND scope = 'GLOBAL'
            AND viral_score >= 10
            GROUP BY topic
            HAVING country_count >= 2
            ORDER BY total_count DESC
        ''', self.conn)

        if len(df) == 0:
            return []

        stories = []
        for _, row in df.iterrows():
            stories.append({
                'type': 'GLOBAL_STORY',
                'headline': f"🌍 {row['topic']} trending in {row['country_count']} countries",
                'viz_type': 'global_comparison',
                'data': row,
                'virality_score': min(row['country_count'] * 5, 20),
                'country': None
            })

        return stories[:3]

if __name__ == "__main__":
    # Test detector
    print("Testing UK detector...")
    uk_detector = StoryDetector(country='UK')
    uk_stories = uk_detector.find_viral_angles()
    print(f"Found {len(uk_stories)} UK stories")

    print("\nTesting Global detector...")
    global_detector = StoryDetector(country=None)
    global_stories = global_detector.find_viral_angles()
    print(f"Found {len(global_stories)} global stories")
