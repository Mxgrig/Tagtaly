# viral_engine.py
from story_detector import StoryDetector
from viral_viz import ViralChartMaker
from datetime import datetime
import os

def generate_viral_content():
    """Find stories and create shareable charts"""

    detector = StoryDetector()
    viz_maker = ViralChartMaker()

    print("🔍 Hunting for viral story angles...")
    stories = detector.find_viral_angles()

    # Rank by virality score
    stories.sort(key=lambda x: x.get('virality_score', 0), reverse=True)

    # Create charts for top 3 stories
    output_dir = f"viral_charts_{datetime.now().strftime('%Y%m%d')}"
    os.makedirs(output_dir, exist_ok=True)

    for i, story in enumerate(stories[:3]):
        if not story.get('data'):
            continue

        print(f"\n📊 Creating: {story['headline']}")

        if story['type'] == 'SURGE_ALERT':
            fig = viz_maker.create_surge_alert(story)
        elif story['type'] == 'POLITICAL_SCORECARD':
            fig = viz_maker.create_politician_race(story)
        elif story['type'] == 'RECORD_ALERT':
            fig = viz_maker.create_record_highlight(story)
        else:
            continue

        if fig:
            filename = f"{output_dir}/viral_{i+1}_{story['type']}.png"
            fig.savefig(filename, dpi=100, bbox_inches='tight', facecolor=fig.get_facecolor())
            print(f"✅ Saved: {filename}")

            # Generate caption
            caption = generate_caption(story)
            with open(f"{filename.replace('.png', '_caption.txt')}", 'w') as f:
                f.write(caption)

    print(f"\n🎉 {len(stories[:3])} viral charts ready for social media!")
    print(f"📁 Find them in: {output_dir}/")

def generate_caption(story):
    """Create engaging social media caption"""

    emoji_map = {
        'SURGE_ALERT': '🚨📈',
        'POLITICAL_SCORECARD': '🗳️📊',
        'RECORD_ALERT': '⚠️🔥',
        'MEDIA_BIAS': '📰👀'
    }

    caption = f"{emoji_map.get(story['type'], '📊')} {story['headline']}\n\n"
    caption += "UK news, counted & charted. Follow @tagtaly for daily insights.\n\n"
    caption += "#Tagtaly #UKNews #DataViz #UKPolitics"

    return caption

if __name__ == "__main__":
    generate_viral_content()
