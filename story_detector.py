# story_detector.py
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import re

class StoryDetector:
    def __init__(self, db_path='uk_news.db'):
        self.conn = sqlite3.connect(db_path)

    def find_viral_angles(self):
        """Detect the most shareable story angles from recent news"""
        stories = []

        # 1. SURGE DETECTION - What exploded this week?
        stories.append(self.detect_topic_surge())

        # 2. POLITICIAN SCORECARD - Who's dominating the news?
        stories.append(self.track_political_mentions())

        # 3. REGIONAL DISPARITY - Geographic inequality
        stories.append(self.analyze_regional_coverage())

        # 4. SENTIMENT SHIFT - Mood change detection
        stories.append(self.detect_sentiment_shift())

        # 5. RECORD BREAKING - New highs/lows
        stories.append(self.find_record_numbers())

        # 6. MEDIA BIAS TRACKER - Who covers what?
        stories.append(self.compare_outlet_focus())

        return stories

    def detect_topic_surge(self):
        """Find topics that suddenly exploded in coverage"""

        # Compare this week vs last week
        this_week = pd.read_sql_query('''
            SELECT topic, COUNT(*) as count
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-7 days')
            GROUP BY topic
        ''', self.conn)

        last_week = pd.read_sql_query('''
            SELECT topic, COUNT(*) as count
            FROM articles
            WHERE DATE(fetched_at) BETWEEN DATE('now', '-14 days') AND DATE('now', '-7 days')
            GROUP BY topic
        ''', self.conn)

        # Calculate % change
        merged = this_week.merge(last_week, on='topic', suffixes=('_now', '_before'))
        merged['pct_change'] = ((merged['count_now'] - merged['count_before']) /
                                merged['count_before'] * 100)

        top_surge = merged.nlargest(1, 'pct_change').iloc[0]

        return {
            'type': 'SURGE_ALERT',
            'headline': f"🚨 {top_surge['topic']} news UP {top_surge['pct_change']:.0f}% this week",
            'viz_type': 'comparison_bars',
            'data': merged,
            'virality_score': abs(top_surge['pct_change']) / 10
        }

    def track_political_mentions(self):
        """Count mentions of key political figures"""

        politicians = {
            'Keir Starmer': ['starmer', 'keir'],
            'Rishi Sunak': ['sunak', 'rishi'],
            'Nigel Farage': ['farage', 'nigel'],
            'Ed Davey': ['davey', 'ed davey'],
        }

        df = pd.read_sql_query('''
            SELECT headline, summary, fetched_at
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-7 days')
        ''', self.conn)

        mention_counts = {}
        for name, keywords in politicians.items():
            count = 0
            for _, row in df.iterrows():
                text = f"{row['headline']} {row['summary']}".lower()
                if any(keyword in text for keyword in keywords):
                    count += 1
            mention_counts[name] = count

        # Create dramatic headline
        leader = max(mention_counts, key=mention_counts.get)
        runner_up = sorted(mention_counts.items(), key=lambda x: x[1], reverse=True)[1]

        ratio = mention_counts[leader] / max(runner_up[1], 1)

        return {
            'type': 'POLITICAL_SCORECARD',
            'headline': f"📊 {leader} mentioned {ratio:.1f}x more than {runner_up[0]} this week",
            'viz_type': 'race_chart',
            'data': mention_counts,
            'virality_score': ratio * 2
        }

    def find_record_numbers(self):
        """Extract numeric claims and flag records"""

        df = pd.read_sql_query('''
            SELECT headline, summary, source, fetched_at
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-1 days')
        ''', self.conn)

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
                        'text_snippet': text[:200]
                    })
                    break

        if records:
            return {
                'type': 'RECORD_ALERT',
                'headline': f"🚨 {len(records)} record-breaking stories today",
                'viz_type': 'highlight_numbers',
                'data': records[:5],
                'virality_score': len(records)
            }

        return {'type': 'RECORD_ALERT', 'data': None, 'virality_score': 0}

    def compare_outlet_focus(self):
        """What's each outlet obsessed with?"""

        df = pd.read_sql_query('''
            SELECT source, topic, COUNT(*) as count
            FROM articles
            WHERE DATE(fetched_at) >= DATE('now', '-7 days')
            GROUP BY source, topic
        ''', self.conn)

        # Find each outlet's top topic
        outlet_focus = df.loc[df.groupby('source')['count'].idxmax()]

        return {
            'type': 'MEDIA_BIAS',
            'headline': f"📰 What each UK outlet is REALLY covering this week",
            'viz_type': 'source_comparison',
            'data': outlet_focus,
            'virality_score': 7
        }
