"""Country-specific configurations for news feeds, topics, and politicians"""

# Active countries toggle - change this to enable/disable countries
ACTIVE_COUNTRIES = ['UK', 'US']  # Multi-country enabled!

# Country configurations
COUNTRIES = {
    'UK': {
        'name': 'United Kingdom',
        'flag': '🇬🇧',
        'timezone': 'Europe/London',
        'feeds': {
            # Main news sources
            'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
            'Guardian': 'https://www.theguardian.com/uk/rss',
            'Sky News': 'https://feeds.skynews.com/feeds/rss/uk.xml',
            'Telegraph': 'https://www.telegraph.co.uk/news/rss.xml',
            'Independent': 'https://www.independent.co.uk/news/uk/rss',
            # Lifestyle sources
            'BBC Lifestyle': 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
            'Guardian Life': 'https://www.theguardian.com/uk/lifeandstyle/rss',
            'Telegraph Fashion': 'https://www.telegraph.co.uk/fashion/rss.xml',
            'Telegraph Travel': 'https://www.telegraph.co.uk/travel/rss.xml',
            'Metro Lifestyle': 'https://metro.co.uk/lifestyle/feed/',
            'Evening Standard Food': 'https://www.standard.co.uk/topic/food-drink/rss'
        },
        'local_topics': {
            'NHS': ['nhs', 'national health service', 'hospital waiting', 'gp appointment'],
            'Brexit': ['brexit', 'northern ireland protocol', 'windsor framework'],
            'UK Politics': ['downing street', 'westminster', 'parliament', 'prime minister'],
            'UK Cost of Living': ['council tax', 'tv licence', 'ofgem', 'energy price cap']
        },
        'politicians': {
            'Keir Starmer': ['keir starmer', 'starmer'],
            'Nigel Farage': ['nigel farage', 'farage'],
            'Rishi Sunak': ['rishi sunak', 'sunak'],
            'Lee Anderson': ['lee anderson']
        }
    },
    'US': {
        'name': 'United States',
        'flag': '🇺🇸',
        'timezone': 'America/New_York',
        'feeds': {
            # Main news sources
            'CNN': 'http://rss.cnn.com/rss/cnn_topstories.rss',
            'NY Times': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
            'Washington Post': 'https://feeds.washingtonpost.com/rss/politics',
            'Fox News': 'https://moxie.foxnews.com/google-publisher/latest.xml',
            'NPR': 'https://feeds.npr.org/1001/rss.xml',
            # Lifestyle sources
            'NY Times Style': 'https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml',
            'NY Times Travel': 'https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml',
            'CNN Entertainment': 'http://rss.cnn.com/rss/cnn_showbiz.rss',
            'NPR Food': 'https://feeds.npr.org/1053/rss.xml',
            'E! News': 'https://eonline.com/syndication/feeds/rssfeeds/topstories.xml',
            'People Magazine': 'https://people.com/feeds/all-articles.rss'
        },
        'local_topics': {
            'US Healthcare': ['medicare', 'medicaid', 'health insurance', 'obamacare', 'aca'],
            'Immigration': ['border', 'immigration', 'deportation', 'asylum', 'migrants'],
            'Gun Control': ['gun control', 'second amendment', 'shooting', 'firearms'],
            'US Politics': ['white house', 'congress', 'senate', 'house of representatives'],
            'US Cost of Living': ['401k', 'student debt', 'medical bills', 'insurance premium']
        },
        'politicians': {
            'Donald Trump': ['donald trump', 'trump'],
            'Joe Biden': ['joe biden', 'biden', 'president biden'],
            'Ron DeSantis': ['ron desantis', 'desantis'],
            'AOC': ['alexandria ocasio-cortez', 'ocasio-cortez', 'aoc']
        }
    }
}

# Global topics (relevant to multiple countries)
GLOBAL_TOPICS = {
    'Climate': ['climate change', 'global warming', 'carbon emissions', 'net zero', 'renewable energy'],
    'Tech': ['artificial intelligence', 'ai', 'chatgpt', 'openai', 'meta', 'google', 'apple'],
    'International': ['ukraine', 'russia', 'china', 'middle east', 'israel', 'gaza'],
    'Royal Family': ['king charles', 'prince william', 'kate middleton', 'prince harry', 'meghan markle'],
    'Entertainment': ['celebrity', 'hollywood', 'netflix', 'disney', 'streaming'],
    'Science': ['nasa', 'space', 'research', 'study finds', 'scientists']
}

# High-engagement public figures (Tech Billionaires, Influencers, Royals, Celebrities)
VIRAL_PEOPLE = {
    'Tech Billionaires': {
        'Elon Musk': ['elon musk', 'musk', 'tesla', 'spacex', 'twitter', 'x corp'],
        'Mark Zuckerberg': ['mark zuckerberg', 'zuckerberg', 'meta', 'facebook'],
        'Jeff Bezos': ['jeff bezos', 'bezos', 'amazon', 'blue origin'],
        'Sam Altman': ['sam altman', 'altman', 'openai'],
        'Larry Ellison': ['larry ellison', 'ellison', 'oracle']
    },
    'Controversial Influencers': {
        'MrBeast': ['mrbeast', 'jimmy donaldson', 'beast games'],
        'Andrew Tate': ['andrew tate', 'tate'],
        'Kim Kardashian': ['kim kardashian'],
        'Kylie Jenner': ['kylie jenner'],
        'Hasan Piker': ['hasan piker', 'hasanabi']
    },
    'Royal Drama': {
        'Prince Harry': ['prince harry', 'harry'],
        'Meghan Markle': ['meghan markle', 'duchess of sussex'],
        'King Charles': ['king charles'],
        'Prince William': ['prince william'],
        'Kate Middleton': ['kate middleton', 'princess of wales', 'princess kate']
    },
    'Celebrities': {
        'Beyoncé': ['beyonce', 'beyoncé'],
        'Rihanna': ['rihanna'],
        'Taylor Swift': ['taylor swift'],
        'Billie Eilish': ['billie eilish'],
        'Lana Del Rey': ['lana del rey'],
        'Cardi B': ['cardi b']
    }
}

# Helper functions
def get_country_config(country_code):
    """Get configuration for specific country"""
    return COUNTRIES.get(country_code.upper(), None)

def get_active_countries():
    """Get list of active countries"""
    return ACTIVE_COUNTRIES

def get_global_topics():
    """Get global topics dictionary"""
    return GLOBAL_TOPICS

def get_viral_people():
    """Get viral people dictionary"""
    return VIRAL_PEOPLE
