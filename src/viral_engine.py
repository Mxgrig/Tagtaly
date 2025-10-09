# viral_engine.py
from story_detector import StoryDetector
from viral_viz import ViralChartMaker
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
    Generate charts for a specific country

    Args:
        country: 'UK', 'US', or None for global
        date_str: Date string for output folder

    Returns:
        int: Number of charts created
    """
    detector = StoryDetector(country=country)
    viz_maker = ViralChartMaker()

    country_name = get_country_config(country)['name'] if country else 'Global'
    print(f"\n🔍 Hunting for {country_name} viral story angles...")

    stories = detector.find_viral_angles()

    if not stories:
        print(f"   No viral stories found for {country_name}")
        return 0

    # Rank by virality score
    stories.sort(key=lambda x: x.get('virality_score', 0), reverse=True)

    # Create output directory
    if country:
        output_dir = f"output/viral_charts_{country.lower()}_{date_str}"
    else:
        output_dir = f"output/viral_charts_global_{date_str}"

    os.makedirs(output_dir, exist_ok=True)

    charts_created = 0

    # Create charts for top 3-4 stories
    for i, story in enumerate(stories[:4]):
        data = story.get('data')
        if data is None or (hasattr(data, 'empty') and data.empty):
            continue

        print(f"   📊 Creating: {story['headline']}")

        # Select appropriate chart type
        fig = None
        if story['type'] == 'SURGE_ALERT':
            fig = viz_maker.create_surge_alert(story, country)
        elif story['type'] in ['VIRAL_PEOPLE_SCORECARD', 'POLITICAL_SCORECARD']:
            fig = viz_maker.create_viral_people_race(story, country)
        elif story['type'] == 'RECORD_ALERT':
            fig = viz_maker.create_record_highlight(story, country)
        elif story['type'] == 'SENTIMENT_SHIFT':
            fig = viz_maker.create_sentiment_shift(story, country)
        elif story['type'] == 'MEDIA_BIAS':
            fig = viz_maker.create_media_bias_chart(story, country)

        if fig:
            filename = f"{output_dir}/viral_{i+1}_{story['type']}.png"
            fig.savefig(filename, dpi=100, bbox_inches='tight', facecolor=fig.get_facecolor())
            print(f"   ✅ Saved: {filename}")

            # Generate caption
            caption = generate_caption(story, country)
            with open(f"{filename.replace('.png', '_caption.txt')}", 'w') as f:
                f.write(caption)

            charts_created += 1

    print(f"   🎉 {charts_created} charts created for {country_name}")
    print(f"   📁 Location: {output_dir}/")

    return charts_created

def generate_viral_content():
    """
    Generate charts for all active countries + global

    This is the main entry point for viral content generation.
    Creates separate folders for each country and global content.
    """
    active_countries = get_active_countries()
    date_str = datetime.now().strftime('%Y%m%d')

    print(f"🚀 Tagtaly Viral Content Generator")
    print(f"📅 Date: {date_str}")
    print(f"🌍 Active countries: {', '.join(active_countries)}")

    total_charts = 0

    # Generate country-specific charts
    for country in active_countries:
        count = create_charts_for_country(country, date_str)
        total_charts += count

    # Generate global charts
    global_count = create_charts_for_country(None, date_str)
    total_charts += global_count

    print(f"\n✨ COMPLETE! Total {total_charts} viral charts ready for social media!")
    print(f"\n📂 Output locations:")
    for country in active_countries:
        print(f"   {country}: output/viral_charts_{country.lower()}_{date_str}/")
    print(f"   Global: output/viral_charts_global_{date_str}/")

if __name__ == "__main__":
    generate_viral_content()
