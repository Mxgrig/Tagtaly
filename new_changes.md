# Tagtaly Implementation Specification

**Version:** 2.0  
**Date:** October 2025  
**For:** Claude Code Implementation  
**Status:** Ready for Implementation

---

## Executive Summary

Tagtaly is evolving from UK-only news charts to a **multi-country (UK + US), engagement-focused** news analytics platform. The core principle: **Only track news that people actually care about and will engage with on social media.**

### Key Changes

1. **Multi-country support:** UK, US, and Global content
2. **Engagement-first topics:** Focus on cost of living, drama, and human impact
3. **Three content tiers:** Country-specific, Global, and Comparative
4. **Viral scoring:** Prioritize stories with high social media engagement potential

---

## 1. Project Structure

### Current Structure
```
Tagtaly/
├── main_pipeline.py
├── news_collector.py
├── news_analyzer.py
├── story_detector.py
├── viral_viz.py
├── viral_engine.py
├── social_publisher.py
├── visualizer.py
└── requirements.txt
```

### Required New Structure
```
Tagtaly/
├── config/                          # NEW FOLDER
│   ├── __init__.py
│   ├── countries.py                 # Country configurations
│   ├── viral_topics.py              # Engagement-focused topics
│   └── feeds.py                     # RSS feed URLs
│
├── src/                             # Move existing files here
│   ├── __init__.py
│   ├── news_collector.py            # UPDATE for multi-country
│   ├── news_analyzer.py             # UPDATE for viral topics
│   ├── story_detector.py            # UPDATE for global stories
│   ├── viral_viz.py                 # UPDATE for country flags
│   ├── viral_engine.py              # UPDATE for multi-output
│   └── main_pipeline.py             # UPDATE for orchestration
│
├── data/
│   └── tagtaly.db                   # Renamed from uk_news.db
│
├── output/
│   ├── viral_charts_uk_YYYYMMDD/    # UK-specific charts
│   ├── viral_charts_us_YYYYMMDD/    # US-specific charts
│   └── viral_charts_global_YYYYMMDD/ # Global charts
│
├── docs/
│   ├── PRD.md
│   ├── README.md
│   ├── SETUP.md
│   └── IMPLEMENTATION_SPEC.md       # This file
│
├── requirements.txt
└── .gitignore
```

---

## 2. Database Schema Updates

### Add New Fields to `articles` Table

```sql
-- New fields to add
ALTER TABLE articles ADD COLUMN country TEXT NOT NULL DEFAULT 'UK';
ALTER TABLE articles ADD COLUMN scope TEXT;  -- 'LOCAL', 'GLOBAL', or 'BOTH'
ALTER TABLE articles ADD COLUMN viral_score REAL DEFAULT 0;

-- Create new indexes
CREATE INDEX IF NOT EXISTS idx_country ON articles(country);
CREATE INDEX IF NOT EXISTS idx_scope ON articles(scope);
CREATE INDEX IF NOT EXISTS idx_viral_score ON articles(viral_score);

-- Rename database
-- uk_news.db → tagtaly.db
```

### Updated Schema
```sql
CREATE TABLE articles (
    id TEXT PRIMARY KEY,
    headline TEXT NOT NULL,
    source TEXT NOT NULL,
    url TEXT NOT NULL,
    published_date TEXT,
    summary TEXT,
    fetched_at TEXT NOT NULL,
    country TEXT NOT NULL,        -- NEW: 'UK', 'US', etc.
    scope TEXT,                    -- NEW: 'LOCAL', 'GLOBAL', 'BOTH'
    topic TEXT,
    sentiment TEXT,
    sentiment_score REAL,
    viral_score REAL DEFAULT 0     -- NEW: 0-100 engagement prediction
);
```

---

## 3. Configuration Files

### 3.1 Country Configuration (`config/countries.py`)

**Purpose:** Define RSS feeds, topics, and politicians for each country

**Key Components:**

```python
# Active countries toggle (easy on/off)
ACTIVE_COUNTRIES = ['UK', 'US']  # Can change to ['UK'] or ['US'] only

# Country structure
COUNTRIES = {
    'UK': {
        'name': 'United Kingdom',
        'flag': '🇬🇧',
        'timezone': 'Europe/London',
        'feeds': {...},           # RSS feed URLs
        'local_topics': {...},    # UK-specific topics
        'politicians': {...}      # UK politicians to track
    },
    'US': {...}
}

# Global topics (relevant to both countries)
GLOBAL_TOPICS = {
    'Climate': [...],
    'Tech': [...],
    'International': [...],
    'Royal Family': [...],
    'Entertainment': [...]
}
```

**RSS Feeds to Include:**

**UK:**
- BBC: `http://feeds.bbci.co.uk/news/rss.xml`
- Guardian: `https://www.theguardian.com/uk/rss`
- Sky News: `https://feeds.skynews.com/feeds/rss/uk.xml`
- Telegraph: `https://www.telegraph.co.uk/news/rss.xml`
- Independent: `https://www.independent.co.uk/news/uk/rss`

**US:**
- CNN: `http://rss.cnn.com/rss/cnn_topstories.rss`
- NY Times: `https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml`
- Washington Post: `https://feeds.washingtonpost.com/rss/politics`
- Fox News: `https://moxie.foxnews.com/google-publisher/latest.xml`
- NPR: `https://feeds.npr.org/1001/rss.xml`

**UK Lifestyle:**
- BBC Lifestyle: `http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml`
- Guardian Life & Style: `https://www.theguardian.com/uk/lifeandstyle/rss`
- Telegraph Fashion: `https://www.telegraph.co.uk/fashion/rss.xml`
- Telegraph Travel: `https://www.telegraph.co.uk/travel/rss.xml`
- Metro Lifestyle: `https://metro.co.uk/lifestyle/feed/`
- Evening Standard Food: `https://www.standard.co.uk/topic/food-drink/rss`

**US Lifestyle:**
- NY Times Style: `https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml`
- NY Times Travel: `https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml`
- CNN Entertainment: `http://rss.cnn.com/rss/cnn_showbiz.rss`
- NPR Food: `https://feeds.npr.org/1053/rss.xml`
- E! News: `https://eonline.com/syndication/feeds/rssfeeds/topstories.xml`
- People Magazine: `https://people.com/feeds/all-articles.rss`

---

### 3.2 Viral Topics Configuration (`config/viral_topics.py`)

**Purpose:** Define ONLY topics that get social media engagement

**Critical Principle:** If it doesn't make someone stop scrolling, don't track it.

**HIGH ENGAGEMENT Topics (Track These):**

```python
VIRAL_TOPICS = {
    # Tier 1: Personal Finance (Everyone cares)
    'Cost of Living': {
        'Energy Bills': ['energy bill', 'gas bill', 'electricity', 'heating costs'],
        'Food Prices': ['food price', 'grocery', 'tesco', 'sainsbury', 'weekly shop'],
        'Petrol': ['petrol price', 'diesel price', 'fuel cost'],
        'Rent & Housing': ['rent', 'house price', 'mortgage', 'landlord'],
        'Wages': ['wage', 'salary', 'pay rise', 'minimum wage', 'layoff']
    },
    
    # Tier 2: Drama & Scandals (Entertainment)
    'Corporate Drama': {
        'Collapses': ['bankruptcy', 'collapse', 'administration', 'goes bust'],
        'Scandals': ['ceo fired', 'fraud', 'scandal', 'investigation'],
        'Layoffs': ['layoff', 'job cuts', 'redundancy', 'closing'],
        'Greed': ['record profit', 'ceo pay', 'bonus', 'windfall profit']
    },
    
    # Tier 3: Tech Drama (Elon & Co.)
    'Tech Entertainment': {
        'Elon Musk': ['elon musk', 'musk', 'twitter', 'x corp', 'tesla'],
        'Big Tech': ['apple', 'google', 'meta', 'amazon', 'microsoft'],
        'AI': ['chatgpt', 'ai', 'openai', 'artificial intelligence'],
        'Crypto': ['bitcoin', 'crypto crash', 'ftx', 'cryptocurrency']
    },
    
    # Tier 4: Worker Power (Social justice)
    'Labor': {
        'Strikes': ['strike', 'industrial action', 'union', 'walkout'],
        'Conditions': ['amazon warehouse', 'gig economy', 'zero hours']
    }
}
```

**LOW ENGAGEMENT Topics (IGNORE These):**

```python
BORING_TOPICS = {
    # Do NOT track these - they get no engagement
    'earnings_reports': False,     # "Apple Q3 earnings beat expectations"
    'stock_indices': False,        # "FTSE 100 up 0.3%"
    'analyst_ratings': False,      # "Goldman upgrades to Buy"
    'market_forecasts': False,     # "UK growth forecast revised"
    'mergers': False,              # Unless dramatic/affects consumers
    'dividends': False             # "Company announces dividend"
}
```

---

## 4. Code Changes Required

### 4.1 News Collector (`src/news_collector.py`)

**Changes:**

1. Import country configuration
2. Fetch news for each active country
3. Tag articles with country code
4. Save to `tagtaly.db` (renamed from `uk_news.db`)

**Key Functions:**

```python
from config.countries import get_country_config, get_active_countries

def fetch_news_for_country(country_code, conn):
    """Fetch news for specific country"""
    config = get_country_config(country_code)
    
    for source, url in config['feeds'].items():
        # Fetch and parse RSS
        # Create unique ID: hash(country + url)
        article_id = hashlib.md5(f"{country_code}:{url}".encode()).hexdigest()
        
        # Insert with country tag
        conn.execute('''INSERT INTO articles 
            (id, headline, source, url, ..., country)
            VALUES (?, ?, ?, ?, ..., ?)''',
            (..., country_code))

def fetch_news():
    """Fetch from all active countries"""
    for country in get_active_countries():
        fetch_news_for_country(country, conn)
```

---

### 4.2 News Analyzer (`src/news_analyzer.py`)

**Changes:**

1. Classify articles as LOCAL vs GLOBAL
2. Use country-specific keywords for local topics
3. Use global keywords for universal topics
4. Calculate viral score based on engagement factors

**Key Functions:**

```python
from config.countries import get_country_config, get_global_topics
from config.viral_topics import VIRAL_TOPICS, is_socially_viral

def classify_article_scope(text):
    """Determine if article is LOCAL or GLOBAL"""
    # Check if matches global topics
    global_matches = count_keyword_matches(text, get_global_topics())
    
    if global_matches >= 2:
        return 'GLOBAL'
    else:
        return 'LOCAL'

def classify_topic(text, country_code):
    """Classify with country-specific OR global keywords"""
    
    # First check global topics
    for topic, keywords in get_global_topics().items():
        if matches(text, keywords):
            return topic
    
    # Then check country-specific
    config = get_country_config(country_code)
    for topic, keywords in config['local_topics'].items():
        if matches(text, keywords):
            return topic
    
    return 'Other'

def calculate_viral_score(headline, summary):
    """Calculate 0-100 engagement prediction"""
    is_viral, score, reason = is_socially_viral(headline, summary)
    return score
```

---

### 4.3 Story Detector (`src/story_detector.py`)

**Changes:**

1. Detect stories per country AND globally
2. Filter stories by viral score (must be >= 5)
3. Create comparison stories (UK vs US)

**New Story Types:**

```python
class StoryDetector:
    def __init__(self, country=None):
        self.country = country  # None = global stories
        self.conn = sqlite3.connect('tagtaly.db')
    
    def find_viral_angles(self):
        """Find stories, filtered by country and viral score"""
        
        if self.country:
            # Country-specific stories
            stories = self.detect_local_stories(self.country)
        else:
            # Global stories
            stories = self.detect_global_stories()
        
        # Filter by viral score
        stories = [s for s in stories if s.get('viral_score', 0) >= 5]
        
        return sorted(stories, key=lambda x: x['viral_score'], reverse=True)
    
    def detect_global_stories(self):
        """Stories that work for BOTH UK and US audiences"""
        # Example: "Climate coverage in UK vs US"
        # Example: "Elon Musk mentioned X times globally"
        pass
    
    def detect_comparison_stories(self):
        """UK vs US comparison stories"""
        # Example: "UK vs US immigration coverage"
        # Example: "Who's more obsessed with climate?"
        pass
```

---

### 4.4 Viral Viz (`src/viral_viz.py`)

**Changes:**

1. Add country flag emoji to charts
2. Support comparison charts (UK vs US)
3. Update branding from "UK News in Charts" to "Tagtaly"

**Key Updates:**

```python
class ViralChartMaker:
    def create_surge_alert(self, story_data, country=None):
        """Create chart with optional country flag"""
        
        # Add country flag to title
        if country:
            config = get_country_config(country)
            flag = config['flag']
            title = f"{flag} {story_data['headline']}"
        else:
            title = f"🌍 {story_data['headline']}"  # Global
        
        # Update branding
        ax.text(0.98, 0.02, 'Tagtaly',  # Not "UK News in Charts"
               transform=ax.transAxes, ...)
    
    def create_comparison_chart(self, uk_data, us_data, topic):
        """NEW: Create UK vs US comparison chart"""
        # Shows both countries side by side
        pass
```

---

### 4.5 Viral Engine (`src/viral_engine.py`)

**Changes:**

1. Generate charts for each country separately
2. Generate global charts
3. Create comparison charts
4. Update captions with country-specific hashtags

**Output Structure:**

```python
def generate_viral_content():
    """Generate charts for all active countries + global"""
    
    active_countries = get_active_countries()
    
    # Generate country-specific charts
    for country in active_countries:
        detector = StoryDetector(country=country)
        stories = detector.find_viral_angles()
        
        output_dir = f"viral_charts_{country.lower()}_{date}"
        create_charts(stories[:3], output_dir, country)
    
    # Generate global charts
    global_detector = StoryDetector(country=None)
    global_stories = global_detector.find_viral_angles()
    
    output_dir = f"viral_charts_global_{date}"
    create_charts(global_stories[:4], output_dir, 'GLOBAL')

def generate_caption(story, country):
    """Generate country-specific caption"""
    
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
    
    return f"{emoji} TAGTALY: {story['headline']}\n\n{story['context']}\n\n{hashtags}"
```

---

### 4.6 Main Pipeline (`src/main_pipeline.py`)

**Changes:**

1. Import country configuration
2. Show which countries are active
3. Report output locations per country

**Updated Flow:**

```python
def run_pipeline():
    """Run for all active countries"""
    
    active_countries = get_active_countries()
    print(f"Active countries: {', '.join(active_countries)}")
    
    # Step 1: Collect (all countries)
    fetch_news()
    
    # Step 2: Analyze (all countries)
    analyze_articles()
    
    # Step 3: Generate (per country + global)
    generate_viral_content()
    
    # Show output
    for country in active_countries:
        print(f"   {country}: viral_charts_{country.lower()}_{date}/")
    print(f"   Global: viral_charts_global_{date}/")
```

---

## 5. Content Strategy Implementation

### 5.1 Weekly Posting Schedule

```python
POSTING_SCHEDULE = {
    'Monday': {
        'source': 'UK',
        'focus': 'Politics or Cost of Living'
    },
    'Tuesday': {
        'source': 'US',
        'focus': 'Politics or Cost of Living'
    },
    'Wednesday': {
        'source': 'GLOBAL',
        'focus': 'Tech, Climate, or International'
    },
    'Thursday': {
        'source': 'UK',
        'focus': 'Economy, Health, or Drama'
    },
    'Friday': {
        'source': 'US',
        'focus': 'Economy, Healthcare, or Drama'
    },
    'Saturday': {
        'source': 'GLOBAL',
        'focus': 'Royal Family, Entertainment, Science'
    },
    'Sunday': {
        'source': 'COMPARISON',
        'focus': 'UK vs US on same topic'
    }
}
```

### 5.2 Topic Priority

```python
TOPIC_WEIGHTS = {
    # Higher weight = more important to cover
    'Cost of Living': 10,      # Highest priority
    'Corporate Drama': 8,
    'Tech Entertainment': 7,
    'Labor Action': 6,
    'Climate': 5,
    'International': 4,
    'Royal Family': 3,
    'Other': 1
}
```

---

## 6. Viral Scoring Algorithm

### 6.1 Scoring Factors

```python
def calculate_viral_score(headline, summary):
    """
    Score: 0-100 (higher = more viral)
    Threshold: >= 5 to be considered for posting
    """
    
    text = f"{headline} {summary}".lower()
    score = 0
    
    # Personal impact (+10)
    if any(word in text for word in ['your', 'you', 'families', 'people']):
        score += 10
    
    # Big numbers (+5)
    if any(word in text for word in ['billion', 'million', 'thousands']):
        score += 5
    
    # Records (+15)
    if any(word in text for word in ['record', 'highest ever', 'lowest', 'worst']):
        score += 15
    
    # Emotion words (+8)
    if any(word in text for word in ['crisis', 'shock', 'scandal', 'outrage']):
        score += 8
    
    # Villains (+6)
    if any(word in text for word in ['ceo', 'company', 'corporation']):
        score += 6
    
    # Topic multipliers
    for topic, weight in TOPIC_WEIGHTS.items():
        if topic_matches(text, topic):
            score *= (weight / 5)  # Multiply by topic importance
    
    return min(score, 100)  # Cap at 100
```

### 6.2 Filtering Rules

```python
def should_post(article):
    """Final decision: post or skip?"""
    
    viral_score = article['viral_score']
    topic = article['topic']
    
    # Minimum viral score
    if viral_score < 5:
        return False, "Viral score too low"
    
    # Block boring topics even with decent scores
    if topic in ['Other', 'Generic Business']:
        if viral_score < 15:  # Need very high score
            return False, "Boring topic"
    
    # Require higher scores for less popular topics
    if topic in ['International', 'Science']:
        if viral_score < 10:
            return False, "Niche topic needs higher score"
    
    return True, "Approved for posting"
```

---

## 7. Migration Steps

### Phase 1: Setup (Week 1)

1. Create `config/` folder and files
2. Rename `uk_news.db` to `tagtaly.db`
3. Run database migration (add columns)
4. Update `requirements.txt` if needed

### Phase 2: Core Updates (Week 2)

1. Update `news_collector.py` for multi-country
2. Update `news_analyzer.py` for viral topics
3. Test with `ACTIVE_COUNTRIES = ['UK']` first

### Phase 3: Multi-Country (Week 3)

1. Update `story_detector.py` for global stories
2. Update `viral_viz.py` for country flags
3. Update `viral_engine.py` for multi-output
4. Test with `ACTIVE_COUNTRIES = ['UK', 'US']`

### Phase 4: Validation (Week 4)

1. Run full pipeline
2. Verify output folders created correctly
3. Check viral scores are calculated
4. Validate charts have correct branding

---

## 8. Testing Checklist

```markdown
### Database
- [ ] `tagtaly.db` created with new schema
- [ ] Articles have `country`, `scope`, `viral_score` fields
- [ ] Indexes created on new fields

### Collection
- [ ] Fetches from UK feeds
- [ ] Fetches from US feeds
- [ ] Articles tagged with correct country
- [ ] No duplicate articles

### Analysis
- [ ] Topics classified correctly
- [ ] Global vs local scope detected
- [ ] Viral scores calculated
- [ ] High scores for engaging content (energy bills, Elon, etc.)
- [ ] Low scores for boring content (earnings reports, etc.)

### Story Detection
- [ ] UK-specific stories found
- [ ] US-specific stories found
- [ ] Global stories found
- [ ] Stories filtered by viral score >= 5

### Visualization
- [ ] UK charts have 🇬🇧 flag
- [ ] US charts have 🇺🇸 flag
- [ ] Global charts have 🌍 icon
- [ ] Branding says "Tagtaly" not "UK News in Charts"

### Output
- [ ] `viral_charts_uk_YYYYMMDD/` created
- [ ] `viral_charts_us_YYYYMMDD/` created
- [ ] `viral_charts_global_YYYYMMDD/` created
- [ ] Each folder has 3-4 charts
- [ ] Caption files generated with correct hashtags
```

---

## 9. Configuration Toggle

**Easy switching between modes:**

```python
# In config/countries.py

# UK only (start here)
ACTIVE_COUNTRIES = ['UK']

# Add US (after UK works)
ACTIVE_COUNTRIES = ['UK', 'US']

# Just US (if pivoting)
ACTIVE_COUNTRIES = ['US']

# Future: Add more
ACTIVE_COUNTRIES = ['UK', 'US', 'CA', 'AU']
```

**No code changes needed - just edit this one line!**

---

## 10. Success Metrics

### Engagement Targets

```python
ENGAGEMENT_TARGETS = {
    'Cost of Living posts': {
        'likes': 2000,
        'shares': 500,
        'comments': 50
    },
    'Drama posts': {
        'likes': 3000,
        'shares': 800,
        'comments': 100
    },
    'Global posts': {
        'likes': 2500,
        'shares': 600,
        'comments': 75
    },
    'Comparison posts': {
        'likes': 4000,
        'shares': 1000,
        'comments': 150
    }
}
```

### Quality Metrics

```python
QUALITY_TARGETS = {
    'viral_score_avg': 15,      # Average across all stories
    'high_score_ratio': 0.3,    # 30% of stories score >= 20
    'boring_filter_rate': 0.7   # Filter out 70% of boring stories
}
```

---

## 11. File-by-File Implementation Order

1. ✅ Create `config/countries.py`
2. ✅ Create `config/viral_topics.py`
3. ✅ Update `news_collector.py` (multi-country)
4. ✅ Update `news_analyzer.py` (viral scoring)
5. ✅ Update `story_detector.py` (global detection)
6. ✅ Update `viral_viz.py` (country flags)
7. ✅ Update `viral_engine.py` (multi-output)
8. ✅ Update `main_pipeline.py` (orchestration)
9. ✅ Test end-to-end
10. ✅ Deploy

---

## 12. Critical Don'ts

**DO NOT:**

❌ Track boring business news (earnings, stock movements)  
❌ Create charts people won't engage with  
❌ Use "UK News in Charts" branding (it's "Tagtaly" now)  
❌ Post without calculating viral score  
❌ Mix countries in same database without `country` field  
❌ Assume people care about stocks/markets (they don't)  

**DO:**

✅ Focus on cost of living (everyone cares)  
✅ Track drama and scandals (entertainment value)  
✅ Include Elon Musk (he's a reality TV show)  
✅ Show human impact (job losses, bill increases)  
✅ Use country flags for clarity (🇬🇧🇺🇸🌍)  
✅ Calculate viral scores for everything  

---

## 13. Dependencies

No new dependencies needed! Everything uses existing packages:

```txt
feedparser==6.0.10
pandas==2.1.4
matplotlib==3.8.2
seaborn==0.13.0
textblob==0.17.1
pillow==10.1.0
requests==2.31.0
```

---

## 14. Rollback Plan

If multi-country doesn't work:

```python
# In config/countries.py
ACTIVE_COUNTRIES = ['UK']  # Back to UK-only

# Database still works (country field defaults to 'UK')
# All charts revert to UK-only output
# Zero code changes needed
```

---

## End of Specification

**This document provides everything Claude Code needs to implement the multi-country, engagement-focused version of Tagtaly.**

**Start implementation with Phase 1 (Setup) and proceed sequentially through the phases.**

**Questions? Check PRD.md for strategic context or refer back to this spec for technical details.**
