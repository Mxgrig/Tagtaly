#!/usr/bin/env python3
"""
Add QWE columns to database and populate with basic categorization
Workaround for TextBlob dependency issues
"""

import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from category_utils import canonical_category

def add_qwe_columns():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'tagtaly.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Add QWE columns if they don't exist
    try:
        cursor.execute('ALTER TABLE articles ADD COLUMN qwe_primary TEXT DEFAULT "viral"')
        print("✓ Added qwe_primary column")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("  qwe_primary column already exists")
        else:
            raise

    try:
        cursor.execute('ALTER TABLE articles ADD COLUMN urgency TEXT DEFAULT "background"')
        print("✓ Added urgency column")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("  urgency column already exists")
        else:
            raise

    conn.commit()

    # Simple categorization based on keywords
    QWE_KEYWORDS = {
        'quality': ['health', 'safety', 'hospital', 'nhs', 'weather', 'storm', 'emergency', 'cancer', 'disease'],
        'money': ['price', 'cost', 'market', 'stock', 'tax', 'inflation', 'economy', 'job', 'wage', 'bill'],
        'stories': ['celebrity', 'scandal', 'viral', 'trending', 'trump', 'elon', 'sport', 'championship']
    }

    URGENCY_KEYWORDS = {
        'urgent': ['breaking', 'urgent', 'alert', 'warning', 'emergency', 'recall'],
        'important': ['announces', 'major', 'significant', 'launches', 'reveals']
    }

    # Get all articles
    cursor.execute("""
        SELECT id, headline, summary
        FROM articles
        WHERE qwe_primary IS NULL
           OR qwe_primary IN ('viral', 'wallet')
    """)
    articles = cursor.fetchall()

    print(f"\nCategorizing {len(articles)} articles...")

    for article_id, headline, summary in articles:
        text = f"{headline or ''} {summary or ''}".lower()

        # Determine QWE category
        category_scores = {}
        for category, keywords in QWE_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score

        # Pick category with highest score, default to viral
        qwe_primary = max(category_scores, key=category_scores.get) if any(category_scores.values()) else 'stories'
        if category_scores[qwe_primary] == 0:
            qwe_primary = 'stories'
        qwe_primary = canonical_category(qwe_primary)

        # Determine urgency
        urgency = 'background'
        for level in ['urgent', 'important']:
            if any(keyword in text for keyword in URGENCY_KEYWORDS[level]):
                urgency = level
                if level == 'urgent':
                    break

        # Update article
        cursor.execute("""
            UPDATE articles
            SET qwe_primary = ?, urgency = ?
            WHERE id = ?
        """, (qwe_primary, urgency, article_id))

    conn.commit()
    print(f"✓ Categorized {len(articles)} articles")

    # Show summary
    cursor.execute("""
        SELECT qwe_primary, urgency, COUNT(*) as count
        FROM articles
        GROUP BY qwe_primary, urgency
        ORDER BY qwe_primary, urgency
    """)

    print("\n📊 QWE Distribution:")
    print("-" * 60)
    print(f"{'Category':<15} {'Urgency':<15} {'Count':<10}")
    print("-" * 60)
    for row in cursor.fetchall():
        category = canonical_category(row[0]) if row[0] else 'quality'
        print(f"{category:<15} {row[1]:<15} {row[2]:<10}")

    conn.close()
    print("\n✓ QWE columns added and populated successfully!")

if __name__ == '__main__':
    add_qwe_columns()
