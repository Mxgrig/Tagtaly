# viral_engine.py
from story_detector import StoryDetector
from json_generator import JSONChartGenerator
from datetime import datetime
import os
import sys

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.countries import get_active_countries, get_country_config

def generate_caption(story, country):
    """
    Generate country-specific caption

    Args:
        story: Story dictionary
        country: 'UK', 'US', or None for global

    Returns:
        str: Social media caption
    """
    emoji_map = {
        'SURGE_ALERT': '🚨📈',
        'VIRAL_PEOPLE_SCORECARD': '🗳️📊',
        'POLITICAL_SCORECARD': '🗳️📊',
        'RECORD_ALERT': '⚠️🔥',
        'MEDIA_BIAS': '📰👀',
        'SENTIMENT_SHIFT': '😤😊',
        'GLOBAL_STORY': '🌍📊'
    }

    if country == 'UK':
        emoji = '🇬🇧'
        handle = '@tagtaly'
        hashtags = '#TagtalyUK #UKNews #DataViz'
    elif country == 'US':
        emoji = '🇺🇸'
        handle = '@tagtaly'
        hashtags = '#TagtalyUS #USNews #DataViz'
    else:  # Global
        emoji = '🌍'
        handle = '@tagtaly'
        hashtags = '#Tagtaly #GlobalNews #DataViz'

    type_emoji = emoji_map.get(story['type'], '📊')
    caption = f"{type_emoji} {story['headline']}\n\n"
    caption += f"News that matters. Data that shows it. Follow {handle}\n\n"
    caption += hashtags

    return caption

def create_charts_for_country(country, date_str):
    """
    Generate JSON charts for a specific country (ECharts format)

    Args:
        country: 'UK', 'US', or None for global
        date_str: Date string for output folder

    Returns:
        int: Number of JSON chart pairs created
    """
    detector = StoryDetector(country=country)

    # Create country-specific output directory
    country_code = country.lower() if country else 'global'
    output_dir = f"social_dashboard/assets/data/{country_code}"
    os.makedirs(output_dir, exist_ok=True)

    json_generator = JSONChartGenerator(output_dir=output_dir)

    country_name = get_country_config(country)['name'] if country else 'Global'
    print(f"\n🔍 Hunting for {country_name} viral story angles...")

    stories = detector.find_viral_angles()

    if not stories:
        print(f"   No viral stories found for {country_name}")
        return 0

    # Rank by virality score
    stories.sort(key=lambda x: x.get('virality_score', 0), reverse=True)

    print(f"   📊 Generating {len(stories[:4])} chart pairs (primary + alternate)...")

    # Generate JSON charts for top 4 stories
    charts_created = json_generator.generate_all_from_stories(stories[:4], country)

    print(f"   🎉 {charts_created} JSON charts created for {country_name}")
    print(f"   📁 Location: {output_dir}/")

    return charts_created

def generate_viral_content():
    """
    Generate interactive JSON charts for all active countries + global

    This is the main entry point for viral content generation.
    Creates JSON data files for ECharts visualization.
    Each story generates 2 variants: primary + alternate (for hover).
    """
    active_countries = get_active_countries()
    date_str = datetime.now().strftime('%Y%m%d')

    print(f"🚀 Tagtaly Viral Content Generator")
    print(f"📅 Date: {date_str}")
    print(f"🌍 Active countries: {', '.join(active_countries)}")
    print(f"📊 Output format: Interactive JSON (ECharts)")

    total_charts = 0

    # Generate country-specific charts
    for country in active_countries:
        count = create_charts_for_country(country, date_str)
        total_charts += count

    # Generate global charts
    global_count = create_charts_for_country(None, date_str)
    total_charts += global_count

    print(f"\n✨ COMPLETE! Total {total_charts} interactive JSON charts generated!")
    print(f"\n📂 Output location: social_dashboard/assets/data/[country]/")
    print(f"   - social_dashboard/assets/data/uk/")
    print(f"   - social_dashboard/assets/data/us/")
    print(f"   - social_dashboard/assets/data/global/")
    print(f"📋 Each folder contains: chart_1_primary.json, chart_1_alternate.json, ...")
    print(f"🎨 Charts render in: social_dashboard/index.html with ECharts")

if __name__ == "__main__":
    generate_viral_content()
