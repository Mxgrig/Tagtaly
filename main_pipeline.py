# main_pipeline.py
import schedule
import time
from news_collector import fetch_news
from news_analyzer import analyze_articles
from viral_engine import generate_viral_content

def daily_job():
    print(f"\n{'='*50}")
    print(f"Starting daily news pipeline...")
    print(f"{'='*50}\n")

    # Step 1: Fetch news
    fetch_news()

    # Step 2: Analyze
    analyze_articles()

    # Step 3: Generate viral charts
    generate_viral_content()

    print(f"\n{'='*50}")
    print(f"Pipeline complete!")
    print(f"{'='*50}\n")

# Schedule to run daily at 7 AM
schedule.every().day.at("07:00").do(daily_job)

# Or run immediately for testing
if __name__ == "__main__":
    print("Running pipeline now (test mode)...")
    daily_job()

    # Uncomment below to run on schedule
    # print("Scheduler started. Waiting for 7 AM daily run...")
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)
