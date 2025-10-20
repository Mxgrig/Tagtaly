"""RSS Feed Configuration - All active news sources"""

# All RSS feeds by country
RSS_FEEDS = {
    'UK': {
        'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
        'Guardian': 'https://www.theguardian.com/uk/rss',
        'Sky News': 'https://feeds.skynews.com/feeds/rss/uk.xml',
        'Telegraph': 'https://www.telegraph.co.uk/news/rss.xml',
        'Independent': 'https://www.independent.co.uk/news/uk/rss',
        'BBC Lifestyle': 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
        'Guardian Life': 'https://www.theguardian.com/uk/lifeandstyle/rss',
        'Telegraph Fashion': 'https://www.telegraph.co.uk/fashion/rss.xml',
        'Telegraph Travel': 'https://www.telegraph.co.uk/travel/rss.xml',
        'Metro Lifestyle': 'https://metro.co.uk/lifestyle/feed/',
        'Evening Standard Food': 'https://www.standard.co.uk/topic/food-drink/rss'
    },
    'US': {
        'CNN': 'http://rss.cnn.com/rss/cnn_topstories.rss',
        'NY Times': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'Washington Post': 'https://feeds.washingtonpost.com/rss/politics',
        'Fox News': 'https://moxie.foxnews.com/google-publisher/latest.xml',
        'NPR': 'https://feeds.npr.org/1001/rss.xml',
        'NY Times Style': 'https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml',
        'NY Times Travel': 'https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml',
        'CNN Entertainment': 'http://rss.cnn.com/rss/cnn_showbiz.rss',
        'NPR Food': 'https://feeds.npr.org/1053/rss.xml',
        'E! News': 'https://eonline.com/syndication/feeds/rssfeeds/topstories.xml',
        'US Magazine': 'https://www.usmagazine.com/feed/'
    }
}

# Global feeds (not country-specific)
GLOBAL_FEEDS = {
    'BBC World': 'http://feeds.bbci.co.uk/news/world/rss.xml',
    'Reuters': 'https://www.reuters.com/world/',
    'AP News': 'https://apnews.com/hub/ap-feeds'
}

def get_feeds_by_country(country_code):
    """Get all RSS feeds for a specific country"""
    return RSS_FEEDS.get(country_code.upper(), {})

def get_all_feeds():
    """Get all feeds combined"""
    all_feeds = {}
    for country, feeds in RSS_FEEDS.items():
        all_feeds.update(feeds)
    all_feeds.update(GLOBAL_FEEDS)
    return all_feeds

def get_feed_count():
    """Get total number of active feeds"""
    uk_count = len(RSS_FEEDS.get('UK', {}))
    us_count = len(RSS_FEEDS.get('US', {}))
    global_count = len(GLOBAL_FEEDS)
    return {
        'UK': uk_count,
        'US': us_count,
        'Global': global_count,
        'Total': uk_count + us_count + global_count
    }

if __name__ == '__main__':
    # Test feeds configuration
    print("RSS Feeds Configuration")
    print("=" * 50)
    counts = get_feed_count()
    print(f"UK Feeds: {counts['UK']}")
    print(f"US Feeds: {counts['US']}")
    print(f"Global Feeds: {counts['Global']}")
    print(f"Total Active Feeds: {counts['Total']}")
    print("\nFeeds are ready for collection!")
