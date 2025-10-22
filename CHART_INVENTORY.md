# Tagtaly Chart & Visualization Inventory

## Overview
Tagtaly is a UK news analysis pipeline that generates interactive social media charts from 500+ daily articles. The system has two parallel chart implementations:
1. **Legacy**: Matplotlib PNG generation (`viral_viz.py`)
2. **Current**: ECharts JSON generation for interactive web dashboards (`json_generator.py` + `social_charts.js`)

**Status**: JSON/ECharts implementation is PRIMARY and LIVE. PNG generation is legacy fallback.

---

## Chart Generation Architecture

### Data Flow
```
RSS Feeds (5+ sources)
  ↓ news_collector.py (fetches articles)
  ↓ news_analyzer.py (classifies topics, sentiment)
  ↓ story_detector.py (detects viral angles)
  ↓ viral_engine.py (orchestrates generation)
  ↓
  ├─→ json_generator.py (creates ECharts JSON)
  │   ├─ chart_1_primary.json, chart_1_alternate.json
  │   ├─ chart_2_primary.json, chart_2_alternate.json
  │   └─ ...chart_4_primary/alternate.json
  │
  └─→ viral_viz.py (creates PNG files - LEGACY)
      ├─ PNG images in output/viral_charts_*
      └─ Captions as TXT files

  ↓
  social_charts.js (renders in browser with hover effects)
  ↓
  social_dashboard/index.html (LIVE dashboard)
```

---

## 1. JSON/ECharts Implementation (PRIMARY - LIVE)

### Files Location
- **Generator**: `/home/grig/Projects/Tagtaly/src/json_generator.py` (294 lines)
- **Renderer**: `/home/grig/Projects/Tagtaly/social_dashboard/assets/js/social_charts.js` (258 lines)
- **HTML**: `/home/grig/Projects/Tagtaly/social_dashboard/index.html`
- **CSS**: `/home/grig/Projects/Tagtaly/social_dashboard/assets/css/style.css`
- **Data Output**: `/home/grig/Projects/Tagtaly/social_dashboard/assets/data/`

### Core Components

#### A. JSONChartGenerator Class (json_generator.py)
Converts story objects into ECharts-compatible JSON format.

**Key Methods**:
- `generate_surge_alert()` - Topic surge visualization (primary: bar chart, alternate: table)
- `generate_viral_people_race()` - Celebrity/politician mention race (primary: horiz bars, alternate: ranked list)
- `generate_record_highlight()` - Record-breaking numbers (primary: giant number, alternate: metric card)
- `generate_sentiment_shift()` - Mood change visualization (primary: diverging bar, alternate: gauges)
- `generate_media_bias()` - Source coverage focus (primary: media bars, alternate: bias indicators)
- `generate_all_from_stories()` - Main orchestrator (generates top 4 stories × 2 variants = 8 JSONs)

**Output Pattern**: Each story type generates 2 JSON variants for hover-switching:
```
chart_1_primary.json   (initial view)
chart_1_alternate.json (hover view)
chart_2_primary.json
chart_2_alternate.json
...
chart_4_primary.json
chart_4_alternate.json
```

#### B. ECharts Rendering (social_charts.js)
Five chart types rendered with ECharts 5.0 library.

**Chart Functions**:
1. **initEmotionalRollercoaster()** - Line chart showing mood trends over time
2. **initWeeklyWinner()** - Custom HTML card showing top topic
3. **initSurgeAlert()** - Horizontal bar chart of topic changes (% up/down)
4. **initMediaDivide()** - Mood score by news outlet (color-coded green/red)
5. **initSentimentShowdown()** - Diverging bar comparing two news outlets

**Dual-Chart Hover Feature**:
- `createDualChartCard()` function loads both primary + alternate JSON
- On hover: switches to alternate chart (300ms delay)
- On mouse leave: reverts to primary chart
- Preserves ECharts instance for smooth transitions

### 5 Chart Types Implemented

#### Chart 1: Emotional Rollercoaster
- **Type**: Line chart with gradient fill
- **Data**: Time series of mood scores
- **Colors**: Purple gradient (#8b5cf6)
- **Files**:
  - `chart_1_primary.json` - Full line chart
  - `chart_1_alternate.json` - Alternative time period/metric
- **JSON Structure**:
  ```json
  {
    "headline": "📍 Headline text",
    "type": "line",
    "dates": ["Mon", "Tue", ...],
    "scores": [0.5, 0.6, ...]
  }
  ```

#### Chart 2: Weekly Winner
- **Type**: Custom HTML card (not ECharts)
- **Data**: Single topic with article count
- **Colors**: Teal/indigo themed
- **File**: `social_weekly_winner.json`
- **JSON Structure**:
  ```json
  {
    "headline": "This Week's Winner",
    "topic": "Technology",
    "count": 127,
    "subtitle": "articles"
  }
  ```

#### Chart 3: Surge Alert
- **Type**: Horizontal bar chart
- **Data**: Top 5 topics with % change (positive=red, negative=green)
- **Files**:
  - `chart_2_primary.json` - Bar percentages
  - `chart_2_alternate.json` - Alternative metric
- **JSON Structure**:
  ```json
  {
    "headline": "🇬🇧 Andrew Tate mentioned 5.1x more...",
    "type": "bar",
    "chart_type": "surge_alert_primary",
    "data": [
      ["Topic Name", 125],
      ["Topic 2", 45]
    ]
  }
  ```

#### Chart 4: Media Divide
- **Type**: Horizontal bar chart with mood scores
- **Data**: News outlets with sentiment scores (-/+)
- **Colors**: Red (negative) / Green (positive)
- **Files**:
  - `chart_3_primary.json` - Bar chart by source
  - `chart_3_alternate.json` - Alternative grouping
- **JSON Structure**:
  ```json
  {
    "headline": "What Global outlets...",
    "type": "media_bars",
    "chart_type": "media_bias_primary",
    "data": [
      {"source": "BBC", "topic": "Tech", "count": 28},
      {"source": "CNN", "topic": "Health", "count": 27}
    ]
  }
  ```

#### Chart 5: Sentiment Showdown
- **Type**: Stacked diverging bar
- **Data**: Two outlets competing on mood score
- **Colors**: Green vs Red (positive vs negative)
- **File**: `chart_4_primary.json`
- **JSON Structure**:
  ```json
  {
    "headline": "Sentiment Showdown - BBC vs Daily Mail",
    "positive": {
      "source": "BBC",
      "mood_score": 24
    },
    "negative": {
      "source": "Daily Mail",
      "mood_score": 31
    }
  }
  ```

### Technology Stack
- **Frontend Framework**: Pure vanilla JavaScript (no framework)
- **Chart Library**: ECharts 5.0 (CDN: `echarts.min.js`)
- **Data Format**: JSON
- **Styling**: CSS custom properties, flexbox layout
- **Font**: Inter (Google Fonts)

### Dashboard Features
- **Responsive**: Mobile-first design, CSS Grid layout
- **Interactive**: Hover to switch between chart variants
- **Auto-Resize**: Window resize event listener triggers chart resize
- **Error Handling**: Try/catch for JSON fetch failures, graceful degradation
- **Real-time Updates**: Fetches JSON on page load (can be updated via API)

---

## 2. Legacy Matplotlib PNG Implementation

### Files Location
- **Generator**: `/home/grig/Projects/Tagtaly/src/viral_viz.py` (333 lines)
- **Orchestrator**: `/home/grig/Projects/Tagtaly/viral_engine.py` (123 lines)
- **Output**: `/home/grig/Projects/Tagtaly/output/viral_charts_*/`

### Chart Types Generated

#### PNG Chart 1: Surge Alert
- **Method**: `create_surge_alert()` in `ViralChartMaker`
- **Chart Type**: Horizontal bar chart
- **Size**: 1080×1350px (Instagram portrait)
- **Colors**: Red (surge), Green (drop)
- **Data**: Top 5 topics with % change
- **Output**: `viral_1_SURGE_ALERT.png`

#### PNG Chart 2: Viral People Race
- **Method**: `create_viral_people_race()`
- **Chart Type**: Horizontal bar chart
- **Size**: 1080×1350px
- **Colors**: Orange highlight
- **Data**: Top 8 people with mention counts
- **Output**: `viral_2_VIRAL_PEOPLE_SCORECARD.png`

#### PNG Chart 3: Record Highlight
- **Method**: `create_record_highlight()`
- **Chart Type**: Giant number on colored background
- **Size**: 1080×1350px
- **Colors**: Red background, white text
- **Data**: Single large number + context
- **Output**: `viral_3_RECORD_ALERT.png`

#### PNG Chart 4: Sentiment Shift
- **Method**: `create_sentiment_shift()`
- **Chart Type**: Horizontal bar chart
- **Size**: 1080×1350px
- **Colors**: Green (positive sentiment), Red (negative)
- **Data**: Top 5 topics with sentiment change
- **Output**: `viral_4_SENTIMENT_SHIFT.png`

#### PNG Chart 5: Media Bias
- **Method**: `create_media_bias_chart()`
- **Chart Type**: Horizontal bar chart
- **Size**: 1080×1350px
- **Colors**: Orange bars with topic labels
- **Data**: News sources and their topic focus
- **Output**: `viral_5_MEDIA_BIAS.png`

#### PNG Chart 6: Comparison
- **Method**: `create_comparison_chart()`
- **Chart Type**: Vertical bar chart
- **Size**: 1080×1350px
- **Colors**: Red (UK), Orange (US)
- **Data**: UK vs US comparison of a topic
- **Output**: `viral_6_COMPARISON.png`

### Design Specifications (PNG)
- **DPI**: 100 (web optimized)
- **File Size Target**: < 2MB per PNG
- **Color Palette**:
  - Background: `#000000` (black)
  - Text: `#FFFFFF` (white)
  - Surge: `#FF3B30` (red)
  - Drop: `#34C759` (green)
  - Highlight: `#FF9500` (orange)
  - Neutral: `#8E8E93` (gray)
- **Font**: System fonts, 16pt+ for mobile readability
- **Branding**: "Tagtaly" watermark in bottom-right

---

## 3. Story Detection Engine

### File
`/home/grig/Projects/Tagtaly/src/story_detector.py` (12,467 bytes)

### Story Types Detected

1. **SURGE_ALERT** - Topics that exploded in coverage (week-over-week % change)
2. **VIRAL_PEOPLE_SCORECARD** - Celebrity/politician mention counts
3. **POLITICAL_SCORECARD** - Political figure mentions (UK-specific)
4. **SENTIMENT_SHIFT** - Mood changes by topic
5. **RECORD_ALERT** - New highs/lows in news coverage
6. **MEDIA_BIAS** - Different outlets covering different topics

### Detection Methods

**detect_topic_surge()**
- Compares this week vs last week article counts by topic
- Calculates % change: `(this_week - last_week) / last_week * 100`
- Returns top 5 topics by change

**track_viral_people_mentions()** / **track_politicians()**
- Counts mentions of specific people in headlines + summaries
- Viral people list: Andrew Tate, Mark Zuckerberg, Prince Harry, Jeff Bezos, King Charles, Kim Kardashian, Elon Musk, Taylor Swift
- UK politicians: Boris Johnson, Keir Starmer, Penny Mordaunt, Sunak

**detect_sentiment_shift()**
- Compares sentiment scores by topic over two time periods
- Calculates sentiment_change = recent_avg - historical_avg
- Returns topics with largest mood swings

**find_record_numbers()**
- Extracts numbers from headlines matching "record", "highest", "lowest", "new"
- Ranks by extracted number size

**compare_outlet_focus()**
- Groups articles by source × topic
- Identifies media bias (what each outlet prioritizes)

### Virality Scoring
- Each story gets a `virality_score` (0-20)
- Only stories with score >= 5 are included in final output
- Higher score = more likely to go viral on social media

---

## 4. Pipeline Orchestration

### File
`/home/grig/Projects/Tagtaly/src/viral_engine.py` (123 lines)

### Main Function: `generate_viral_content()`
1. Gets active countries from config
2. For each country:
   - Initialize `StoryDetector`
   - Find viral angles
   - Sort by virality score
   - Generate JSON charts for top 4 stories
3. Generates global charts
4. Outputs total count of JSON files created

### Output Structure
```
social_dashboard/assets/data/
├── chart_1_primary.json
├── chart_1_alternate.json
├── chart_2_primary.json
├── chart_2_alternate.json
├── chart_3_primary.json
├── chart_3_alternate.json
├── chart_4_primary.json
├── chart_4_alternate.json
└── social_weekly_winner.json
```

---

## 5. Supporting Chart Files

### Other Visualization Data Files (Pre-generated Examples)
Location: `/home/grig/Projects/Tagtaly/social_dashboard/assets/data/`

**Legacy/Demo Files** (may not be updated):
- `social_emotional_rollercoaster.json` - Sentiment trend data
- `social_topic_surges.json` - Topic surge data
- `social_media_divide.json` - Media outlet comparison
- `social_sentiment_showdown.json` - Outlet mood comparison
- `images.json` - Image references (for future image gallery)

---

## 6. Dashboard Styling

### File
`/home/grig/Projects/Tagtaly/social_dashboard/assets/css/style.css`

### Color System (CSS Variables)
```css
--black: #0f172a
--white: #ffffff
--gray: #8E8E93
--red: #FF3B30
--green: #22c55e
--orange: #FF9500
--indigo: #6366F1
--purple: #8B5CF6
--teal: #14b8a6
--card-bg: #ffffff
--surface: #f4f5fb
```

### Layout
- **Max Width**: 1200px
- **Grid**: Charts in responsive CSS Grid
- **Cards**: White background, subtle shadows
- **Typography**: Inter font family, clean hierarchy
- **Spacing**: Consistent padding/margins throughout

### Chart Container Styles
```css
.chart-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
}

.chart-placeholder {
  height: 400px;
  width: 100%;
}
```

---

## 7. HTML Dashboard

### File
`/home/grig/Projects/Tagtaly/social_dashboard/index.html` (60+ lines)

### Structure
```html
<header class="page-header">
  <h1>Social Media Dashboard</h1>
  <p>A showcase of shareable, social-first charts...</p>
</header>

<main class="charts-grid">
  <div class="chart-card">
    <!-- Chart 1: Emotional Rollercoaster -->
    <div id="emotional-rollercoaster-chart" class="chart-placeholder"></div>
  </div>

  <div class="chart-card">
    <!-- Chart 2: Weekly Winner -->
    <div id="weekly-winner-chart" class="chart-placeholder"></div>
  </div>

  <div class="chart-card">
    <!-- Chart 3: Surge Alert -->
    <div id="surge-alert-chart" class="chart-placeholder"></div>
  </div>

  <div class="chart-card">
    <!-- Chart 4: Media Divide -->
    <div id="media-divide-chart" class="chart-placeholder"></div>
  </div>

  <div class="chart-card">
    <!-- Chart 5: Sentiment Showdown -->
    <div id="sentiment-showdown-chart" class="chart-placeholder"></div>
  </div>
</main>
```

### Dependencies
- ECharts 5.0 CDN
- Google Fonts (Inter)
- Custom CSS (shadcn_style.css + style.css)
- Custom JS (social_charts.js)

---

## 8. Data Generators

### news_collector.py
Fetches articles from RSS feeds, stores in database

### news_analyzer.py
Classifies topics (9 categories), analyzes sentiment (TextBlob)

### story_detector.py
Detects viral angles using 5 algorithms

### json_generator.py
Converts stories to ECharts JSON format

### viral_engine.py
Orchestrates generation for all countries

---

## 9. Summary Statistics

### Chart Implementation Status

| Component | Type | Status | Location |
|-----------|------|--------|----------|
| ECharts JSON | Primary | LIVE | `src/json_generator.py` |
| JavaScript Renderer | Primary | LIVE | `social_dashboard/assets/js/social_charts.js` |
| HTML Dashboard | Primary | LIVE | `social_dashboard/index.html` |
| Matplotlib PNG | Legacy | Maintained | `src/viral_viz.py` |
| Story Detection | Core | LIVE | `src/story_detector.py` |
| Pipeline Orchestration | Core | LIVE | `src/viral_engine.py` |

### Files Generated Daily
- 4 story types × 2 variants = 8 JSON files (`chart_1_primary.json`, etc.)
- 1 weekly winner JSON
- 6 legacy PNG files (if enabled)
- 6 legacy caption TXT files (if enabled)

### Code Metrics
- **Total chart generation code**: ~1,500 lines
- **JSON Generator**: 294 lines
- **JavaScript Renderer**: 258 lines
- **Matplotlib PNG Generator**: 333 lines
- **Story Detector**: 12,467 bytes
- **Pipeline Engine**: 123 lines

---

## 10. Important Notes

### No PNG Charts in Production
Per CLAUDE.md instructions: "Please there should not be any png charts in this project. All charts are javascript generated."

The Matplotlib PNG code in `viral_viz.py` is LEGACY and should not be used. All production charts are ECharts JSON rendered via JavaScript.

### Key Technologies
- **Backend**: Python 3.10+, SQLite, pandas
- **Frontend**: Vanilla JavaScript, ECharts 5.0, CSS Grid
- **Data Format**: JSON (ECharts-compatible)
- **Deployment**: Cloudflare Pages, Vercel config

### Unique Features
1. **Dual-Chart Hover** - Switch between primary/alternate on hover
2. **Responsive Design** - Mobile-first CSS Grid
3. **Story Virality Scoring** - 0-20 scale based on detectability
4. **Multi-Country Support** - UK, US, Global with region-specific topics
5. **ECharts Integration** - Interactive, animated charts with tooltips

---

## File Locations Summary

```
/home/grig/Projects/Tagtaly/
├── src/
│   ├── json_generator.py          ← JSON chart generation (PRIMARY)
│   ├── viral_engine.py            ← Orchestrator
│   ├── story_detector.py          ← Viral angle detection
│   ├── viral_viz.py               ← PNG generation (LEGACY)
│   ├── news_analyzer.py
│   ├── news_collector.py
│   └── main_pipeline.py
├── social_dashboard/
│   ├── index.html                 ← Main dashboard
│   ├── assets/
│   │   ├── js/
│   │   │   └── social_charts.js   ← ECharts rendering (PRIMARY)
│   │   ├── css/
│   │   │   └── style.css
│   │   └── data/
│   │       ├── chart_1_primary.json
│   │       ├── chart_1_alternate.json
│   │       ├── chart_2_primary.json
│   │       ├── chart_2_alternate.json
│   │       ├── chart_3_primary.json
│   │       ├── chart_3_alternate.json
│   │       ├── chart_4_primary.json
│   │       ├── chart_4_alternate.json
│   │       ├── social_weekly_winner.json
│   │       └── [legacy files]
│   └── social_dashboard/
│       └── [subdirectory structure]
├── output/
│   └── viral_charts_*_YYYYMMDD/   ← Legacy PNG output
├── config/
│   ├── countries.py
│   ├── feeds.py
│   └── viral_topics.py
├── data/
│   └── tagtaly.db                 ← SQLite database
└── CLAUDE.md                      ← Project documentation
```

