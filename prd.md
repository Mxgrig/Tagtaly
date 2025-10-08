# 🏷️ Tagtaly - Product Requirements Document (PRD)

**Version:** 1.0  
**Last Updated:** October 2025  
**Owner:** Grig Ugwunze  
**Status:** In Development

---

## 1. Executive Summary

### 1.1 Product Vision
Tagtaly transforms UK news into viral, data-driven social media content by automatically analyzing 500+ articles daily, detecting dramatic story angles, and generating Instagram-ready charts that stop the scroll.

### 1.2 Problem Statement
- **For content creators:** Manually tracking news trends is time-consuming
- **For audiences:** News is overwhelming; data visualization makes it digestible
- **For businesses:** Monitoring media coverage requires expensive tools

### 1.3 Solution
A fully automated pipeline that:
1. Collects news from UK outlets (BBC, Guardian, Sky, etc.)
2. Analyzes topics, sentiment, and trends
3. Detects viral story angles using proprietary algorithms
4. Generates 3 mobile-optimized charts daily
5. Delivers them ready to post in 5 minutes

### 1.4 Success Metrics
- **Month 1:** Daily charts generated, 1K followers
- **Month 6:** 50K followers, first sponsor (£1.5K/month)
- **Month 12:** 100K followers, 3 sponsors + 2 B2B clients (£10K/month)
- **Month 18:** £15-20K/month revenue (sponsors + B2B + affiliate)

---

## 2. Product Goals & Objectives

### 2.1 Primary Goals
1. **Automate news analysis:** 0 hours/day spent reading articles
2. **Generate viral content:** 3 high-quality charts daily without manual work
3. **Build social audience:** Grow to 50K+ engaged followers
4. **Create revenue:** £10K+/month from sponsors, B2B clients, affiliates

### 2.2 Secondary Goals
1. Build proprietary historical news database
2. Establish "Tagtaly" as trusted UK news data brand
3. Create scalable B2B product (media monitoring dashboard)
4. Develop SEO-optimized website (tagtaly.com)

### 2.3 Non-Goals (Out of Scope for v1.0)
- ❌ Real-time breaking news alerts (batch processing only)
- ❌ Multiple countries (UK only)
- ❌ User-generated content
- ❌ Mobile app
- ❌ Paid API access (future: v2.0)

---

## 3. User Personas

### 3.1 Primary User: Content Creator (Grig)
**Who:** Social media creator building news commentary brand  
**Goals:** Post daily, grow followers, monetize  
**Pain Points:** Time-consuming research, inconsistent posting  
**Success:** 3 charts ready each morning, 2-minute posting workflow

### 3.2 Secondary User: B2B Client (Political Campaign)
**Who:** Political party/candidate campaign team  
**Goals:** Monitor media coverage, track opponent mentions  
**Pain Points:** Expensive monitoring tools, delayed insights  
**Success:** Real-time alerts, custom dashboards, weekly reports

### 3.3 Tertiary User: Website Visitor
**Who:** Data enthusiast searching Google for UK news charts  
**Goals:** Understand trends, cite data in work  
**Pain Points:** Can't find good visualizations  
**Success:** Find historical charts, explore archive

---

## 4. Core Features & Requirements

### 4.1 News Collection Engine

**Feature:** Automated RSS feed aggregation

**Requirements:**
- Fetch from 5+ UK news sources (BBC, Guardian, Sky, Telegraph, Independent)
- Run hourly or daily (configurable)
- Deduplicate articles by URL hash
- Extract: headline, summary, source, date, URL
- Store in SQLite database
- Handle feed failures gracefully (retry, skip, log)

**Acceptance Criteria:**
- ✅ Collect 200+ articles per day
- ✅ < 5% duplicate rate
- ✅ 0 crashes from malformed feeds
- ✅ Run time < 2 minutes

**Technical Specs:**
```python
# news_collector.py
FEEDS = {
    'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
    'Guardian': 'https://www.theguardian.com/uk/rss',
    'Sky News': 'https://feeds.skynews.com/feeds/rss/uk.xml',
    'Telegraph': 'https://www.telegraph.co.uk/news/rss.xml',
    'Independent': 'https://www.independent.co.uk/news/uk/rss'
}

# Database schema
articles (
    id TEXT PRIMARY KEY,
    headline TEXT NOT NULL,
    source TEXT NOT NULL,
    url TEXT NOT NULL,
    published_date TEXT,
    summary TEXT,
    fetched_at TEXT NOT NULL,
    topic TEXT,
    sentiment TEXT,
    sentiment_score REAL
)
```

---

### 4.2 Analysis Engine

**Feature:** Topic classification and sentiment analysis

**Requirements:**
- Classify articles into topics: Politics, Health, Economy, Crime, Energy, Education, Immigration, Housing, Transport
- Analyze sentiment: positive/negative/neutral with confidence score
- Extract entities: politicians, organizations, locations (future)
- Process 500+ articles in < 5 minutes
- Accuracy: 80%+ topic match vs manual review

**Acceptance Criteria:**
- ✅ All articles tagged within 5 minutes
- ✅ < 10% "Other" category
- ✅ Sentiment score -1.0 to +1.0 scale
- ✅ No crashes on edge cases (empty text, special chars)

**Technical Specs:**
```python
# news_analyzer.py
TOPICS = {
    'Politics': ['government', 'minister', 'parliament', 'starmer', 'sunak', ...],
    'Health': ['nhs', 'hospital', 'doctor', 'patient', ...],
    'Economy': ['inflation', 'interest rate', 'gdp', 'bank', ...],
    # ... 9 total topics
}

# Sentiment: TextBlob polarity -1 to +1
# Classification: Keyword matching (v1.0), ML later (v2.0)
```

---

### 4.3 Story Detection Engine (The Secret Sauce)

**Feature:** Identify most viral/shareable news angles

**Requirements:**
- Run 5 detection algorithms:
  1. **Topic Surge:** Compare this week vs last week, find % change
  2. **Political Scorecard:** Count mentions of 5+ politicians
  3. **Record Alerts:** Find "highest/lowest ever" phrases + numbers
  4. **Sentiment Shifts:** Detect mood changes by topic
  5. **Media Bias:** Compare outlet coverage focus
  
- Score each story by virality (0-20 scale)
- Return top 3 stories ranked by score
- Minimum data: 2 days history required

**Acceptance Criteria:**
- ✅ Generate 3+ stories per day
- ✅ Stories are factually accurate (verified vs source articles)
- ✅ Virality score correlates with actual engagement (test over time)
- ✅ No duplicate stories in same day

**Technical Specs:**
```python
# story_detector.py
class StoryDetector:
    def find_viral_angles(self) -> List[Story]:
        stories = [
            self.detect_topic_surge(),      # "Health UP 125%"
            self.track_political_mentions(), # "Starmer 7x vs Sunak"
            self.find_record_numbers(),      # "7.6M NHS record"
            self.detect_sentiment_shift(),   # "Mood turns negative"
            self.compare_outlet_focus()      # "BBC focuses on X"
        ]
        return sorted(stories, key=lambda x: x.virality_score, reverse=True)

# Virality scoring formula:
# Surge: abs(pct_change) / 10 (max 20)
# Political: ratio * 2 (max 20)
# Record: 15 + count (max 20)
# Sentiment: abs(change) * 20 (max 20)
# Bias: fixed 7
```

---

### 4.4 Visualization Engine

**Feature:** Generate mobile-optimized chart images

**Requirements:**
- Create 3 chart types:
  1. **Surge Alert:** Horizontal bars showing % change
  2. **Political Race:** Horizontal bars with mention counts
  3. **Record Highlight:** Giant number on colored background
  
- Mobile-first: 1080x1350px (Instagram portrait)
- Bold colors: Black background, white text, red accents
- Branding: "Tagtaly" watermark bottom-right
- Output: PNG with transparent/solid backgrounds
- Also generate: Text caption file with hashtags

**Acceptance Criteria:**
- ✅ 3 charts generated in < 30 seconds
- ✅ All text readable on mobile (16pt+ font)
- ✅ Files < 2MB each
- ✅ No visual artifacts or rendering errors

**Technical Specs:**
```python
# viral_viz.py
class ViralChartMaker:
    fig_size = (10.8, 13.5)  # Instagram portrait
    dpi = 100
    colors = {
        'background': '#000000',
        'text': '#FFFFFF',
        'surge': '#FF3B30',
        'drop': '#34C759'
    }
    
    def create_surge_alert(self, data) -> Figure
    def create_politician_race(self, data) -> Figure
    def create_record_highlight(self, data) -> Figure
```

---

### 4.5 Caption Generation

**Feature:** Auto-generate social media captions

**Requirements:**
- Extract headline from story
- Add context (1-2 sentences)
- Include branding line
- Add 4-6 relevant hashtags
- Character limits: Twitter 280, Instagram 2200, LinkedIn 3000
- Save as .txt file alongside PNG

**Acceptance Criteria:**
- ✅ Caption matches chart content
- ✅ No spelling/grammar errors
- ✅ Hashtags relevant to topic
- ✅ Fits platform limits

**Technical Specs:**
```python
# viral_engine.py
def generate_caption(story) -> str:
    caption = f"{emoji} {story['headline']}\n\n"
    caption += "UK news, counted & charted. "
    caption += "Follow @tagtaly for daily insights.\n\n"
    caption += f"#Tagtaly #UKNews #DataViz #{topic_tag}"
    return caption
```

---

### 4.6 Pipeline Orchestration

**Feature:** Run all steps in sequence automatically

**Requirements:**
- Single command: `python main_pipeline.py`
- Steps: Collect → Analyze → Detect → Visualize → Caption
- Error handling: Continue on non-fatal errors, log issues
- Output: Create `viral_charts_YYYYMMDD/` folder with 3 PNGs + 3 TXTs
- Logging: Print progress, time taken, summary stats
- Exit codes: 0 success, 1 failure

**Acceptance Criteria:**
- ✅ Complete run in < 10 minutes
- ✅ No user interaction required
- ✅ Graceful failure (partial results OK)
- ✅ Clear success/failure messaging

**Technical Specs:**
```python
# main_pipeline.py
def run_pipeline():
    print("TAGTALY - DAILY PIPELINE")
    
    # Step 1: Collect (2-3 min)
    new_articles = fetch_news()
    
    # Step 2: Analyze (2-3 min)
    analyze_articles()
    
    # Step 3: Generate (2-3 min)
    generate_viral_content()
    
    print("✅ PIPELINE COMPLETE")
    return True
```

---

## 5. Technical Architecture

### 5.1 System Overview

```
┌─────────────────────────────────────────────────────┐
│                   TAGTALY SYSTEM                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [RSS Feeds] → [Collector] → [Database]            │
│                                  ↓                  │
│                              [Analyzer]             │
│                                  ↓                  │
│                          [Story Detector]           │
│                                  ↓                  │
│                           [Visualizer]              │
│                                  ↓                  │
│                         [Output Folder]             │
│                                  ↓                  │
│                      [Manual Posting]               │
│                 (or Buffer/GitHub Actions)          │
└─────────────────────────────────────────────────────┘
```

### 5.2 Technology Stack

**Language:** Python 3.10+

**Core Libraries:**
- `feedparser` - RSS parsing
- `pandas` - Data manipulation
- `matplotlib` - Chart generation
- `textblob` - Sentiment analysis
- `sqlite3` - Database (built-in)
- `requests` - HTTP requests

**Optional:**
- `schedule` - Task scheduling (local)
- GitHub Actions - Cloud automation
- Buffer API - Social media posting

**Infrastructure:**
- Local: Developer laptop (development)
- GitHub Pages: Static website (future)
- GitHub Actions: Daily automation (free tier)

### 5.3 Data Flow

```
Input → Collection → Storage → Analysis → Detection → Visualization → Output

RSS → articles → uk_news.db → tagged articles → stories → charts → viral_charts_*/
```

### 5.4 File Structure

```
Tagtaly/
├── src/                     # Source code
│   ├── news_collector.py
│   ├── news_analyzer.py
│   ├── story_detector.py
│   ├── viral_viz.py
│   └── main_pipeline.py
├── data/
│   └── uk_news.db          # SQLite database
├── output/
│   └── viral_charts_*/     # Daily output folders
├── docs/                   # Documentation
│   ├── PRD.md
│   ├── README.md
│   └── SETUP.md
└── tests/                  # Unit tests (future)
```

---

## 6. Data Models

### 6.1 Article Schema

```sql
CREATE TABLE articles (
    id TEXT PRIMARY KEY,              -- MD5 hash of URL
    headline TEXT NOT NULL,           -- Article title
    source TEXT NOT NULL,             -- BBC, Guardian, etc.
    url TEXT NOT NULL,                -- Article URL
    published_date TEXT,              -- ISO 8601 format
    summary TEXT,                     -- First paragraph
    fetched_at TEXT NOT NULL,         -- When we collected it
    topic TEXT,                       -- Politics, Health, etc.
    sentiment TEXT,                   -- positive/neutral/negative
    sentiment_score REAL              -- -1.0 to +1.0
);

CREATE INDEX idx_fetched_at ON articles(fetched_at);
CREATE INDEX idx_topic ON articles(topic);
CREATE INDEX idx_source ON articles(source);
```

### 6.2 Story Schema (In-Memory)

```python
@dataclass
class Story:
    type: str                    # SURGE_ALERT, POLITICAL_SCORECARD, etc.
    headline: str                # "NHS news UP 125%"
    viz_type: str                # comparison_bars, race_chart, etc.
    data: pd.DataFrame           # Chart data
    virality_score: float        # 0-20
    metadata: dict               # Additional context
```

---

## 7. API & Integrations

### 7.1 RSS Feeds (Read-Only)

**Endpoints:**
- BBC: `http://feeds.bbci.co.uk/news/rss.xml`
- Guardian: `https://www.theguardian.com/uk/rss`
- Sky: `https://feeds.skynews.com/feeds/rss/uk.xml`
- Telegraph: `https://www.telegraph.co.uk/news/rss.xml`
- Independent: `https://www.independent.co.uk/news/uk/rss`

**Rate Limits:** None (RSS is pull-based)  
**Auth:** None required  
**Format:** XML (RSS 2.0)

### 7.2 Buffer API (Optional, Future)

**Purpose:** Semi-automated social posting  
**Endpoint:** `https://api.bufferapp.com/1/`  
**Auth:** OAuth 2.0 token  
**Rate Limit:** 100 requests/hour  
**Cost:** Free tier (10 posts)

### 7.3 GitHub API (Automation)

**Purpose:** Store code, run Actions, host Pages  
**Endpoint:** `https://api.github.com/`  
**Auth:** `GITHUB_TOKEN` (automatic in Actions)  
**Free Tier:** 2,000 minutes/month Actions

---

## 8. Development Phases

### Phase 1: MVP (Week 1-2) ✅ CURRENT
**Goal:** Basic pipeline working locally

- [x] News collector (5 sources)
- [x] Topic analyzer (9 topics)
- [x] Sentiment analysis (TextBlob)
- [x] Story detector (5 algorithms)
- [x] Chart generator (3 types)
- [x] Main pipeline orchestrator
- [ ] Update branding to "Tagtaly"
- [ ] Test end-to-end

**Deliverable:** 3 charts generated daily on local machine

---

### Phase 2: Automation (Week 3-4)
**Goal:** Zero manual intervention

- [ ] GitHub Actions workflow
- [ ] Daily automatic runs (7 AM UTC)
- [ ] Email notification with charts
- [ ] Database persistence in repo
- [ ] Error monitoring/alerts

**Deliverable:** Charts in inbox every morning

---

### Phase 3: Website (Month 2)
**Goal:** SEO-optimized archive at tagtaly.com

- [ ] Static site generator (Jekyll/Hugo)
- [ ] Homepage with latest chart
- [ ] Archive page (all charts)
- [ ] Topic pages (filter by topic)
- [ ] Search functionality
- [ ] Google Analytics
- [ ] AdSense integration

**Deliverable:** Live website with 60+ charts

---

### Phase 4: Monetization (Month 3-6)
**Goal:** First revenue stream

- [ ] Reach 10K followers
- [ ] Create sponsor deck
- [ ] Add affiliate links
- [ ] Pitch 10 potential sponsors
- [ ] Close first sponsor (£500-1,500/month)

**Deliverable:** £1,500/month revenue

---

### Phase 5: B2B Product (Month 6-12)
**Goal:** Enterprise clients

- [ ] Build monitoring dashboard (Streamlit)
- [ ] Custom keyword tracking
- [ ] Email alerts for clients
- [ ] Weekly reports
- [ ] API access (premium)
- [ ] Close 2-3 B2B clients (£5K/month)

**Deliverable:** £10K+/month total revenue

---

## 9. Success Metrics & KPIs

### 9.1 Product Metrics

**Daily Active:**
- Charts generated: 3/day (100% uptime target)
- Articles processed: 200-500/day
- Pipeline runtime: < 10 minutes
- Error rate: < 5%

**Weekly:**
- Database growth: +1,500 articles/week
- Chart archive: +21 charts/week
- Topics covered: 9 minimum

**Monthly:**
- Total articles: 6,000+
- Total charts: 90+
- Data retention: 12 months rolling

### 9.2 Business Metrics

**Audience Growth:**
- Month 1: 1,000 followers
- Month 3: 10,000 followers
- Month 6: 50,000 followers
- Month 12: 100,000 followers

**Engagement:**
- Likes per post: 1-2% of followers
- Shares: 0.1-0.5% of followers
- Comments: 10-50 per post
- Click-through (website): 2-5%

**Revenue:**
- Month 6: £1,500/month
- Month 12: £10,000/month
- Month 18: £20,000/month

### 9.3 Quality Metrics

**Accuracy:**
- Topic classification: 80%+ correct
- Sentiment analysis: 70%+ correct
- Story headlines: 100% factual
- Chart data: 0 errors

**User Satisfaction:**
- Time to post: < 5 minutes
- Manual intervention: 0 hours/day
- Chart quality: 8/10+ rating

---

## 10. Risks & Mitigations

### 10.1 Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| RSS feeds go down | High | Medium | Cache last fetch, retry logic, multiple sources |
| Database corruption | High | Low | Daily backups, GitHub version control |
| API rate limits | Medium | Low | Batch processing, respectful delays |
| Chart generation errors | Medium | Medium | Error handling, fallback templates |

### 10.2 Business Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| No audience growth | High | Medium | Test different content angles, collaborate with others |
| Can't monetize | High | Low | Multiple revenue streams (sponsors, B2B, affiliate) |
| Competitors copy | Medium | High | Keep algo private, build brand first-mover advantage |
| News sources paywall | Low | Medium | Switch to alternative sources, use public data |

### 10.3 Legal/Compliance Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Copyright issues | High | Low | Only use headlines/metadata, never full text, cite sources |
| Defamation claims | Medium | Very Low | Show data only, no editorial content, cite sources |
| Data privacy (GDPR) | Low | Very Low | No personal data collected |

---

## 11. Future Enhancements (v2.0+)

### Potential Features (Prioritized)

**High Priority:**
1. Real-time alerts (breaking news detection)
2. Historical trend analysis (month-over-month)
3. Entity extraction (tag specific people/orgs)
4. Animated charts (MP4 for Reels/TikTok)
5. A/B testing (multiple chart variants)

**Medium Priority:**
6. User dashboard (web UI)
7. Custom date range queries
8. Regional UK breakdown (England/Scotland/Wales)
9. API for third-party access
10. Slack/Discord bot integration

**Low Priority:**
11. Multi-country support (US, EU)
12. Predictive modeling (forecast trends)
13. AI-generated commentary
14. Mobile app
15. White-label for agencies

---

## 12. Appendix

### 12.1 Glossary

- **Tally:** Count or score of mentions/occurrences
- **Tag:** Classify or categorize (e.g., topic tag)
- **Virality Score:** 0-20 metric predicting social engagement
- **Surge:** Rapid increase in coverage (>50% week-over-week)
- **Sentiment:** Emotional tone (positive/negative/neutral)
- **RSS:** Really Simple Syndication (news feed format)

### 12.2 References

- TextBlob Documentation: https://textblob.readthedocs.io/
- GitHub Actions: https://docs.github.com/actions
- Buffer API: https://buffer.com/developers/api
- RSS 2.0 Spec: https://www.rssboard.org/rss-specification

### 12.3 Contact

**Product Owner:** Grig Ugwunze  
**Domain:** tagtaly.com  
**Repo:** github.com/grigugwunze/tagtaly (private)

---

**End of PRD v1.0**
