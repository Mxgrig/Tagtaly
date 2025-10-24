# Daily Automated Page Update System

## Overview

The Tagtaly website now features a **fully automated daily update system** that refreshes ALL page components synchronously every day at **7 AM UTC** (8 AM UK, 2 AM US ET).

## What Gets Updated

### 1. **Articles** (`docs/assets/data/articles.json`)
- All articles from RSS feeds collected in the past 24 hours
- Includes sentiment scores, topic classification, viral scores
- Updated timestamp shows latest data collection time

### 2. **Viral Charts** (Country-specific)
- **UK Charts** (`docs/assets/data/uk/chart_*.json`) - 6 charts
  - Record-breaking stories, media bias, people scorecards
- **US Charts** (`docs/assets/data/us/chart_*.json`) - 4 charts
  - Similar story angles for US news
- **Global Charts** (`docs/assets/data/global/chart_*.json`) - 6 charts
  - International news insights

Each chart includes:
- Primary visualization (ECharts JSON)
- Alternate visualization (hover variant)
- Virality scores
- Detailed story data

### 3. **Dashboard Data Files**
Four key data files update automatically:

#### `sentiment_tracker.json`
- Today's news sentiment score (0-100)
- Yesterday's sentiment for comparison
- Mood trend visualization

#### `topic_surges.json`
- Top 15 topics trending today
- Percentage change from yesterday
- Article counts (today vs yesterday)

#### `category_dominance.json`
- Dominant topic category for the day
- Top 5 categories with article counts
- Distribution breakdown

#### `wordcloud.json`
- 50 most frequent keywords from today's headlines
- Keyword frequency counts
- Filtered for meaningful words (3+ chars, no stop words)

### 4. **Page Metadata**
- **Dates** - Automatically updates all date references on index.html
- **Updated Time** - Shows latest pipeline execution time
- **Statistics** - Article counts, source counts, sentiment distribution

## Workflow Architecture

```
GitHub Actions (Daily 7 AM UTC)
    ↓
1. Checkout repository
    ↓
2. Setup Python environment
    ↓
3. News Collection (RSS feeds)
    ↓
4. News Analysis (sentiment, topics)
    ↓
5. Generate Articles JSON
    ↓
6. Generate Viral Charts (with fixes)
    ↓
7. Generate Dashboard Data (4 files)
    ↓
8. Generate Word Cloud
    ↓
9. Sync all assets
    ↓
10. Update HTML metadata
    ↓
11. Commit & Push to main
    ↓
12. Verification Report
    ↓
Live Site (www.tagtaly.com) Updated ✓
```

## File Locations

### Source Files (Repository)
```
assets/data/
├── articles.json
├── sentiment_tracker.json
├── topic_surges.json
├── category_dominance.json
└── wordcloud.json

src/social_dashboard/assets/data/
├── uk/
│   ├── chart_1_primary.json
│   ├── chart_1_alternate.json
│   └── ... (6 charts total)
├── us/
│   ├── chart_1_primary.json
│   ├── chart_1_alternate.json
│   └── ... (4 charts total)
└── global/
    ├── chart_1_primary.json
    ├── chart_1_alternate.json
    └── ... (6 charts total)
```

### Live Site Files (Deployed)
```
docs/assets/data/
├── articles.json
├── sentiment_tracker.json
├── topic_surges.json
├── category_dominance.json
├── wordcloud.json
├── uk/
│   └── chart_*.json (6 files)
├── us/
│   └── chart_*.json (4 files)
└── global/
    └── chart_*.json (6 files)

docs/index.html (with updated dates)
```

## How It Works

### 1. **Data Collection Phase**
```bash
python news_collector.py    # Fetch 500+ articles from 20+ RSS feeds
python news_analyzer.py     # Classify topics, analyze sentiment
```
- Stores all data in `data/tagtaly.db` (SQLite)
- Deduplicates by URL hash
- Scores articles for virality

### 2. **Data Export Phase**
```bash
python -c "... export articles.json"
python viral_engine.py      # Generate charts (country-specific)
```
- Exports articles to JSON
- Generates viral story detection
- Creates ECharts-compatible JSON charts

### 3. **Dashboard Generation Phase**
```bash
# Generate each dashboard file
sentiment_tracker.json      # Mood analysis
topic_surges.json           # Topic trends
category_dominance.json     # Category breakdown
wordcloud.json              # Keyword extraction
```

### 4. **Sync Phase**
```bash
cp assets/data/*.json docs/assets/data/
cp -r src/social_dashboard/assets/data/* docs/assets/data/
```
- Copies all generated data to live site folder
- Preserves directory structure

### 5. **Commit Phase**
```bash
git add docs/assets/data/**/*.json
git commit -m "🔄 Daily update: All components refreshed"
git push origin main
```
- Commits all changes with timestamp
- Pushes to GitHub
- Triggers Cloudflare Pages deployment

## Manual Trigger

To run the update manually:

1. Go to GitHub: https://github.com/Mxgrig/Tagtaly
2. Click "Actions" tab
3. Select "Daily Full Page Update"
4. Click "Run workflow"
5. Monitor execution in real-time

Or via command line:
```bash
gh workflow run daily-full-update.yml
```

## What the Frontend Sees

### Dynamic Updates
The index.html frontend automatically displays:

1. **Statistics** (via `data-stat` attributes)
   - `total-articles` - Count of all articles
   - `uk-articles` - UK article count
   - `us-articles` - US article count
   - `positive-pct`, `neutral-pct`, `negative-pct` - Sentiment distribution
   - `top-topic-name` - Dominant topic
   - `top-topic-share` - Topic coverage percentage
   - `updated-time` - Last update timestamp

2. **Charts** (via ECharts rendering)
   - Loads chart JSON from `assets/data/{uk,us,global}/chart_*.json`
   - Renders with dual-chart hover (primary + alternate)
   - Fully interactive with tooltips

3. **Word Cloud** (via word-cloud.js)
   - Loads keywords from `wordcloud.json`
   - Visual size based on frequency
   - Interactive hover tooltips

4. **Hero Banner & Images**
   - Dynamically updates from `featured_images.json`
   - Falls back to Unsplash if missing
   - Loads asynchronously

## Verification & Monitoring

After each run, the workflow generates a verification report showing:

```
✓ Articles: 850+ articles updated
✓ Dashboard Data: sentiment_tracker, topic_surges, category_dominance, wordcloud
✓ Charts: UK 6 files, US 4 files, Global 6 files
✓ Metadata: Updated with current date
🎉 Daily update complete!
```

View logs at: GitHub Actions → Daily Full Page Update → Latest Run

## Troubleshooting

### Charts Not Updating
1. Check workflow execution: GitHub Actions tab
2. Verify chart JSON files exist: `docs/assets/data/{uk,us,global}/`
3. Clear browser cache (Ctrl+Shift+Del)
4. Check browser console for JS errors

### Articles Not Showing
1. Verify `articles.json` is generated
2. Check file size (should be > 100KB)
3. Validate JSON syntax at jsonlint.com
4. Check article counts in verification report

### Dates Not Updating
1. Verify `index.html` has correct regex patterns
2. Check HTML file was committed
3. Wait for Cloudflare Pages cache to refresh (~30 seconds)

### Manual Workflow Trigger
```bash
# Check workflow status
gh run list --workflow=daily-full-update.yml

# View latest run
gh run view <RUN_ID>

# Trigger manually
gh workflow run daily-full-update.yml
```

## Performance Notes

- **Total execution time**: ~3-5 minutes
- **Data file sizes**:
  - articles.json: ~750KB
  - Chart JSON files: 100-300 bytes each
  - Dashboard files: < 5KB each
  - wordcloud.json: ~3KB
- **Deployment**: Automatic via Cloudflare Pages (~30s after push)

## Schedule

| Time | Timezone | Action |
|------|----------|--------|
| 7:00 AM | UTC | Workflow starts |
| 7:00 AM | UTC | News collection begins |
| 7:03 AM | UTC | Charts generation begins |
| 7:05 AM | UTC | Dashboard data generation |
| 7:06 AM | UTC | Data sync & commit |
| 7:07 AM | UTC | Workflow completes |
| 7:30-8:00 AM | UTC | Cloudflare Pages deployment |

**Result**: Page fully updated by **7:30 AM UTC** (8:30 AM UK, 2:30 AM US ET)

## Future Enhancements

- [ ] Add image fetch from Unsplash/Pexels API
- [ ] Generate PNG chart exports (PNG for social media)
- [ ] Add email notifications on workflow completion
- [ ] Generate dashboard PDF reports
- [ ] Add webhook for external integrations
- [ ] Multi-language support
- [ ] Archive historical data

## Configuration

To modify the schedule, edit `.github/workflows/daily-full-update.yml`:

```yaml
on:
  schedule:
    # Change cron expression (7 AM UTC = '0 7 * * *')
    - cron: '0 7 * * *'
```

Cron format: `minute hour day month dayofweek`

Examples:
- `0 8 * * *` = 8 AM UTC (9 AM UK)
- `0 14 * * *` = 2 PM UTC (3 PM UK)
- `0 */4 * * *` = Every 4 hours

## Support

For issues or enhancements:
1. Check GitHub Actions logs
2. Run manual workflow trigger
3. Review verification report
4. Check this documentation

---

**Last Updated**: October 24, 2025
**Workflow Version**: 1.0
**Status**: ✅ Active & Running
