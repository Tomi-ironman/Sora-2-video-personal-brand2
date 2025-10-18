#!/usr/bin/env python3
"""
ZENYAI AFFILIATE PARTNERSHIPS DATABASE - BATCH 1
60 potential affiliate partners across Audio, Film, Podcast, and Gaming
"""

AFFILIATE_PARTNERS_BATCH1 = {
    # AUDIO CREATORS (15)
    "audio_1": {
        "name": "Sound Design Live",
        "category": "audio",
        "platform": "YouTube",
        "size": "mid",
        "followers": "245K",
        "focus": "Sound design tutorials and workflows",
        "why_partner": "Large audience of audio professionals struggling with organization",
        "contact": {"twitter": "@sounddesignlive", "youtube": "SoundDesignLive"},
        "engagement_rate": "4.2%"
    },
    "audio_2": {
        "name": "Andrew Scheps",
        "category": "audio",
        "platform": "YouTube",
        "size": "mid",
        "followers": "180K",
        "focus": "Mixing engineer with tutorials",
        "why_partner": "Respected mixing engineer, audience needs file management",
        "contact": {"twitter": "@andrewscheps", "youtube": "AndrewScheps"},
        "engagement_rate": "3.8%"
    },
    "audio_3": {
        "name": "Produce Like A Pro",
        "category": "audio",
        "platform": "YouTube",
        "size": "mid",
        "followers": "520K",
        "focus": "Music production education",
        "why_partner": "Huge music production audience with organization pain",
        "contact": {"youtube": "ProduceLikeAPro", "website": "producelikeapro.com"},
        "engagement_rate": "3.5%"
    },
    "audio_4": {
        "name": "In The Mix",
        "category": "audio",
        "platform": "YouTube",
        "size": "mid",
        "followers": "830K",
        "focus": "Music production tutorials",
        "why_partner": "Large beginner/intermediate audience needing organization tools",
        "contact": {"youtube": "inthemix", "twitter": "@inthemixyt"},
        "engagement_rate": "4.1%"
    },
    "audio_5": {
        "name": "Venus Theory",
        "category": "audio",
        "platform": "YouTube",
        "size": "small",
        "followers": "156K",
        "focus": "Electronic music production",
        "why_partner": "Engaged community, heavy sample library users",
        "contact": {"youtube": "VenusTheory", "twitter": "@venustheory"},
        "engagement_rate": "5.2%"
    }
}

def get_batch1_by_category(category=None):
    """Get batch 1 affiliates by category"""
    if category:
        return {k: v for k, v in AFFILIATE_PARTNERS_BATCH1.items() if v['category'] == category}
    return AFFILIATE_PARTNERS_BATCH1

def get_batch1_count():
    """Get count by category"""
    counts = {}
    for partner in AFFILIATE_PARTNERS_BATCH1.values():
        cat = partner['category']
        counts[cat] = counts.get(cat, 0) + 1
    return counts
