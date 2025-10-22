# main_pipeline.py
import schedule
import time
import sys
import os

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from news_collector import fetch_news
from news_analyzer import analyze_articles
from viral_engine import generate_viral_content
from image_fetcher import ImageFetcher
from config.countries import get_active_countries
from datetime import datetime

def daily_job():
    """Main pipeline execution"""
    active_countries = get_active_countries()

    print(f"\n{'='*60}")
    print(f"🚀 TAGTALY NEWS PIPELINE")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌍 Active countries: {', '.join(active_countries)}")
    print(f"{'='*60}\n")

    try:
        # Step 1: Fetch news from all active countries
        print("📰 STEP 1: Fetching news...")
        fetch_news()

        # Step 2: Analyze articles (classify topics, score virality)
        print("\n🔬 STEP 2: Analyzing articles...")
        analyze_articles()

        # Step 3: Generate viral charts for each country + global
        print("\n📊 STEP 3: Generating viral charts...")
        generate_viral_content()

        # Step 4: Fetch and generate images for dashboard
        print("\n🖼️  STEP 4: Fetching dashboard images...")
        image_fetcher = ImageFetcher()
        topics = ['Tech', 'Politics', 'Business', 'Health', 'Entertainment', 'Science', 'International']
        image_fetcher.generate_images_json(topics)

        print(f"\n{'='*60}")
        print(f"✅ PIPELINE COMPLETE!")
        print(f"{'='*60}\n")

        print("📂 Output folders:")
        date_str = datetime.now().strftime('%Y%m%d')
        for country in active_countries:
            print(f"   {country}: output/viral_charts_{country.lower()}_{date_str}/")
        print(f"   Global: output/viral_charts_global_{date_str}/")

    except Exception as e:
        print(f"\n❌ ERROR: Pipeline failed!")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

# Schedule to run daily at 7 AM
schedule.every().day.at("07:00").do(daily_job)

# Or run immediately for testing
if __name__ == "__main__":
    print("🧪 Running pipeline now (test mode)...\n")
    exit_code = daily_job()

    # Uncomment below to run on schedule
    # print("\n⏰ Scheduler started. Waiting for 7 AM daily run...")
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)

    sys.exit(exit_code)
