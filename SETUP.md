# 🚀 Tagtaly Setup Guide

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download TextBlob Data

```bash
python -m textblob.download_corpora
```

### 3. Run Your First Pipeline

```bash
python main_pipeline.py
```

That's it! Charts will appear in `viral_charts_YYYYMMDD/` folder.

---

## What Just Happened?

**Step 1:** Collected 200+ articles from UK news sources  
**Step 2:** Analyzed topics and sentiment  
**Step 3:** Created 3 viral-ready charts  

**Find your charts:**
```bash
ls viral_charts_*/
```

**Open them:**
```bash
# Mac
open viral_charts_*/viral_1_*.png

# Linux
xdg-open viral_charts_*/viral_1_*.png

# Windows
start viral_charts_*\viral_1_*.png
```

---

## Troubleshooting

### "pip: command not found"
```bash
# Try pip3 instead
pip3 install -r requirements.txt
```

### "No module named 'feedparser'"
```bash
# Dependencies not installed
pip install -r requirements.txt
```

### "Permission denied"
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### "No new articles found"
- RSS feeds might be temporarily down
- Try again in an hour
- Check your internet connection

---

## Daily Usage

```bash
# Just run this each day
python main_pipeline.py

# Or run individual steps
python news_collector.py  # Fetch news
python news_analyzer.py   # Analyze
python viral_engine.py    # Create charts
```

---

## Next Steps

1. ✅ Post your first chart to social media
2. ✅ Run daily for a week to build data
3. ✅ Customize colors in `viral_viz.py`
4. ✅ Add more news sources in `news_collector.py`
5. ✅ Set up GitHub Actions for automation

See README.md for full documentation.
