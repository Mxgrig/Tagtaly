# Tagtaly Color Palette Implementation Guide

## Quick Reference: New vs Old Colors

| Purpose | Old Color | New Color | Hex Code | Why Change? |
|---------|-----------|-----------|----------|-------------|
| Surges/Increases | Indigo | Orange | `#FF6B35` | Energetic without alarm |
| Drops/Decreases | Green | Purple | `#8B5CF6` | Consistent mood, not confusing |
| Extreme Values | N/A | Hot Pink | `#EC4899` | Extra emphasis |
| Primary Data | Indigo | Electric Blue | `#0078FF` | Modern, trustworthy |
| Positive Sentiment | Green | Teal | `#14B8A6` | Fresh, optimistic |
| Negative Sentiment | N/A | Coral Red | `#EF4444` | Concern without panic |
| Text | Dark gray | Near-black | `#171717` | Higher contrast |
| Borders | Gray | Light gray | `#E5E5E5` | Softer, cleaner |

---

## Copy-Paste Color Dictionary

### Replace in viral_viz.py

```python
# OLD COLORS (REMOVE)
self.colors = {
    'surge': '#6366F1',      # Indigo accent
    'drop': '#10B981',       # Green
    'neutral': '#A3A3A3',    # Gray
    'highlight': '#8B5CF6',  # Purple accent
    'background': '#FFFFFF', # White background
    'text': '#171717',       # Dark gray text
    'border': '#E5E5E5'      # Light border
}
```

```python
# NEW COLORS (USE THIS)
self.colors = {
    # Primary data colors
    'surge': '#FF6B35',      # Orange - increases/trending up
    'drop': '#8B5CF6',       # Purple - decreases (not negative)
    'extreme': '#EC4899',    # Hot pink - records/huge changes
    'primary': '#0078FF',    # Electric blue - main data
    'secondary': '#14B8A6',  # Teal - supporting data

    # Sentiment colors
    'positive': '#10B981',   # Green - good news
    'negative': '#EF4444',   # Coral red - bad news
    'neutral': '#A3A3A3',    # Gray - neutral

    # UI colors
    'background': '#FFFFFF', # White
    'text': '#171717',       # Near-black
    'text_secondary': '#737373', # Medium gray
    'border': '#E5E5E5',     # Light gray

    # Accent colors (for variety)
    'yellow': '#FFD93D',     # Highlights
    'coral': '#FF6B6B',      # Alternative to pink
    'mint': '#6FCF97',       # Alternative to teal
}
```

---

## Chart-by-Chart Updates

### 1. Surge Alert Chart

**What to change:**
- Replace indigo bars with orange (increases) and purple (decreases)
- Add hot pink for extreme changes (>100%)
- Increase font sizes
- Remove bar borders

```python
# FIND THIS CODE (lines 42-53 in viral_viz.py):
bars = ax.barh(data['topic'], data['pct_change'])

for i, (bar, pct) in enumerate(zip(bars, data['pct_change'])):
    bar.set_color(self.colors['surge'] if pct > 0 else self.colors['drop'])
    bar.set_edgecolor(self.colors['border'])
    bar.set_linewidth(0)

    ax.text(pct + 5, i, f"+{pct:.0f}%",
           va='center', fontsize=20, fontweight='bold',
           color=self.colors['text'])
```

```python
# REPLACE WITH:
bars = ax.barh(data['topic'], data['pct_change'], height=0.6)

for i, (bar, pct) in enumerate(zip(bars, data['pct_change'])):
    # Color logic: orange for increases, purple for decreases
    # Hot pink for extreme changes (>100% or <-50%)
    if abs(pct) > 100:
        bar.set_color(self.colors['extreme'])
    elif pct > 0:
        bar.set_color(self.colors['surge'])
    else:
        bar.set_color(self.colors['drop'])

    bar.set_edgecolor('none')  # No borders - cleaner look
    bar.set_linewidth(0)

    # Larger value labels
    sign = '+' if pct > 0 else ''
    ax.text(pct + max(abs(data['pct_change']))*0.05, i,
           f"{sign}{pct:.0f}%",
           va='center', fontsize=22,  # Increased from 20
           fontweight='bold',
           color=self.colors['text'])
```

**Font size changes:**
```python
# Title (line 57)
ax.text(0.5, 1.15, title,
       fontsize=28,  # Up from 24
       fontweight='bold',
       ha='center', color=self.colors['text'])

# Subtitle (line 64)
ax.text(0.5, 1.08, 'vs last week',
       fontsize=16,  # Up from 14
       ha='center',
       color=self.colors['text_secondary'])  # Use secondary text color
```

---

### 2. Viral People Race Chart

**What to change:**
- Top 3 get distinct colors (orange, blue, pink)
- Rest get muted gradient
- Add medal emojis
- Larger fonts

```python
# FIND THIS CODE (lines 92-103 in viral_viz.py):
mentions = sorted(story_data['data'].items(), key=lambda x: x[1], reverse=True)[:8]
names = [m[0] for m in mentions]
counts = [m[1] for m in mentions]

bars = ax.barh(names, counts, color=self.colors['highlight'])

for i, (bar, count) in enumerate(zip(bars, counts)):
    ax.text(count + max(counts)*0.02, i, f"{count} mentions",
           va='center', fontsize=18, fontweight='bold',
           color=self.colors['text'])
```

```python
# REPLACE WITH:
mentions = sorted(story_data['data'].items(), key=lambda x: x[1], reverse=True)[:8]
names = [m[0] for m in mentions]
counts = [m[1] for m in mentions]

# Top 3 get special colors, rest get muted gradient
top_colors = [
    self.colors['surge'],      # 1st - Orange
    self.colors['primary'],    # 2nd - Blue
    self.colors['extreme'],    # 3rd - Hot pink
]
other_colors = [
    self.colors['drop'],       # 4th - Purple
    self.colors['secondary'],  # 5th - Teal
    self.colors['yellow'],     # 6th - Yellow
    self.colors['neutral'],    # 7th - Gray
    '#D1D5DB',                # 8th - Light gray
]

colors = (top_colors + other_colors)[:len(names)]

bars = ax.barh(names, counts, color=colors, edgecolor='none', height=0.6)

# Add medal emojis for top 3
medals = ['🥇', '🥈', '🥉']
for i, medal in enumerate(medals[:min(3, len(names))]):
    ax.text(-max(counts)*0.03, i, medal,
           va='center', ha='right', fontsize=20)

# Value labels
for i, (bar, count) in enumerate(zip(bars, counts)):
    ax.text(count + max(counts)*0.02, i, f"{count} mentions",
           va='center', fontsize=18, fontweight='bold',
           color=self.colors['text'])
```

**Font size changes:**
```python
# Title (line 107)
ax.text(0.5, 1.12, title,
       fontsize=26,  # Up from 22
       fontweight='bold',
       ha='center', color=self.colors['text'])
```

---

### 3. Record Highlight Chart

**What to change:**
- Dynamic background colors based on record type
- Larger numbers
- Bolder text

```python
# FIND THIS CODE (lines 133-136 in viral_viz.py):
fig, ax = plt.subplots(figsize=self.fig_size, facecolor=self.colors['surge'])
ax.axis('off')

record = story_data['data'][0]
```

```python
# REPLACE WITH:
record = story_data['data'][0]

# Dynamic background based on record type
headline_lower = record['headline'].lower()
if 'high' in headline_lower or 'record' in headline_lower or 'peak' in headline_lower:
    bg_color = self.colors['extreme']  # Hot pink for highs/records
elif 'low' in headline_lower or 'minimum' in headline_lower:
    bg_color = self.colors['primary']  # Blue for lows
else:
    bg_color = self.colors['surge']    # Orange for other milestones

fig, ax = plt.subplots(figsize=self.fig_size, facecolor=bg_color)
ax.axis('off')
```

**Font size changes:**
```python
# Giant number (line 156)
ax.text(0.5, 0.55, big_number,
       fontsize=140,  # Up from 120
       fontweight='900',  # Extra bold (up from 'bold')
       ha='center', va='center',
       color='white')

# Headline (line 163)
ax.text(0.5, 0.85, "RECORD HIGH" if 'high' in record['headline'].lower() else "RECORD LOW",
       fontsize=36,  # Up from 32
       fontweight='bold',
       ha='center', color='white')

# Context (line 169)
ax.text(0.5, 0.35, record['headline'][:80],
       fontsize=20,  # Up from 18
       ha='center',
       color='white', wrap=True)
```

---

### 4. Sentiment Shift Chart

**What to change:**
- Use teal for positive shifts (not green on green confusion)
- Use coral red for negative shifts (not indigo)
- Add emoji indicators

```python
# FIND THIS CODE (lines 200-212 in viral_viz.py):
bars = ax.barh(data['topic'], data['sentiment_change'])

for i, (bar, change) in enumerate(zip(bars, data['sentiment_change'])):
    bar.set_color(self.colors['drop'] if change > 0 else self.colors['surge'])
    bar.set_edgecolor(self.colors['border'])
    bar.set_linewidth(0)

    direction = "+" if change > 0 else ""
    ax.text(change + 0.05, i, f"{direction}{change:.2f}",
           va='center', fontsize=18, fontweight='bold',
           color=self.colors['text'])
```

```python
# REPLACE WITH:
bars = ax.barh(data['topic'], data['sentiment_change'], height=0.6)

for i, (bar, change) in enumerate(zip(bars, data['sentiment_change'])):
    # Color logic: teal for positive, coral for negative, gray for neutral
    if abs(change) < 0.05:
        bar.set_color(self.colors['neutral'])
    elif change > 0:
        bar.set_color(self.colors['secondary'])  # Teal - positive shift
    else:
        bar.set_color(self.colors['negative'])   # Coral red - negative shift

    bar.set_edgecolor('none')
    bar.set_linewidth(0)

    # Add emoji indicators
    if change > 0.1:
        emoji = '📈'
    elif change < -0.1:
        emoji = '📉'
    else:
        emoji = '➡️'

    # Emoji before bar
    ax.text(-max(abs(data['sentiment_change']))*0.08, i, emoji,
           va='center', ha='right', fontsize=18)

    # Value label
    direction = "+" if change > 0 else ""
    ax.text(change + max(abs(data['sentiment_change']))*0.05, i,
           f"{direction}{change:.2f}",
           va='center', fontsize=20,  # Up from 18
           fontweight='bold',
           color=self.colors['text'])
```

**Font size changes:**
```python
# Title (line 218)
ax.text(0.5, 1.15, title,
       fontsize=28,  # Up from 24
       fontweight='bold',
       ha='center', color=self.colors['text'])

# Subtitle (line 223)
ax.text(0.5, 1.08, 'Sentiment change (-1 to +1 scale)',
       fontsize=14,  # Up from 12
       ha='center',
       color=self.colors['text_secondary'])
```

---

### 5. Media Bias Chart

**What to change:**
- Use color variety for bars
- Larger fonts

```python
# FIND THIS CODE (lines 256-262 in viral_viz.py):
bars = ax.barh(data['source'], data['count'], color=self.colors['highlight'])

for i, (bar, topic) in enumerate(zip(bars, data['topic'])):
    ax.text(bar.get_width() / 2, i, topic,
           va='center', ha='center', fontsize=16, fontweight='bold',
           color=self.colors['background'])
```

```python
# REPLACE WITH:
# Rotate through accent colors
colors = [
    self.colors['surge'],
    self.colors['primary'],
    self.colors['drop'],
    self.colors['secondary'],
    self.colors['extreme'],
    self.colors['yellow'],
]

bar_colors = [colors[i % len(colors)] for i in range(len(data))]

bars = ax.barh(data['source'], data['count'],
               color=bar_colors, edgecolor='none', height=0.6)

for i, (bar, topic) in enumerate(zip(bars, data['topic'])):
    ax.text(bar.get_width() / 2, i, topic,
           va='center', ha='center',
           fontsize=18,  # Up from 16
           fontweight='bold',
           color='white')  # White text on colored bars
```

**Font size changes:**
```python
# Title (line 266)
ax.text(0.5, 1.12, title,
       fontsize=26,  # Up from 22
       fontweight='bold',
       ha='center', color=self.colors['text'])

# Axis labels (line 277)
ax.tick_params(colors=self.colors['text'], labelsize=16)  # Up from 14
```

---

## Font Size Summary

| Element | Old Size | New Size | Weight |
|---------|----------|----------|--------|
| Chart titles | 22-24pt | 26-28pt | Bold (700) |
| Subtitles | 12-14pt | 14-16pt | Normal (400) |
| Value labels | 18-20pt | 20-22pt | Bold (700) |
| Axis labels | 14-16pt | 16-18pt | Medium (500) |
| Small text/branding | 10pt | 12pt | Normal (400) |
| Record highlight numbers | 120pt | 140pt | Extra-bold (900) |

---

## Testing Checklist

After making changes, test each chart type:

- [ ] Generate surge alert chart - check orange/purple colors
- [ ] Generate people race chart - verify top 3 colors + medals
- [ ] Generate record highlight - test different record types
- [ ] Generate sentiment shift - check teal/coral + emojis
- [ ] Generate media bias chart - verify color variety
- [ ] View all charts on mobile screen (actual size)
- [ ] Check text readability at arm's length
- [ ] Verify colors look good in Instagram preview
- [ ] Test colorblind mode (use simulator tool)
- [ ] Get feedback from others: "Does this look modern?"

---

## Quick Fix Script

If you want to update all at once, run this after backing up `viral_viz.py`:

```bash
# Backup original
cp src/viral_viz.py src/viral_viz.py.backup

# Then apply changes manually or use this as reference
# Test one chart type at a time
python -c "
from src.viral_viz import ViralChartMaker
import pandas as pd

maker = ViralChartMaker()
print('Colors updated:', maker.colors)
"
```

---

## Common Mistakes to Avoid

❌ **Don't** keep green for "drops" - confusing (green = good usually)
❌ **Don't** use same color for all bars in rankings - boring
❌ **Don't** keep small fonts (<18pt for values)
❌ **Don't** add bar borders - looks outdated
❌ **Don't** use pure black for text - too harsh (#000000)

✅ **Do** use orange for increases - energetic without alarm
✅ **Do** vary colors in multi-bar charts - engaging
✅ **Do** increase all font sizes by 2-4pt
✅ **Do** remove borders - cleaner modern look
✅ **Do** use near-black for text - softer (#171717)

---

## Side-by-Side Comparison

### Surge Alert Chart

**BEFORE:**
- Indigo bars for increases
- Green bars for decreases
- 20pt font for values
- Border on bars

**AFTER:**
- Orange bars for increases
- Purple bars for decreases
- Hot pink for extreme changes (>100%)
- 22pt font for values
- No borders
- 28pt title (up from 24pt)

**Impact:** More energetic, clearer hierarchy, better mobile readability

---

### People Race Chart

**BEFORE:**
- All bars purple
- No visual hierarchy
- 18pt fonts

**AFTER:**
- Top 3: Orange, blue, hot pink
- Rest: Purple, teal, yellow, gray gradient
- Medal emojis for top 3
- 18pt fonts (keep same - already good)
- 26pt title (up from 22pt)

**Impact:** Clear winners, more engaging, playful elements

---

## File Locations

- **Main color definitions:** `/home/grig/Projects/Tagtaly/src/viral_viz.py` (lines 18-27)
- **Dashboard colors:** `/home/grig/Projects/Tagtaly/src/generate_dashboard_charts.py` (lines 16-24)
- **Old visualizer (if still used):** `/home/grig/Projects/Tagtaly/visualizer.py` (lines 8-14)

Update all three files for consistency across the project.

---

**Last Updated:** October 9, 2025
**Next Review:** After user feedback on new charts
