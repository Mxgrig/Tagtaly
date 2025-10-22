# QWE Categorization Quick Start

## What is QWE?

**QWE = Quality + Wallet + Viral**

A user-centric framework for categorizing news into three dimensions:

- **💊 Quality**: Stories affecting your health, safety, and wellbeing
- **💰 Wallet**: Stories affecting your money and financial situation
- **🎭 Viral**: Stories trending on social media and entertainment

## Quick Examples

| Headline | QWE Category | Urgency | Why? |
|----------|--------------|---------|------|
| "Breaking: Fed Raises Interest Rates" | Wallet | Urgent | Affects mortgages, loans, savings |
| "Warning: Flu Outbreak in Hospitals" | Quality | Urgent | Health emergency requiring action |
| "Taylor Swift Breaks Record at Finals" | Viral | Background | Entertainment news, not urgent |
| "Stock Market Crash Amid Health Crisis" | Wallet + Quality | Urgent | Multiple impacts, financial primary |

## Running QWE Analysis

```bash
# Analyze all articles (automatically includes QWE categorization)
python src/news_analyzer.py

# Output shows both traditional and QWE analysis:
# 📊 Analysis Summary: (topic breakdown)
# 💊💰🎭 QWE Framework Summary: (QWE breakdown)
```

## Database Schema

```sql
-- New QWE columns
qwe_categories TEXT    -- JSON: ["wallet", "quality"]
qwe_primary TEXT       -- "wallet"
urgency TEXT           -- "urgent" | "important" | "background"
qwe_keywords TEXT      -- JSON: ["fed", "rate", "mortgage"]
```

## Querying QWE Data

### Find Urgent Wallet Stories
```sql
SELECT headline, urgency, qwe_keywords
FROM articles
WHERE qwe_primary = 'wallet' AND urgency = 'urgent'
ORDER BY viral_score DESC;
```

### Count by Category and Urgency
```sql
SELECT qwe_primary, urgency, COUNT(*) as count
FROM articles
GROUP BY qwe_primary, urgency;
```

### Multi-Category Articles
```sql
SELECT headline, qwe_categories
FROM articles
WHERE qwe_categories LIKE '%,%';  -- Contains comma = multiple categories
```

## Using categorize_qwe() in Code

```python
from src.news_analyzer import categorize_qwe

# Analyze an article
result = categorize_qwe(
    article_text="The Fed announced emergency rate cuts affecting mortgages.",
    headline="Breaking: Fed Cuts Rates"
)

print(result)
# {
#     'categories': ['wallet'],
#     'primary_category': 'wallet',
#     'urgency': 'urgent',
#     'qwe_keywords_found': ['fed', 'rate', 'mortgage', 'emergency']
# }
```

## Category Selection Logic

1. **Keyword Matching**: Each category scored by keyword matches
2. **Primary Category**: Category with highest score
3. **Multi-Category**: All categories with >0 matches included
4. **No Match**: If no keywords match, `primary_category = None`

## Urgency Levels

| Level | Keywords | Use Case |
|-------|----------|----------|
| **urgent** | breaking, emergency, alert, warning, recall | Immediate user action needed |
| **important** | major, significant, announces | User should be aware |
| **background** | (everything else) | Nice to know |

**Priority**: Urgent keywords override important keywords

## Testing

```bash
# Run test suite
python test_qwe_categorization.py

# Tests cover:
# - Single category (wallet, quality, viral)
# - Multi-category classification
# - Urgency detection
# - Keyword extraction
```

## Common Patterns

### Quality Stories
- Health emergencies (outbreak, virus, warning)
- Safety recalls (toxic, contamination, recall)
- Weather events (storm, flood, emergency)
- Infrastructure failures (blackout, shortage, crash)

### Wallet Stories
- Economic news (inflation, recession, market)
- Employment (layoff, hiring, salary, job)
- Personal finance (mortgage, tax, debt, rent)
- Consumer prices (gas, grocery, utilities)

### Viral Stories
- Celebrity news (taylor, trump, elon, kardashian)
- Social media trends (viral, trending, meme)
- Entertainment drama (scandal, feud, breakup)
- Sports championships (finals, olympics, world cup)

## Integration with Existing Pipeline

QWE categorization runs **automatically** when you run news_analyzer.py:

```
Articles → Topic Classification → Sentiment Analysis → QWE Categorization → Database
           (Politics, Economy)    (Positive/Negative)   (Quality/Wallet/Viral)
```

All existing functionality preserved:
- Topic classification still works
- Sentiment analysis still works
- Viral scoring still works
- Country/scope classification still works

QWE adds a **parallel categorization layer** for user-centric filtering.

## Next Steps

1. **Run analysis**: `python src/news_analyzer.py`
2. **Check results**: View QWE summary in output
3. **Query data**: Use SQL examples above
4. **Build features**: Filter charts by QWE category + urgency

## Support

**Documentation**: `/home/grig/Projects/Tagtaly/claudedocs/QWE_IMPLEMENTATION.md`
**Test Script**: `/home/grig/Projects/Tagtaly/test_qwe_categorization.py`
**Source Code**: `/home/grig/Projects/Tagtaly/src/news_analyzer.py`
