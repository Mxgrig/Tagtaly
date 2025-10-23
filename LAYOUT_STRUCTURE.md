# Tagtaly Magazine Dashboard - Layout Structure

## Visual Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                          HEADER (Sticky)                        │
│  Logo + Tagtaly   [Dashboard] [Archive] [About]   [Get Started]│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        HERO SECTION                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │         [Large Featured Image with Overlay]              │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────┐                 │  │
│  │  │ "What's Moving in News Today"       │                 │  │
│  │  │ Real-time viral trends...           │                 │  │
│  │  │ [273 Stories] [BBC] [12:34]         │                 │  │
│  │  └─────────────────────────────────────┘                 │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────┬───────────────────────────┐
│     MAIN CONTENT (3 columns)      │   SIDEBAR (1.35 columns)  │
│                                   │                           │
│ ┌───────────────────────────────┐ │ ┌───────────────────────┐ │
│ │ Today's Data Summary          │ │ │                       │ │
│ │                               │ │ │  [Featured Image]     │ │
│ ├─────────────────┬─────────────┤ │ │                       │ │
│ │ Emotional       │  Surge      │ │ └───────────────────────┘ │
│ │ Rollercoaster   │  Alert      │ │                           │
│ │ [Chart 1]       │ [Chart 2]   │ │ ┌───────────────────────┐ │
│ └─────────────────┴─────────────┘ │ │ Today's Top Stories   │ │
│                                   │ │ • Story 1             │ │
│ ┌───────────────────────────────┐ │ │ • Story 2             │ │
│ │ What Newsrooms Are Covering   │ │ │ • Story 3             │ │
│ │                               │ │ │ • Story 4             │ │
│ ├──────────────┬────────────────┤ │ │ • Story 5             │ │
│ │ Weekly       │ Tone Split     │ │ └───────────────────────┘ │
│ │ Winner       │ [Chart 4]      │ │                           │
│ │ [Chart 3]    │                │ │ ┌───────────────────────┐ │
│ ├──────────────┴────────────────┤ │ │ Need custom           │ │
│ │ Story Types Today             │ │ │ intelligence?         │ │
│ │ [Chart 5 - Category Dom.]     │ │ │                       │ │
│ ├───────────────────────────────┤ │ │ [Talk to ops@...]     │ │
│ │ Outlet Sentiment              │ │ └───────────────────────┘ │
│ │ [Chart 6 - Sentiment Show.]   │ │                           │
│ └───────────────────────────────┘ │                           │
│                                   │                           │
│ ┌───────────────────────────────┐ │                           │
│ │ Publishing Operations         │ │                           │
│ │                               │ │                           │
│ ├──────────────┬────────────────┤ │                           │
│ │ Outlet       │ Publishing     │ │                           │
│ │ Productivity │ Rhythm         │ │                           │
│ │ [Chart 7]    │ [Chart 8]      │ │                           │
│ └──────────────┴────────────────┘ │                           │
│                                   │                           │
│ ┌───────────────────────────────┐ │                           │
│ │ Keywords in Focus             │ │                           │
│ │                               │ │                           │
│ │ [Chart 9 - Wordcloud]         │ │                           │
│ │                               │ │                           │
│ └───────────────────────────────┘ │                           │
└───────────────────────────────────┴───────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                           FOOTER                                │
│  Tagtaly         Product           Company                      │
│  Description     • Dashboard       • Privacy                    │
│                  • Archive         • Legal                      │
│                  • About           • Contact                    │
│                                                                 │
│  © 2025 Tagtaly Inc. All rights reserved.                       │
└─────────────────────────────────────────────────────────────────┘
```

## Chart Placement

### Today's Data Summary (2 charts)
1. **Emotional Rollercoaster** (70% width) - Line chart showing 7-day sentiment trend
2. **Surge Alert** (30% width) - Bar chart showing topics accelerating

### What Newsrooms Are Covering (4 charts)
3. **Weekly Winner** (50% width) - Card displaying dominant topic
4. **Media Divide** (50% width) - Positive vs negative tone split
5. **Category Dominance** (100% width, centered) - Story types breakdown
6. **Sentiment Showdown** (100% width, right-aligned) - Outlet sentiment comparison

### Publishing Operations (2 charts)
7. **Outlet Productivity** (55% width) - Stories per source
8. **Publishing Rhythm** (45% width) - Hour-by-hour publishing pattern

### Keywords in Focus (1 chart)
9. **Wordcloud** (100% width, centered) - Word frequency visualization

## Responsive Breakpoints

### Desktop (> 1200px)
- 3-column main content + 1.35-column sidebar
- Sidebar has left border (vertical gradient line)
- Hero image: 460px height
- Section descriptions: 2-column text layout

### Tablet (768px - 1200px)
- Charts stack in 2-column grid
- Sidebar moves below main content
- Hero image: ~380px height
- Section descriptions: Single column

### Mobile (< 768px)
- All charts stack in single column
- Navigation hidden (show brand + CTA only)
- Hero image: 320px height
- Simplified spacing and padding

## Typography Scale

- **Hero Title**: 3.6rem (desktop) → 2.6rem (mobile)
- **Section Titles**: 2.3rem (desktop) → 1.9rem (mobile)
- **Chart Titles**: 1.25rem
- **Body Text**: 1.05rem
- **Meta/Labels**: 0.82rem

## Color Palette

- **Background**: #f8f3eb (warm beige canvas)
- **Surface**: #ffffff (card backgrounds)
- **Text Primary**: #1f1611 (near-black)
- **Text Secondary**: #484847 (dark gray)
- **Text Muted**: #7a6a61 (muted brown-gray)
- **Accent Primary**: #d97706 (orange)
- **Accent Secondary**: #fbbf24 (light orange/yellow)

## Spacing System

- **Section Gap**: 2.5rem - 3.5rem (responsive)
- **Card Gap**: 1.8rem - 2rem
- **Card Padding**: 1.8rem - 2.2rem
- **Border Radius**: 18px (cards), 28px (hero)

## Shadow Hierarchy

- **Card Base**: `0 18px 32px rgba(31, 22, 17, 0.07)`
- **Card Hover**: `0 22px 38px rgba(31, 22, 17, 0.1)`
- **Hero Image**: `0 28px 40px rgba(31, 22, 17, 0.08)`
- **Sidebar Cards**: `0 10px 22px rgba(31, 22, 17, 0.06)`

## Interaction States

- **Links**: Orange (#d97706) → Black on hover
- **Cards**: Lift on hover (translateY(-2px))
- **CTA Buttons**: Lift on hover with shadow increase
- **Charts**: Dual-view on hover (where applicable)

## Accessibility Features

- Semantic HTML5 structure
- ARIA labels where appropriate
- Focus states with visible outlines
- Keyboard navigation support
- Readable contrast ratios (WCAG AA)
- Responsive font sizing with clamp()
