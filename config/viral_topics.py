"""Viral topics configuration - engagement-focused content only"""

# Viral Topics - ONLY track topics that get social media engagement
VIRAL_TOPICS = {
    # Tier 1: Personal Finance (Everyone cares)
    'Cost of Living': {
        'Energy Bills': ['energy bill', 'gas bill', 'electricity', 'heating costs', 'energy price'],
        'Food Prices': ['food price', 'grocery', 'tesco', 'sainsbury', 'weekly shop', 'supermarket'],
        'Petrol': ['petrol price', 'diesel price', 'fuel cost', 'gas price'],
        'Rent & Housing': ['rent', 'house price', 'mortgage', 'landlord', 'housing crisis'],
        'Wages': ['wage', 'salary', 'pay rise', 'minimum wage', 'layoff', 'redundancy']
    },

    # Tier 2: Drama & Scandals (Entertainment)
    'Corporate Drama': {
        'Collapses': ['bankruptcy', 'collapse', 'administration', 'goes bust', 'liquidation'],
        'Scandals': ['ceo fired', 'fraud', 'scandal', 'investigation', 'lawsuit'],
        'Layoffs': ['layoff', 'job cuts', 'redundancy', 'closing', 'mass layoffs'],
        'Greed': ['record profit', 'ceo pay', 'bonus', 'windfall profit', 'shareholder']
    },

    # Tier 3: Tech Drama (Elon & Co.)
    'Tech Entertainment': {
        'AI Controversy': ['chatgpt', 'ai', 'openai', 'artificial intelligence', 'ai regulation'],
        'Crypto': ['bitcoin', 'crypto crash', 'ftx', 'cryptocurrency', 'blockchain'],
        'Big Tech': ['antitrust', 'monopoly', 'tech regulation', 'data privacy']
    },

    # Tier 4: Worker Power (Social justice)
    'Labor': {
        'Strikes': ['strike', 'industrial action', 'union', 'walkout', 'picket'],
        'Conditions': ['amazon warehouse', 'gig economy', 'zero hours', 'worker rights']
    }
}

# Boring Topics - DO NOT TRACK (they get no engagement)
BORING_TOPICS = {
    'earnings_reports': False,     # "Apple Q3 earnings beat expectations"
    'stock_indices': False,        # "FTSE 100 up 0.3%"
    'analyst_ratings': False,      # "Goldman upgrades to Buy"
    'market_forecasts': False,     # "UK growth forecast revised"
    'mergers': False,              # Unless dramatic/affects consumers
    'dividends': False             # "Company announces dividend"
}

# Topic Priority Weights (higher = more important)
TOPIC_WEIGHTS = {
    'Cost of Living': 10,      # Highest priority
    'Corporate Drama': 8,
    'Tech Entertainment': 7,
    'Labor Action': 6,
    'Climate': 5,
    'International': 4,
    'Royal Family': 3,
    'Other': 1
}

def calculate_viral_score(headline, summary):
    """
    Calculate viral engagement score (0-100)
    Threshold: >= 5 to be considered for posting

    Args:
        headline: Article headline
        summary: Article summary/description

    Returns:
        float: Score between 0-100
    """
    text = f"{headline} {summary}".lower()
    score = 0

    # Personal impact (+10)
    if any(word in text for word in ['your', 'you', 'families', 'people', 'we', 'us']):
        score += 10

    # Big numbers (+5)
    if any(word in text for word in ['billion', 'million', 'thousands', 'hundreds of']):
        score += 5

    # Records (+15)
    if any(word in text for word in ['record', 'highest ever', 'lowest', 'worst', 'best', 'unprecedented']):
        score += 15

    # Emotion words (+8)
    if any(word in text for word in ['crisis', 'shock', 'scandal', 'outrage', 'fury', 'slams']):
        score += 8

    # Villains (+6)
    if any(word in text for word in ['ceo', 'company', 'corporation', 'boss', 'executive']):
        score += 6

    # Money amounts (+10)
    if any(word in text for word in ['£', '$', 'cost', 'price', 'expensive', 'cheap']):
        score += 10

    # Conflict (+7)
    if any(word in text for word in ['vs', 'versus', 'battle', 'fight', 'war', 'clash']):
        score += 7

    # Viral people bonus (+12)
    viral_people_keywords = [
        'elon musk', 'bezos', 'zuckerberg', 'prince harry', 'meghan',
        'mrbeast', 'andrew tate', 'kardashian', 'trump', 'biden'
    ]
    if any(person in text for person in viral_people_keywords):
        score += 12

    # Check if it's a boring topic (penalty)
    boring_keywords = [
        'earnings', 'quarterly', 'analyst', 'forecast', 'outlook',
        'rating', 'upgrade', 'downgrade', 'consensus', 'eps'
    ]
    if any(keyword in text for keyword in boring_keywords):
        score -= 20  # Heavy penalty

    return min(max(score, 0), 100)  # Clamp between 0-100

def is_socially_viral(headline, summary):
    """
    Determine if content is likely to be viral on social media

    Args:
        headline: Article headline
        summary: Article summary

    Returns:
        tuple: (is_viral: bool, score: float, reason: str)
    """
    score = calculate_viral_score(headline, summary)

    if score >= 20:
        return True, score, "High viral potential"
    elif score >= 10:
        return True, score, "Moderate viral potential"
    elif score >= 5:
        return True, score, "Low viral potential"
    else:
        return False, score, "Unlikely to go viral"

def should_post(article):
    """
    Final decision: post or skip?

    Args:
        article: dict with keys: viral_score, topic

    Returns:
        tuple: (should_post: bool, reason: str)
    """
    viral_score = article.get('viral_score', 0)
    topic = article.get('topic', 'Other')

    # Minimum viral score
    if viral_score < 5:
        return False, "Viral score too low"

    # Block boring topics even with decent scores
    if topic in ['Other', 'Generic Business']:
        if viral_score < 15:  # Need very high score
            return False, "Boring topic"

    # Require higher scores for less popular topics
    if topic in ['International', 'Science']:
        if viral_score < 10:
            return False, "Niche topic needs higher score"

    return True, "Approved for posting"

def get_topic_weight(topic):
    """Get weight for a topic"""
    return TOPIC_WEIGHTS.get(topic, 1)
