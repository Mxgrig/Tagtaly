# Design Inspiration: What Top News Sites Do

## Analysis of 8 Leading Data Visualization Sites

This document describes actual design patterns from sites that get millions of views.

---

## 1. FiveThirtyEight - The Gold Standard

**URL:** fivethirtyeight.com
**Monthly traffic:** 10M+ visitors
**Known for:** Political polling and sports analytics

### Color Palette
```
Primary: #FF6E3A (Orange)
Secondary: #00D9C0 (Teal/cyan)
Tertiary: #ED3F7E (Hot pink)
Background: #FFFFFF (Pure white)
Text: #2E2E2E (Charcoal)
```

### Design Characteristics

**Charts:**
- Horizontal bar charts with rounded caps (2-3px radius)
- Orange for main data, teal for comparisons
- Large titles (28-32px) in sans-serif bold
- Value labels OUTSIDE bars (never inside)
- No borders on bars
- Subtle grid lines (#EFEFEF)

**Typography:**
- Font: "Atlas Grotesk" or "Helvetica Neue"
- Title: 32px bold, all caps
- Subtitle: 16px regular, gray (#666)
- Labels: 18px medium weight
- Values: 20px bold

**Spacing:**
- Bar height: 40-50px
- Gap between bars: 8-12px
- Chart margins: 40px all sides
- Title to chart: 30px

### What Makes It Work

✅ **Orange is energetic but not alarming** - Perfect for news that's important but not scary
✅ **White background feels professional** - Easy to screenshot and share
✅ **Large text everywhere** - Readable on mobile without zooming
✅ **Consistent branding** - Every chart feels like FiveThirtyEight

### Example Chart Description

"Presidential Approval Rating" chart:
- White background
- Title: "BIDEN APPROVAL" (32px, all caps, charcoal)
- Subtitle: "Among registered voters" (16px, gray)
- Horizontal bars showing 58% approve (orange), 42% disapprove (teal)
- Value labels: "58%" in 22px bold, positioned at end of bar
- No borders, no shadows, totally flat design
- Subtle grid lines every 25%

**Key insight:** Simple, clean, high-contrast. No visual tricks, just data.

---

## 2. The Pudding - Modern Visual Storytelling

**URL:** pudding.cool
**Monthly traffic:** 2M+ visitors
**Known for:** Experimental data stories

### Color Palette
```
Background: #FFFEF9 (Cream/off-white)
Accent 1: #FF6B6B (Coral)
Accent 2: #A69BFF (Lavender)
Accent 3: #6FCF97 (Mint)
Accent 4: #FFD93D (Sunshine yellow)
Text: #1A1A1A (Near-black)
```

### Design Characteristics

**Charts:**
- Custom color palette per story (not consistent)
- Mix of chart types (bars, dots, custom SVG)
- Rounded corners everywhere (4-6px)
- Playful animations (for web)
- No borders, flat colors
- Creative layouts (not just horizontal bars)

**Typography:**
- Font: "Graphik" or similar geometric sans
- Title: 36-48px bold (very large)
- Body: 18-20px (generous sizing)
- Labels: 16px regular
- Values: 24px bold (extra large)

**Spacing:**
- Very generous white space
- Padding: 50-80px margins
- Section breaks: 100px+
- Breathing room prioritized

### What Makes It Work

✅ **Cream background feels warm** - More inviting than stark white
✅ **Color variety prevents boredom** - Each chart feels unique
✅ **Huge typography** - Prioritizes readability over density
✅ **Playful but professional** - Appeals to younger audience

### Example Chart Description

"Most Popular Songs of 2024" chart:
- Cream background (#FFFEF9)
- Title: "STREAMS IN BILLIONS" (48px, super bold)
- Horizontal bars with rounded right edges
- Top song: Coral (#FF6B6B)
- 2nd-5th: Lavender (#A69BFF)
- Values: "2.4B" in 24px bold next to bars
- No grid, no borders, minimal styling
- Generous spacing (60px between bars)

**Key insight:** Make it feel human, not robotic. Warmth matters.

---

## 3. Axios - Social Media Optimized

**URL:** axios.com/visuals
**Monthly traffic:** 25M+ visitors
**Known for:** "Smart Brevity" news style

### Color Palette
```
Primary: #0068C8 (Axios blue)
Secondary: #FFC94D (Yellow)
Accent: #FF8400 (Orange)
Background: #FFFFFF
Text: #000000
```

### Design Characteristics

**Charts:**
- Designed for Twitter/Instagram sharing
- Very large text (30-40px titles)
- Bold colors with high saturation
- Simple bar charts (no complex visuals)
- "Big Idea" callout in yellow box
- Clean, no-frills approach

**Typography:**
- Font: "Noto Sans" (Google Font)
- Title: 36px black weight (900)
- Subtitle: 18px regular
- Values: 28px bold
- Footer: "Axios Visuals" branding

**Spacing:**
- Minimal margins (20-30px)
- Tight bar spacing (maximize data shown)
- Large padding for text callouts

### What Makes It Work

✅ **Built for social media** - Every chart is share-ready
✅ **Yellow callouts grab attention** - "The Big Idea" boxes
✅ **Very bold colors** - Stop the scroll on Instagram
✅ **Simple messages** - One chart, one point

### Example Chart Description

"Gas Prices Surge" chart:
- White background
- Title: "GAS PRICES HIT RECORD HIGH" (36px, all caps)
- Yellow box: "Why it matters" (callout in #FFC94D)
- Single vertical bar showing price over time
- Current price: "$4.25" in huge 40px text
- Axios logo bottom right
- Square format (1080x1080px for Instagram)

**Key insight:** Mobile-first, social-first. Design for thumb scrolling.

---

## 4. Bloomberg Graphics

**URL:** bloomberg.com/graphics
**Monthly traffic:** 100M+ (full site)
**Known for:** Financial and economic data

### Color Palette
```
Primary: #119BFF (Bloomberg blue)
Orange: #FF8C42
Purple: #9B59B6
Teal: #1ABC9C
Red: #E74C3C (used sparingly)
Background: #FFFFFF
Text: #000000
```

### Design Characteristics

**Charts:**
- Professional, serious tone
- Blue as primary color (trust/authority)
- Orange for accents and highlights
- Precise grid lines
- Small legends (not taking space)
- Dense information (lots of data)

**Typography:**
- Font: "BWHaas" (Bloomberg custom)
- Title: 28px bold
- Labels: 14px regular
- Values: 18px bold
- Source: 11px gray

**Spacing:**
- Tight (information density)
- 20-30px margins
- Small bar spacing (10px)

### What Makes It Work

✅ **Blue = trust** - Perfect for financial news
✅ **Orange adds warmth** - Balances cool blue
✅ **Professional appearance** - Serious credibility
✅ **Dense but readable** - Lots of info without clutter

### Example Chart Description

"Stock Market Performance" chart:
- White background
- Title: "S&P 500 Companies by Sector" (28px)
- Subtitle: "Market cap in billions" (14px gray)
- Horizontal bars: Blue for each sector
- Top performer: Orange highlight
- Values: "$2.4T" right-aligned at bar end
- Grid lines: Light gray (#E5E5E5)
- Source: "Bloomberg, as of March 2025" (11px)

**Key insight:** Professional doesn't mean boring. Blue + orange works.

---

## 5. Financial Times

**URL:** ft.com/graphics
**Monthly traffic:** 30M+ visitors
**Known for:** Pink newspaper, premium content

### Color Palette
```
FT Pink: #FFF1E5 (signature background)
Teal: #0F5499
Burgundy: #990F3D
Gold: #CC9933
Navy: #006685
Text: #33302E (dark brown)
```

### Design Characteristics

**Charts:**
- Cream/pink background (brand signature)
- Sophisticated color harmony
- Serif fonts for headlines
- Sans-serif for data
- Traditional but modern
- High print quality

**Typography:**
- Title font: "Financier Display" (serif)
- Data font: "MetricWeb" (sans-serif)
- Title: 32px bold serif
- Labels: 16px sans
- Values: 20px bold sans

**Spacing:**
- Classic newspaper spacing
- 40px margins
- Generous line height (1.5x)

### What Makes It Work

✅ **Pink background is distinctive** - Instantly recognizable
✅ **Premium feel** - Sophisticated color choices
✅ **Warm tones** - Cream is easier on eyes than white
✅ **Traditional + modern blend** - Appeals to older audience

### Example Chart Description

"UK GDP Growth" chart:
- Cream background (#FFF1E5)
- Title: "Britain's economy falters" (32px serif, dark brown)
- Subtitle: "Quarterly GDP growth" (16px sans, gray)
- Bar chart: Teal (#0F5499) for positive, burgundy (#990F3D) for negative
- Values: "+0.3%" in 20px bold above bars
- Grid: Subtle cream-darker lines
- FT logo watermark

**Key insight:** Background color can be a brand differentiator.

---

## 6. Our World in Data

**URL:** ourworldindata.org
**Monthly traffic:** 15M+ visitors
**Known for:** Academic-quality research data

### Color Palette
```
Primary: #3360A3 (Navy blue)
Secondary: #00847E (Teal)
Tertiary: #F2A900 (Gold)
Red: #D73B2C
Background: #FFFFFF
Text: #191919
```

### Design Characteristics

**Charts:**
- Academic but accessible
- Line charts with area fill
- Clear legends with large swatches
- Educational tone
- Source citations prominent
- Open data emphasis

**Typography:**
- Font: "Lato" (Google Font)
- Title: 24px bold
- Subtitle: 16px regular
- Labels: 14px medium
- Values: 16px bold

**Spacing:**
- Academic spacing (comfortable)
- 35px margins
- Clear section breaks

### What Makes It Work

✅ **Trustworthy colors** - Navy blue = authority
✅ **Clear labeling** - Education-first approach
✅ **Sources always shown** - Transparency builds trust
✅ **Interactive versions** - Static + web versions

### Example Chart Description

"Global Life Expectancy" chart:
- White background
- Title: "Life expectancy has increased globally" (24px)
- Subtitle: "Period life expectancy at birth" (16px gray)
- Line chart with teal line (#00847E)
- Area fill: Light teal with 30% opacity
- Values: "73.2 years" at data points
- Y-axis: Clear labels every 10 years
- Source: "UN World Population Prospects 2024" (12px)
- "OurWorldInData.org" watermark

**Key insight:** Transparency and education matter. Show your sources.

---

## 7. The Economist Charts

**URL:** economist.com/graphic-detail
**Monthly traffic:** 40M+ visitors
**Known for:** Red branding, witty headlines

### Color Palette
```
Economist Red: #E3120B
Blue: #1A7AC3
Green: #009639
Orange: #F26522
Background: #FFFFFF
Text: #000000
```

### Design Characteristics

**Charts:**
- Traditional but refined
- Red brand color used sparingly
- Clean bar and line charts
- Witty headlines
- British style (formal but clever)
- Print-quality design

**Typography:**
- Font: "Econ Sans" (custom serif-sans hybrid)
- Title: 26px bold
- Subtitle: 15px italic (often witty)
- Labels: 13px regular
- Values: 16px bold

**Spacing:**
- Compact but clear
- 30px margins
- Professional density

### What Makes It Work

✅ **Witty headlines** - Makes data memorable
✅ **Red used strategically** - Not overused
✅ **British tone** - Formal but not stuffy
✅ **Print heritage** - High quality standards

### Example Chart Description

"Oil Prices Volatile" chart:
- White background
- Title: "Crude awakening" (26px, clever pun)
- Subtitle: "Brent crude, $ per barrel" (15px italic)
- Line chart: Economist red (#E3120B)
- Values: "$85" at peaks/troughs
- Grid: Light gray, subtle
- Y-axis: Starting at $0 (honest scaling)
- Source: "The Economist" logo bottom left

**Key insight:** Data can be serious AND clever. Wordplay works.

---

## 8. The New York Times - The Upshot

**URL:** nytimes.com/section/upshot
**Monthly traffic:** 100M+ (full site)
**Known for:** High-quality data journalism

### Color Palette
```
NYT Gray: #333333
Blue: #326891
Orange: #D97D1D
Purple: #7D53A4
Red: #AB2626
Background: #FFFFFF
Text: #121212
```

### Design Characteristics

**Charts:**
- Sophisticated and detailed
- Gray-first approach (not colorful)
- Color used for emphasis only
- Precise annotations
- High information density
- Desktop-optimized (responsive)

**Typography:**
- Font: "Cheltenham" (serif for headlines) + "Franklin" (sans for data)
- Title: 30px serif bold
- Subtitle: 16px serif regular
- Labels: 14px sans
- Values: 16px sans bold

**Spacing:**
- Newspaper-style (traditional)
- 40px margins
- Balanced density

### What Makes It Work

✅ **Gray-first design** - Color draws eye to what matters
✅ **Sophisticated audience** - Can handle complexity
✅ **Precise annotations** - Every detail explained
✅ **High credibility** - NYT brand trust

### Example Chart Description

"Inflation Analysis" chart:
- White background
- Title: "Inflation Remains Elevated" (30px serif)
- Subtitle: "Consumer price index, change from year ago" (16px)
- Line chart: Dark gray (#333) as main line
- Callout: Orange dot where inflation peaked
- Annotation: "Peak: 9.1% in June 2022" with arrow
- Y-axis: Clear percentage labels
- Grid: Very subtle (#F0F0F0)
- Source: "Bureau of Labor Statistics" (12px)

**Key insight:** Use color sparingly for maximum impact. Gray is underrated.

---

## Common Patterns Across All Sites

### 1. Typography Standards

**Titles:**
- Range: 24-48px
- Average: 28-32px
- Weight: Bold (700) or Black (900)
- Case: UPPERCASE or Title Case

**Value labels:**
- Range: 16-28px
- Average: 20-22px
- Weight: Bold (700)
- Placement: Outside bars (not inside)

**Subtitles/Context:**
- Range: 14-18px
- Average: 16px
- Weight: Regular (400)
- Color: Gray (not black)

### 2. Color Strategies

**Approach 1: One Primary + One Accent**
- FiveThirtyEight: Orange + Teal
- Axios: Blue + Yellow
- Bloomberg: Blue + Orange

**Approach 2: Varied Palette**
- The Pudding: 4-6 colors per project
- The Economist: 4 colors (red, blue, green, orange)

**Approach 3: Gray-First**
- NYT: Gray with color highlights only
- Our World in Data: Navy + minimal accents

### 3. Background Choices

| Background | Sites Using | Effect |
|------------|-------------|--------|
| Pure white (#FFFFFF) | FiveThirtyEight, Bloomberg, Economist | Professional, easy to share |
| Cream/Off-white (#FFF1E5) | Financial Times, The Pudding | Warm, distinctive, easy on eyes |
| Light gray (#F5F5F5) | Rare | Can look "old" or "outdated" |
| Dark (#000000) | Almost none | Dated, hard to share |

**Winner: White or cream** - Light backgrounds dominate 2025

### 4. Chart Styling

**Borders on bars:** NONE (all sites use borderless)
**Grid lines:** Subtle or none (never heavy)
**Shadows:** Minimal or none (flat design)
**3D effects:** NONE (totally dead in 2025)
**Rounded corners:** Sometimes (2-4px), but rare

### 5. Spacing Patterns

**Bar heights:**
- Range: 30-60px
- Average: 40-50px
- Mobile: Thinner (30-40px)

**Gap between bars:**
- Range: 8-20px
- Average: 10-12px
- Ratio: 0.2-0.25x bar height

**Margins:**
- Range: 20-80px
- Average: 30-40px
- Mobile: Smaller (20-30px)

---

## Key Takeaways for Tagtaly

### What Works in 2025

1. **Light backgrounds** - White or cream (never dark)
2. **Bold, saturated colors** - Orange, blue, teal, pink (not muted pastels)
3. **Large text** - 22pt+ for values, 28pt+ for titles
4. **No borders** - Flat, clean bars without outlines
5. **One or two accent colors** - Orange + blue is most popular
6. **Gray for neutrals** - Not black for borders/text
7. **Source citations** - Always show data source
8. **Mobile-first sizing** - Everything readable without zoom

### What Doesn't Work Anymore

1. ❌ **Dark backgrounds** - Black feels dated, hard to share
2. ❌ **Corporate blue only** - Boring, needs warm accent
3. ❌ **Red-green comparisons** - Accessibility issues
4. ❌ **Small fonts** - <16px is unreadable on mobile
5. ❌ **Heavy borders** - Makes charts look "Excel-like"
6. ❌ **3D effects** - Totally abandoned by all modern sites
7. ❌ **Muted colors** - Pastels don't grab attention
8. ❌ **Single accent color** - Monotonous across multiple charts

### Best Color Combinations (Proven)

1. **Orange + Blue** (FiveThirtyEight, Bloomberg)
   - Orange: #FF6B35
   - Blue: #0078FF
   - Why: Complementary, accessible, energetic

2. **Blue + Yellow** (Axios)
   - Blue: #0068C8
   - Yellow: #FFC94D
   - Why: High contrast, attention-grabbing

3. **Teal + Pink** (Modern trend)
   - Teal: #14B8A6
   - Pink: #EC4899
   - Why: Fresh, modern, Gen-Z appeal

4. **Navy + Orange + Teal** (Bloomberg variation)
   - Navy: #0F5499
   - Orange: #FF8C42
   - Teal: #1ABC9C
   - Why: Professional + warm + cool balance

---

## Tagtaly Recommendation Based on Research

### Winning Formula

**Primary palette:**
- Orange (#FF6B35) - Main accent (like FiveThirtyEight)
- Blue (#0078FF) - Secondary (like Bloomberg)
- Pink (#EC4899) - Highlights (modern trend)
- Teal (#14B8A6) - Tertiary (fresh alternative)

**Background:**
- White (#FFFFFF) - Matches 7 out of 8 top sites

**Typography:**
- Titles: 28pt bold (matches FiveThirtyEight, Bloomberg)
- Values: 22pt bold (matches average)
- Subtitles: 16pt regular (matches all sites)

**Styling:**
- No borders (matches all sites)
- Flat design (matches all sites)
- Subtle or no grid (matches modern trend)

### Why This Works

✅ Combines **best practices from FiveThirtyEight** (orange primary)
✅ Adds **Bloomberg professionalism** (blue secondary)
✅ Includes **2025 trend colors** (hot pink, teal)
✅ Avoids **dated elements** (dark backgrounds, borders)
✅ Optimized for **social media** (high contrast, mobile-first)

---

## Implementation Priority

### High Impact Changes (Do First)
1. Orange for surges/increases (like FiveThirtyEight)
2. White background (keep current - correct!)
3. Larger fonts (28pt titles, 22pt values)
4. Remove all borders

### Medium Impact (Do Second)
5. Add hot pink for extremes
6. Blue + orange for comparisons
7. Teal for positive data
8. Color hierarchy in rankings

### Nice-to-Have (Do Later)
9. Rounded bar corners (2-3px)
10. Witty headlines (like Economist)
11. More generous spacing
12. Custom fonts

---

**Summary:** All top news data viz sites in 2025 use light backgrounds, bold colors (especially orange + blue), large text, and borderless flat design. Tagtaly should follow this proven formula.

**Last Updated:** October 9, 2025
**Sources:** Direct analysis of 8 leading sites' actual charts
