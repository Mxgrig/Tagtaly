"""Tagtaly configuration package"""

from .countries import (
    ACTIVE_COUNTRIES,
    COUNTRIES,
    GLOBAL_TOPICS,
    get_country_config,
    get_active_countries,
    get_global_topics
)

from .viral_topics import (
    VIRAL_TOPICS,
    BORING_TOPICS,
    TOPIC_WEIGHTS,
    is_socially_viral,
    calculate_viral_score
)

__all__ = [
    'ACTIVE_COUNTRIES',
    'COUNTRIES',
    'GLOBAL_TOPICS',
    'get_country_config',
    'get_active_countries',
    'get_global_topics',
    'VIRAL_TOPICS',
    'BORING_TOPICS',
    'TOPIC_WEIGHTS',
    'is_socially_viral',
    'calculate_viral_score'
]
