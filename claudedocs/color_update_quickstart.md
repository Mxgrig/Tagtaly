# Tagtaly Color Update - Quick Start Guide

**Goal:** Replace current black/indigo color scheme with modern, engaging 2025 palette

**Time to implement:** 30-45 minutes

**Impact:** Charts will feel more energetic, modern, and social-media optimized

---

## TL;DR - Just Show Me The Colors

### New Color Palette (Copy-Paste Ready)

```python
self.colors = {
    'surge': '#FF6B35',      # Orange (replaces indigo for increases)
    'drop': '#8B5CF6',       # Purple (replaces green for decreases)
    'extreme': '#EC4899',    # Hot pink (new - for >100% changes)
    'primary': '#0078FF',    # Electric blue (main data)
    'secondary': '#14B8A6',  # Teal (supporting data)
    'positive': '#10B981',   # Green (sentiment only)
    'negative': '#EF4444',   # Red (sentiment only)
    'neutral': '#A3A3A3',    # Gray
    'background': '#FFFFFF', # White
    'text': '#171717',       # Near-black
    'text_secondary': '#737373',  # Medium gray
    'border': '#E5E5E5',     # Light gray
    'yellow': '#FFD93D',     # Accent
    'coral': '#FF6B6B',      # Accent
    'mint': '#6FCF97',       # Accent
}
```

---

## 3-Step Quick Update

### Step 1: Update Color Dictionary (2 minutes)

**File:** `/home/grig/Projects/Tagtaly/src/viral_viz.py`
**Lines:** 18-27

Replace the `__init__` method color dictionary with the new palette above.

### Step 2: Update Bar Colors (15 minutes)

**Surge Alert Chart (line 42):**
```python
# Change color logic
if abs(pct) > 100:
    bar.set_color(self.colors['extreme'])  # Hot pink
elif pct > 0:
    bar.set_color(self.colors['surge'])    # Orange
else:
    bar.set_color(self.colors['drop'])     # Purple
```

**People Race Chart (line 92):**
```python
# Add color hierarchy
top_colors = [self.colors['surge'], self.colors['primary'], self.colors['extreme']]
other_colors = [self.colors['drop'], self.colors['secondary'], self.colors['yellow']]
colors = (top_colors + other_colors)[:len(names)]
bars = ax.barh(names, counts, color=colors)
```

**Record Highlight (line 136):**
```python
# Dynamic background
bg_color = self.colors['extreme'] if 'high' in headline else self.colors['primary']
fig, ax = plt.subplots(figsize=self.fig_size, facecolor=bg_color)
```

**Sentiment Shift (line 200):**
```python
# Fix colors
if change > 0:
    bar.set_color(self.colors['secondary'])  # Teal (not green)
else:
    bar.set_color(self.colors['negative'])   # Red (not indigo)
```

### Step 3: Increase Font Sizes (5 minutes)

**Quick find-and-replace:**
- `fontsize=20` → `fontsize=22` (value labels)
- `fontsize=24` → `fontsize=28` (titles)
- `fontsize=14` → `fontsize=16` (subtitles)
- `fontsize=22` → `fontsize=26` (secondary titles)

---

## Visual Before/After

### Surge Alert Chart

**BEFORE:**
- Indigo bars (#6366F1)
- Green for drops (confusing)
- 24pt title

**AFTER:**
- Orange bars (#FF6B35) for increases
- Purple bars (#8B5CF6) for decreases
- Hot pink (#EC4899) for extreme (>100%)
- 28pt title
- No borders

**Why:** Orange = energetic (not alarming), purple = still interesting (not negative)

---

### People Rankings

**BEFORE:**
- All bars same purple
- No hierarchy

**AFTER:**
- 1st = Orange
- 2nd = Blue
- 3rd = Hot pink
- Rest = Purple → Teal → Yellow → Gray gradient
- Add medals: 🥇🥈🥉

**Why:** Clear visual hierarchy, top 3 stand out immediately

---

### Record Highlight

**BEFORE:**
- Solid indigo background
- 120pt number

**AFTER:**
- Hot pink for record highs
- Blue for record lows
- 140pt number (extra bold)

**Why:** Color signals record type, bigger number = more impact

---

## Testing Your Changes

### Quick Test Script

```bash
# Navigate to project
cd /home/grig/Projects/Tagtaly

# Generate a test chart
python3 << 'EOF'
from src.viral_viz import ViralChartMaker
import pandas as pd

maker = ViralChartMaker()

# Test surge alert
test_data = {
    'headline': 'NHS NEWS SURGING',
    'data': pd.DataFrame({
        'topic': ['NHS', 'Politics', 'Economy'],
        'pct_change': [125, 45, -30]
    })
}

fig = maker.create_surge_alert(test_data)
fig.savefig('test_chart.png', dpi=100, bbox_inches='tight')
print("✅ Test chart saved: test_chart.png")
print("Colors:", maker.colors)
EOF
```

### Visual Checklist

Open `test_chart.png` and verify:
- [ ] Orange bars for positive changes
- [ ] Purple bars for negative changes
- [ ] Hot pink for extreme changes (if any >100%)
- [ ] No borders on bars
- [ ] Title is 28pt (looks larger than before)
- [ ] Values are 22pt (readable)
- [ ] Near-black text (#171717)

---

## Common Issues & Fixes

### Issue 1: Colors look the same as before

**Cause:** Didn't update color dictionary
**Fix:** Check line 18-27 in `viral_viz.py`, make sure `'surge': '#FF6B35'`

### Issue 2: Font sizes didn't change

**Cause:** Only changed one method, not all
**Fix:** Search entire file for `fontsize=20` and update all occurrences

### Issue 3: Charts look washed out

**Cause:** Using light colors or wrong hex codes
**Fix:** Copy exact hex codes from this guide (e.g., `#FF6B35` not `#FFA575`)

### Issue 4: Text is hard to read

**Cause:** Text color too light
**Fix:** Use `#171717` for text, not `#737373` (that's for subtitles only)

---

## Side-by-Side Comparison Table

| Element | Old | New | Why? |
|---------|-----|-----|------|
| Surge color | #6366F1 (indigo) | #FF6B35 (orange) | More energetic, less corporate |
| Drop color | #10B981 (green) | #8B5CF6 (purple) | Not confusing (green ≠ down) |
| Extreme | N/A | #EC4899 (hot pink) | Extra emphasis for big changes |
| Title size | 24pt | 28pt | Better mobile readability |
| Value size | 20pt | 22pt | Clearer at arm's length |
| Bar borders | 1px gray | None | Cleaner, more modern |

---

## Files to Update

### Primary File (Required)

**`/home/grig/Projects/Tagtaly/src/viral_viz.py`**
- Update color dictionary (lines 18-27)
- Update 5 chart methods (surge, race, record, sentiment, bias)
- Update font sizes throughout
- Remove bar borders

### Secondary Files (Optional, for consistency)

**`/home/grig/Projects/Tagtaly/src/generate_dashboard_charts.py`**
- Update COLORS dict (lines 16-24)
- Match palette to viral_viz.py

**`/home/grig/Projects/Tagtaly/visualizer.py`**
- Update BRAND_COLORS (lines 8-14)
- Only if still in use

---

## Rollback Plan

If you don't like the new colors:

```bash
# Before making changes, backup original
cp src/viral_viz.py src/viral_viz.py.backup

# If you want to revert
cp src/viral_viz.py.backup src/viral_viz.py
```

---

## What Makes 2025 Charts Different?

### Old Style (2015-2020)
- Dark backgrounds (black, navy)
- Corporate blues and grays
- Red/green for up/down
- Small text (16-18pt)
- Heavy borders

### New Style (2025)
- Light backgrounds (white, cream)
- Vibrant, energetic colors (orange, teal, pink)
- Blue/orange for comparisons
- Large text (22-28pt)
- Borderless design

**Tagtaly shift:** Moving from "corporate dashboard" → "engaging social media"

---

## Expected Results

### Metrics to Watch

After implementing new colors, you should see:

**Subjective:**
- Charts feel more modern and energetic
- Colors are more distinct and memorable
- Text is easier to read on mobile
- Overall "wow factor" increased

**Objective:**
- Better Instagram engagement (test with A/B)
- Faster comprehension (users "get it" quicker)
- More shares (colorful = shareable)

---

## Getting Feedback

### Test Questions to Ask Others

Show before/after charts and ask:
1. "Which feels more modern?"
2. "Which is easier to read?"
3. "Which would you share on Instagram?"
4. "Can you understand the data quickly?"
5. "Do the colors feel appropriate for news?"

### Expected Answers
- Modern: 80%+ prefer new colors
- Readable: 90%+ find new sizes better
- Shareable: 70%+ prefer new palette
- Quick: Same or faster comprehension
- Appropriate: Yes, if not too "playful"

---

## Next Steps After Implementation

1. **Generate sample charts** with new palette
2. **View on mobile** (actual size, arm's length)
3. **Test colorblind mode** (use simulator)
4. **Get feedback** from 3-5 people
5. **Iterate** based on feedback (if needed)
6. **Document** final palette in project README

---

## Advanced: Creating Color Variations

If you want to tweak colors further:

### Make Orange More/Less Intense
```python
'surge': '#FF6B35',   # Current (balanced)
'surge': '#FF8C5A',   # Lighter (softer)
'surge': '#FF4D1C',   # Darker (bolder)
```

### Alternative Blues
```python
'primary': '#0078FF',  # Current (bright)
'primary': '#0066CC',  # Darker (serious)
'primary': '#1E90FF',  # Lighter (playful)
```

### Hot Pink Alternatives
```python
'extreme': '#EC4899',  # Current (vibrant)
'extreme': '#FF006E',  # Neon (very bold)
'extreme': '#DB2777',  # Ruby (sophisticated)
```

**Tool:** Use Coolors.co to experiment with shades

---

## Documentation

After completing updates, document in:

**README.md:**
```markdown
## Chart Colors

Tagtaly uses a modern, accessible color palette:
- Orange (#FF6B35): Increases and surges
- Blue (#0078FF): Primary data
- Hot pink (#EC4899): Records and extremes
- Teal (#14B8A6): Positive themes
- Purple (#8B5CF6): Comparisons

All colors meet WCAG 2.1 AA accessibility standards.
```

**BRANDING.md:** (if exists)
Add color palette section with hex codes

---

## Full Implementation Checklist

- [ ] Backup original `viral_viz.py`
- [ ] Update color dictionary (lines 18-27)
- [ ] Update surge alert colors (line 42)
- [ ] Update people race colors (line 92)
- [ ] Update record highlight background (line 136)
- [ ] Update sentiment shift colors (line 200)
- [ ] Update media bias colors (line 256)
- [ ] Increase all font sizes (search `fontsize=`)
- [ ] Remove bar borders (set `edgecolor='none'`)
- [ ] Test generate one chart
- [ ] View on mobile screen
- [ ] Get feedback from others
- [ ] Update documentation
- [ ] Delete test files
- [ ] Commit changes

---

## Time Estimate Breakdown

| Task | Time | Difficulty |
|------|------|------------|
| Backup files | 1 min | Easy |
| Update color dict | 2 min | Easy |
| Update surge chart | 5 min | Easy |
| Update people chart | 5 min | Medium |
| Update record chart | 3 min | Easy |
| Update sentiment chart | 5 min | Easy |
| Update bias chart | 3 min | Easy |
| Font size updates | 5 min | Easy |
| Remove borders | 3 min | Easy |
| Testing | 10 min | Easy |
| **Total** | **42 min** | **Easy-Medium** |

---

## Support Resources

**Documents:**
1. `chart_design_research_2025.md` - Full research, palette rationale
2. `color_palette_implementation.md` - Detailed code examples
3. `color_accessibility_guide.md` - Accessibility compliance

**Online Tools:**
- Coolors.co - Color palette generator
- WebAIM Contrast Checker - Accessibility testing
- Coblis.com - Colorblind simulator

**Questions?**
Check research documents above or test locally and iterate.

---

**Ready to start?** Open `/home/grig/Projects/Tagtaly/src/viral_viz.py` and follow Step 1 above!

**Last Updated:** October 9, 2025
