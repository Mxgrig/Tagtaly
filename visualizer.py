# visualizer.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set your brand colors
BRAND_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'accent': '#2ca02c',
    'background': '#f8f9fa'
}

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_daily_report():
    conn = sqlite3.connect('uk_news.db')

    # Get today's articles
    today = datetime.now().date()
    df = pd.read_sql_query('''
        SELECT * FROM articles
        WHERE DATE(fetched_at) = ?
    ''', conn, params=(today,))

    if len(df) == 0:
        print("No articles found for today")
        return

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Tagtaly - {today.strftime("%B %d, %Y")}',
                 fontsize=20, fontweight='bold')

    # 1. Top Topics
    topic_counts = df['topic'].value_counts().head(7)
    axes[0, 0].barh(topic_counts.index, topic_counts.values, color=BRAND_COLORS['primary'])
    axes[0, 0].set_xlabel('Number of Articles')
    axes[0, 0].set_title('Top Topics Today', fontweight='bold')
    axes[0, 0].invert_yaxis()

    # 2. Sentiment Distribution
    sentiment_counts = df['sentiment'].value_counts()
    colors = {'positive': '#2ca02c', 'neutral': '#7f7f7f', 'negative': '#d62728'}
    axes[0, 1].pie(sentiment_counts.values, labels=sentiment_counts.index,
                   autopct='%1.1f%%', colors=[colors[s] for s in sentiment_counts.index])
    axes[0, 1].set_title('Overall Sentiment', fontweight='bold')

    # 3. Articles by Source
    source_counts = df['source'].value_counts()
    axes[1, 0].bar(source_counts.index, source_counts.values, color=BRAND_COLORS['secondary'])
    axes[1, 0].set_xlabel('News Source')
    axes[1, 0].set_ylabel('Articles Published')
    axes[1, 0].set_title('Coverage by Source', fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=45)

    # 4. Sentiment by Topic
    sentiment_topic = pd.crosstab(df['topic'], df['sentiment'])
    sentiment_topic_pct = sentiment_topic.div(sentiment_topic.sum(axis=1), axis=0) * 100
    sentiment_topic_pct.plot(kind='barh', stacked=True, ax=axes[1, 1],
                             color=[colors['negative'], colors['neutral'], colors['positive']])
    axes[1, 1].set_xlabel('Percentage')
    axes[1, 1].set_title('Sentiment by Topic', fontweight='bold')
    axes[1, 1].legend(title='Sentiment')

    plt.tight_layout()

    # Save with date stamp
    filename = f'uk_news_charts_{today}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Chart saved: {filename}")

    conn.close()

if __name__ == "__main__":
    create_daily_report()
