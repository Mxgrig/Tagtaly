# json_generator.py
"""
Convert viral story data to JSON format for ECharts visualization

Replaces matplotlib PNG generation with interactive JavaScript charts.
Each story type generates 2 chart variants (primary + alternate for hover).
"""

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.countries import get_country_config


class JSONChartGenerator:
    """Generate ECharts-compatible JSON from story data"""

    def __init__(self, output_dir="social_dashboard/assets/data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_json(self, filename, data):
        """Save JSON data to file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"   ✅ Saved: {filepath}")
        return filepath

    def generate_surge_alert(self, story):
        """Convert SURGE_ALERT to JSON - Topic surge visualization"""

        if story.get('data') is None or story['data'].empty:
            return None

        data = story['data']

        # Primary variant: Bar chart (% change)
        primary = {
            "headline": story.get('headline', 'Topic Surge Alert'),
            "type": "bar",
            "chart_type": "surge_alert_primary",
            "data": [
                [topic, float(pct)]
                for topic, pct in zip(data['topic'], data['pct_change'])
            ][:5],  # Top 5
            "virality_score": story.get('virality_score', 0)
        }

        # Alternate variant: Table/list format
        alternate = {
            "headline": story.get('headline', 'Topic Surge Alert'),
            "type": "table",
            "chart_type": "surge_alert_alternate",
            "data": [
                {
                    "topic": topic,
                    "change": float(pct),
                    "direction": "↑" if pct > 0 else "↓"
                }
                for topic, pct in zip(data['topic'], data['pct_change'])
            ][:5],
            "virality_score": story.get('virality_score', 0)
        }

        return primary, alternate

    def generate_viral_people_race(self, story):
        """Convert VIRAL_PEOPLE_SCORECARD to JSON - People mention race"""

        if story.get('data') is None:
            return None

        data_dict = story['data']
        if isinstance(data_dict, dict):
            items = list(data_dict.items())
        else:
            items = []

        if not items:
            return None

        # Sort by mentions count
        items.sort(key=lambda x: x[1], reverse=True)

        # Primary variant: Horizontal bar race
        primary = {
            "headline": story.get('headline', 'Viral People Scorecard'),
            "type": "horizontal_bar",
            "chart_type": "people_race_primary",
            "data": [
                {"name": name, "value": int(count)}
                for name, count in items[:8]
            ],
            "virality_score": story.get('virality_score', 0)
        }

        # Alternate variant: Ranked list with badges
        alternate = {
            "headline": story.get('headline', 'Viral People Scorecard'),
            "type": "ranked_list",
            "chart_type": "people_race_alternate",
            "data": [
                {
                    "rank": i + 1,
                    "name": name,
                    "mentions": int(count),
                    "badge": "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
                }
                for i, (name, count) in enumerate(items[:8])
            ],
            "virality_score": story.get('virality_score', 0)
        }

        return primary, alternate

    def generate_record_highlight(self, story):
        """Convert RECORD_ALERT to JSON - Record breaking number highlight"""

        if story.get('data') is None:
            return None

        record = story['data'][0] if isinstance(story['data'], list) else story['data']

        if not record:
            return None

        # Extract number from headline
        import re
        numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', str(record.get('headline', '')))
        big_number = numbers[0] if numbers else "NEW"

        # Primary variant: Giant number display
        primary = {
            "headline": story.get('headline', 'Record Alert'),
            "type": "giant_number",
            "chart_type": "record_primary",
            "big_number": big_number,
            "record_type": "RECORD HIGH" if 'high' in str(record.get('headline', '')).lower() else "RECORD LOW",
            "source": record.get('source', 'Unknown'),
            "virality_score": story.get('virality_score', 0)
        }

        # Alternate variant: Metric card with context
        alternate = {
            "headline": story.get('headline', 'Record Alert'),
            "type": "metric_card",
            "chart_type": "record_alternate",
            "number": big_number,
            "label": record.get('headline', '')[:60],
            "context": f"Source: {record.get('source', 'Unknown')}",
            "virality_score": story.get('virality_score', 0)
        }

        return primary, alternate

    def generate_sentiment_shift(self, story):
        """Convert SENTIMENT_SHIFT to JSON - Mood change visualization"""

        if story.get('data') is None or story['data'].empty:
            return None

        data = story['data']

        # Primary variant: Diverging bar (positive/negative)
        primary = {
            "headline": story.get('headline', 'Sentiment Shift'),
            "type": "diverging_bar",
            "chart_type": "sentiment_primary",
            "data": [
                {
                    "topic": topic,
                    "value": float(change)
                }
                for topic, change in zip(data['topic'], data['sentiment_change'])
            ][:5],
            "virality_score": story.get('virality_score', 0)
        }

        # Alternate variant: Gauge/meter style
        alternate = {
            "headline": story.get('headline', 'Sentiment Shift'),
            "type": "gauges",
            "chart_type": "sentiment_alternate",
            "data": [
                {
                    "topic": topic,
                    "shift": float(change),
                    "emoji": "📈" if change > 0 else "📉"
                }
                for topic, change in zip(data['topic'], data['sentiment_change'])
            ][:5],
            "virality_score": story.get('virality_score', 0)
        }

        return primary, alternate

    def generate_media_bias(self, story):
        """Convert MEDIA_BIAS to JSON - Source coverage focus"""

        if story.get('data') is None or story['data'].empty:
            return None

        data = story['data']

        # Primary variant: Horizontal bar by source
        primary = {
            "headline": story.get('headline', 'Media Focus'),
            "type": "media_bars",
            "chart_type": "media_bias_primary",
            "data": [
                {
                    "source": source,
                    "topic": topic,
                    "count": int(count)
                }
                for source, topic, count in zip(data['source'], data['topic'], data['count'])
            ][:6],
            "virality_score": story.get('virality_score', 0)
        }

        # Alternate variant: Bias indicator (positive/negative coverage)
        alternate = {
            "headline": story.get('headline', 'Media Focus'),
            "type": "bias_indicator",
            "chart_type": "media_bias_alternate",
            "data": [
                {
                    "source": source,
                    "focus": topic,
                    "intensity": int(count) / 10,  # Normalize
                    "bias_color": "positive" if int(count) > 5 else "neutral" if int(count) > 2 else "low"
                }
                for source, topic, count in zip(data['source'], data['topic'], data['count'])
            ][:6],
            "virality_score": story.get('virality_score', 0)
        }

        return primary, alternate

    def generate_all_from_stories(self, stories, country=None):
        """Generate all JSON charts from story list"""

        if not stories:
            print(f"   No stories to generate JSON from")
            return 0

        json_files_created = 0

        for i, story in enumerate(stories[:4]):  # Top 4 stories
            story_type = story.get('type', '')

            primary, alternate = None, None

            if story_type == 'SURGE_ALERT':
                result = self.generate_surge_alert(story)
                primary, alternate = result if result else (None, None)

            elif story_type in ['VIRAL_PEOPLE_SCORECARD', 'POLITICAL_SCORECARD']:
                result = self.generate_viral_people_race(story)
                primary, alternate = result if result else (None, None)

            elif story_type == 'RECORD_ALERT':
                result = self.generate_record_highlight(story)
                primary, alternate = result if result else (None, None)

            elif story_type == 'SENTIMENT_SHIFT':
                result = self.generate_sentiment_shift(story)
                primary, alternate = result if result else (None, None)

            elif story_type == 'MEDIA_BIAS':
                result = self.generate_media_bias(story)
                primary, alternate = result if result else (None, None)

            # Save both variants
            if primary and alternate:
                primary_file = f"chart_{i+1}_primary.json"
                alternate_file = f"chart_{i+1}_alternate.json"

                self.save_json(primary_file, primary)
                self.save_json(alternate_file, alternate)

                json_files_created += 2

        return json_files_created


if __name__ == "__main__":
    print("JSON Chart Generator ready")
