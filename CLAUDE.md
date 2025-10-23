# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Tagtaly** - "News That Matters. Data That Shows It."

An automated UK news analysis pipeline that transforms 500+ daily articles into viral social media visualizations. The system collects news from RSS feeds, analyzes topics and sentiment, detects dramatic story angles, and generates 3 Instagram-ready charts automatically.

**Tech Stack:** Python 3.10+, SQLite, pandas, matplotlib, TextBlob, feedparser

**Status:** 🚀 **Live in Production** (Phase 2 - Automation Complete)
- **Live URL:** [www.tagtaly.com](https://www.tagtaly.com) (custom domain)
- **Backup URL:** [tagtaly.dev.pages](https://tagtaly.dev.pages) (Cloudflare Pages)
- **Automation:** Cron jobs configured for daily execution (see Deployment section)

# GitHub Setup
## Two-Repository Architecture
- **#tagtaly** (PRIVATE): Stores source code, Python pipeline, GitHub Actions, secrets, and automation workflows
- **#tagtaly-pages** (PUBLIC): Serves static pages, points to custom domain www.tagtaly.com via Cloudflare Pages

## Workflow
1. `#tagtaly` repo runs GitHub Actions at 7 AM UTC → generates JSON charts
2. Commits generated data to `#tagtaly-pages` repo
3. `#tagtaly-pages` automatically deployed to www.tagtaly.com via Cloudflare Pages

---

## Current Deployment Plan (Phase 3 - In Progress)

**Goal:** Automated daily data generation with custom domain deployment

### Architecture
```
#tagtaly (PRIVATE)
  ↓ GitHub Actions (7 AM UTC)
  ↓ Runs Python pipeline
  ↓ Generates JSON charts
  ↓ Commits to #tagtaly-pages
  ↓
#tagtaly-pages (PUBLIC)
  ↓ Cloudflare Pages
  ↓ Auto-deployed to www.tagtaly.com
  ↓
www.tagtaly.com (LIVE ✅)
```

### Repository Structure
**#tagtaly (PRIVATE)** stores:
- Python source code (news_collector.py, viral_engine.py, etc.)
- Configuration files (config/)
- GitHub Actions workflows (.github/workflows/)
- Secrets and API keys (.env)
- SQLite database (uk_news.db)

**#tagtaly-pages (PUBLIC)** stores:
- HTML files (index.html, about.html, privacy.html)
- Static assets (assets/, social_charts.js)
- Generated JSON chart data (from #tagtaly GitHub Actions)
- CNAME file pointing to www.tagtaly.com

### Recent Changes ✅
- ✅ Created `json_generator.py` - converts story data to ECharts JSON
- ✅ Updated `viral_engine.py` - uses JSON generation instead of PNG
- ✅ Enhanced `news_collector.py` - retry logic + error logging for RSS feeds
- ✅ Added dual-chart hover in `social_charts.js` - ECharts with variants
- ✅ Two-repository split (#tagtaly private, #tagtaly-pages public)

### Current Status
- ✅ **GitHub Actions Workflow:** Generates JSON daily, pushes to #tagtaly-pages
- ✅ **Custom Domain:** www.tagtaly.com points to #tagtaly-pages via Cloudflare
- ✅ **Cloudflare Pages:** Auto-deploys from #tagtaly-pages repo
- ⏳ **Local Testing:** Verify JSON output matches expected format

---

## Repository Access
**#tagtaly** (Private)
- Contains: Python pipeline, configs, secrets
- Workflow: GitHub Actions runs daily, commits JSON to #tagtaly-pages
- Access: Private (Grig's account)

**#tagtaly-pages** (Public)
- Contains: Static HTML, assets, generated JSON
- Deployment: Cloudflare Pages auto-deploys on push
- Domain: www.tagtaly.com via CNAME
- Access: Public (read-only for viewers)

## Common Commands

### Development
```bash
# Run full pipeline (test mode - runs immediately)
python main_pipeline.py

# Run individual steps
python news_collector.py    # Fetch 200+ articles from UK news sources
python news_analyzer.py      # Classify topics and analyze sentiment
python viral_engine.py       # Detect stories and create charts
```

### Setup & Installation
```bash
# Quick setup (creates venv, installs deps)
chmod +x setup.sh
./setup.sh

# Quick daily run (checks deps, runs pipeline)
chmod +x run.sh
./run.sh

# Manual installation
python3 -m venv venv
source venv/bin/activate
pip install feedparser pandas matplotlib seaborn textblob schedule requests
python -m textblob.download_corpora
```

### Testing Individual Components
```bash
# Test news collection only
python news_collector.py

# Test analysis only (requires articles in database)
python news_analyzer.py

# Test visualization only (requires analyzed articles)
python viral_engine.py
```

### Database Inspection
```bash
# Open SQLite database
sqlite3 uk_news.db

# Common queries
SELECT COUNT(*) FROM articles;
SELECT topic, COUNT(*) FROM articles GROUP BY topic;
SELECT * FROM articles WHERE DATE(fetched_at) = DATE('now') LIMIT 5;
```

## Architecture

### Pipeline Flow
```
RSS Feeds → Collector → Database → Analyzer → Story Detector → Visualizer → Output
```

**Step-by-step execution:**
1. `news_collector.py`: Fetches from 5 RSS feeds, deduplicates by URL hash, stores in `uk_news.db`
2. `news_analyzer.py`: Classifies topics (9 categories), analyzes sentiment (TextBlob), updates database
3. `story_detector.py`: Runs 5 algorithms to find viral angles, scores stories by virality (0-20)
4. `viral_viz.py`: Generates 3 chart types (surge alerts, political scorecards, record highlights)
5. `viral_engine.py`: Orchestrates story detection + visualization, creates captions
6. Output: `viral_charts_YYYYMMDD/` folder with PNGs and caption TXT files

### Core Components

**news_collector.py** - RSS Feed Aggregation
- Fetches from BBC, Guardian, Sky News, Independent
- Creates MD5 hash from URL for deduplication
- Stores: headline, source, url, published_date, summary, fetched_at
- Database: SQLite (`uk_news.db`)

**news_analyzer.py** - Topic Classification & Sentiment Analysis
- Topics: Politics, Economy, Crime, Health, Energy (9 total)
- Classification: Keyword matching (fast, no ML dependencies)
- Sentiment: TextBlob polarity (-1.0 to +1.0)
- Updates articles table with: topic, sentiment, sentiment_score

**story_detector.py** - Viral Angle Detection (The Secret Sauce)
- **5 Detection Algorithms:**
  1. `detect_topic_surge()`: Week-over-week % change comparison
  2. `track_political_mentions()`: Count mentions of 4 key politicians
  3. `find_record_numbers()`: Extract "highest/lowest/record" phrases
  4. `detect_sentiment_shift()`: Mood change detection by topic
  5. `compare_outlet_focus()`: Media bias tracking (what each outlet covers)
- Returns top 3 stories ranked by virality score

**viral_viz.py** - Chart Generation Engine
- **3 Chart Types:**
  1. Surge Alert: Horizontal bars showing % change (red/green color coding)
  2. Political Race: Horizontal bars with mention counts
  3. Record Highlight: Giant number on colored background
- Design: Mobile-first (1080x1350px Instagram portrait), black background, white text
- Branding: "Tagtaly" watermark bottom-right

**viral_engine.py** - Orchestration & Caption Generation
- Coordinates story detection + visualization
- Generates social media captions with emojis and hashtags
- Creates output folder: `viral_charts_YYYYMMDD/`
- Outputs: 3 PNGs + 3 caption TXT files

**main_pipeline.py** - Pipeline Orchestrator
- Runs all steps in sequence
- Test mode: Executes immediately when run
- Scheduler mode: Can run daily at 7 AM (commented out, use for production)
- Exit codes: 0 success, 1 failure

### Data Model

**articles table schema:**
```sql
CREATE TABLE articles (
    id TEXT PRIMARY KEY,              -- MD5 hash of URL
    headline TEXT NOT NULL,
    source TEXT NOT NULL,             -- BBC, Guardian, Sky, Independent
    url TEXT NOT NULL,
    published_date TEXT,              -- ISO 8601
    summary TEXT,
    fetched_at TEXT NOT NULL,         -- ISO 8601
    topic TEXT,                       -- Politics, Health, Economy, etc.
    sentiment TEXT,                   -- positive, neutral, negative
    sentiment_score REAL              -- -1.0 to +1.0
);
```

**Story object (in-memory):**
```python
{
    'type': 'SURGE_ALERT' | 'POLITICAL_SCORECARD' | 'RECORD_ALERT' | ...,
    'headline': str,                  # "NHS news UP 125% this week"
    'viz_type': str,                  # comparison_bars, race_chart, etc.
    'data': pd.DataFrame,             # Chart data
    'virality_score': float,          # 0-20
    'metadata': dict
}
```

## Code Patterns & Conventions

### Database Access
- Always use context managers or explicit close() calls
- Connection string: `sqlite3.connect('uk_news.db')`
- Use pandas `read_sql_query()` for data retrieval
- Add `ALTER TABLE` columns with try/except to handle existing columns

### Error Handling
- RSS feed failures: Continue processing other sources, log errors
- Malformed articles: Skip with try/except, don't crash pipeline
- Missing data: Graceful fallbacks (e.g., empty string for missing summary)
- Story detector: Return empty/default story if insufficient data

### File Output
- Output folders: `viral_charts_YYYYMMDD/` format
- Chart files: `viral_{1-3}_{TYPE}.png`
- Caption files: `viral_{1-3}_{TYPE}_caption.txt`
- Chart size: 1080x1350px (Instagram portrait), DPI 100
- File size target: < 2MB per PNG

### Styling & Branding
- Brand colors defined in `viral_viz.py`:
  - Background: `#000000` (black)
  - Text: `#FFFFFF` (white)
  - Surge: `#FF3B30` (red)
  - Drop: `#34C759` (green)
  - Neutral: `#8E8E93` (gray)
- Font sizes: 16pt+ for mobile readability
- Always include "Tagtaly" branding watermark

## Development Workflow

### Adding New News Sources
1. Add RSS feed URL to `FEEDS` dict in `news_collector.py`
2. Test feed parsing: `python news_collector.py`
3. Verify articles in database: `sqlite3 uk_news.db "SELECT * FROM articles WHERE source='NewSource'"`

### Adding New Topics
1. Add topic keywords to `TOPICS` dict in `news_analyzer.py`
2. Update topic classification logic if needed
3. Re-analyze existing articles: Delete topic column and run analyzer

### Creating New Story Detection Algorithms
1. Add method to `StoryDetector` class in `story_detector.py`
2. Query database for relevant data (use pandas)
3. Calculate virality_score (0-20 scale)
4. Return story dict with type, headline, data, score
5. Add to `find_viral_angles()` method
6. Create corresponding chart type in `viral_viz.py`

### Modifying Chart Designs
1. Edit methods in `ViralChartMaker` class in `viral_viz.py`
2. Update colors in `self.colors` dict
3. Adjust figure size: `self.fig_size = (width, height)` in inches
4. Test chart generation: `python viral_engine.py`
5. Check output files are < 2MB

## Automation & Deployment

### Production Deployment (Live)
- **Data Generation:** #tagtaly repo (GitHub Actions)
- **Platform:** Cloudflare Pages (serves #tagtaly-pages repo)
- **Primary Domain:** www.tagtaly.com (CNAME in #tagtaly-pages)
- **Backup Domain:** tagtaly.dev.pages (Cloudflare Pages default)
- **Execution:** Automated via GitHub Actions in #tagtaly
- **Flow:** #tagtaly Actions → generates JSON → pushes to #tagtaly-pages → Cloudflare deploys

### GitHub Actions Workflow **#tagtaly**
Automated daily execution at 7 AM UTC:
```bash
# Workflow summary:
1. Install dependencies
2. Run Python pipeline (news_collector.py → analyzer → story_detector → viral_engine)
3. Generate JSON charts via json_generator.py
4. Commit JSON files to #tagtaly-pages repo
5. Cloudflare Pages auto-deploys to www.tagtaly.com
```

Details:
- **Schedule:** 7 AM UTC daily
- **Logs:** Available in GitHub Actions tab of #tagtaly
- **Output:** JSON files in #tagtaly-pages/data/ directory
- **Database:** Persisted in #tagtaly for version control
- **GitHub sync:** Automatic push to #tagtaly-pages after each run

### GitHub Actions (Primary Automation) **#tagtaly**
- Workflow file: `.github/workflows/daily-workflow.yml` in #tagtaly
- Runs daily at 7 AM UTC
- Triggers Python pipeline to generate JSON charts
- Commits results to #tagtaly-pages
- Manual trigger: workflow_dispatch event available

### Local Development Scheduling
For testing locally, uncomment scheduler code in `main_pipeline.py`:
```python
# Schedule to run daily at 7 AM
schedule.every().day.at("07:00").do(daily_job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Production Monitoring

### Checking Cron Job Status
```bash
# View cron job logs
tail -f logs/pipeline.log

# Check last execution
tail -n 50 logs/pipeline.log

# Search for errors
grep "ERROR\|Exception\|Traceback" logs/pipeline.log
```

### Verifying Daily Runs
```bash
# Check if output folders are being created
ls -lh output/viral_charts_*/

# List today's output
ls -lh output/viral_charts_*_$(date +%Y%m%d)/

# Verify database is being updated
sqlite3 uk_news.db "SELECT MAX(fetched_at) FROM articles;"
```

### Common Production Issues
- **Cron not running**: Check server time and timezone
- **Output not syncing to GitHub**: Verify Git credentials and push configuration
- **Database locked**: Ensure no multiple cron instances (check `ps aux | grep python`)
- **Low disk space**: Monitor `logs/` and `output/` directory sizes
- **Missing dependencies**: SSH to server and run `pip install -r requirements.txt`

## Troubleshooting

### "No module named 'feedparser'"
Dependencies not installed. Run: `pip install -r requirements.txt`

### "No articles found for today"
- RSS feeds may be down or slow
- Check internet connection
- Try running `news_collector.py` separately
- Verify database: `sqlite3 uk_news.db "SELECT COUNT(*) FROM articles"`

### "Database is locked"
Multiple processes accessing database. Close other connections or wait.

### Charts not generating
- Requires at least 2 days of data for comparisons
- Check if articles are analyzed: `SELECT COUNT(*) FROM articles WHERE topic IS NOT NULL`
- Run analyzer: `python news_analyzer.py`
- Check for errors in console output

### Empty or incomplete charts
- Verify data exists for story type
- Check virality_score > 0
- Review story detector logic for edge cases
- Test individual chart methods in `viral_viz.py`

## Important Notes

### Data Requirements
- Minimum 2 days of historical data for week-over-week comparisons
- Topic surge detection requires 14 days for accurate trends
- Database grows ~6,000 articles/month (~1-2 MB)

### Performance
- Full pipeline: < 10 minutes typical
- News collection: 2-3 minutes
- Analysis: 2-3 minutes (depends on new articles)
- Chart generation: < 30 seconds

### Dependencies
Required Python packages (install via `requirements.txt`):
- feedparser (RSS parsing)
- pandas (data manipulation)
- matplotlib (chart generation)
- seaborn (chart styling)
- textblob (sentiment analysis)
- schedule (task scheduling)
- requests (HTTP, optional for social posting)

### Project Status
**Current phase: Phase 2 (Automation Complete)** - Live in production ✅

**Phase 1 - MVP** (Complete)
- ✅ News collector (22 RSS feeds, multi-country)
- ✅ Topic analyzer (global + country-specific topics)
- ✅ Sentiment analysis (TextBlob integration)
- ✅ Story detector (5 algorithms with 0-100 virality scoring)
- ✅ Chart generator (6 visualization types)
- ✅ Branding update to "Tagtaly"
- ✅ End-to-end testing

**Phase 2 - Automation & Deployment** (Complete)
- ✅ GitHub repository (public, source of truth)
- ✅ Cloudflare Pages deployment (backup domain: tagtaly.dev.pages)
- ✅ Custom domain configuration (primary: www.tagtaly.com)
- ✅ Cron job automation (daily execution at 7 AM)
- ✅ Production monitoring and logging

**Next phase: Phase 3 (Enhancements)** - Real-time publishing, additional features

## File Locations

**Core scripts:** Root directory (*.py files)
**Documentation:** README.md, SETUP.md, prd.md, BRANDING.md, CLAUDE.md
**Configuration:** config/ directory (countries.py, feeds.py, viral_topics.py)
**Database:** uk_news.db (SQLite, created on first run, synced to GitHub)
**Output:** output/viral_charts_[country]_[YYYYMMDD]/ (generated daily, synced to GitHub)
**Logs:** logs/pipeline.log (cron job execution log)
**Automation:**
- Cron jobs (server-based, see Deployment section)
- daily-workflow.yml (GitHub Actions backup)
**Helper scripts:** setup.sh, run.sh
**Repositories:**
- **#tagtaly** (PRIVATE): [github.com/grig/tagtaly](https://github.com/grig/tagtaly) - Python pipeline, GitHub Actions
- **#tagtaly-pages** (PUBLIC): [github.com/grig/tagtaly-pages](https://github.com/grig/tagtaly-pages) - Static site, served to www.tagtaly.com
