# 🏷️ Tagtaly

**UK News, Counted & Charted**

Transform daily UK news into viral social media visualizations automatically.

---

## 🎯 What It Does

Tagtaly:
1. **Tags** 500+ UK news articles daily by topic (Politics, Health, Economy, etc.)
2. **Tallies** mentions, sentiment, and trends
3. **Creates** 3 Instagram-ready charts showing the most dramatic stories
4. **Delivers** them ready to post in 5 minutes

**Example outputs:**
- 🚨 "NHS mentioned 247 times - record high"
- 📊 "Starmer covered 7x more than Sunak this week"
- 📈 "Health news UP 125% week-over-week"

---

## 🚀 Quick Start

### Install & Run (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m textblob.download_corpora

# 2. Run the pipeline
python main_pipeline.py

# 3. Find your charts
ls viral_charts_*/
```

**That's it!** 3 charts ready to post.

### Even Quicker

```bash
# Mac/Linux
chmod +x run.sh
./run.sh

# Windows
run.bat
```

---

## 📁 What You Get

After running, you'll have:

```
viral_charts_20251008
