import random

def get_brand_updates():
    all_tweets = [
        # Fenty
        {"brand": "Fenty Beauty", "tweet": "Just dropped 10 new shades of our best-selling foundation!"},
        {"brand": "Fenty Beauty", "tweet": "Find your perfect Pro Filt’r match now with new AI tone assist."},
        {"brand": "Fenty Beauty", "tweet": "Gloss Bomb Heat just restocked 🔥"},
        
        # NARS
        {"brand": "NARS", "tweet": "Now in mini sizes – perfect for travel season!"},
        {"brand": "NARS", "tweet": "Try our new Light Reflecting Foundation."},
        {"brand": "NARS", "tweet": "Our Radiant Creamy Concealer is now in 50+ shades."},

        # Maybelline
        {"brand": "Maybelline", "tweet": "Get 25% off all Fit Me products this weekend only!"},
        {"brand": "Maybelline", "tweet": "SuperStay skin tint just launched — transfer-proof tested."},
        {"brand": "Maybelline", "tweet": "Meet our first skin-like matte foundation — Fit Me Luminous."},

        # Glossier
        {"brand": "Glossier", "tweet": "New Stretch Fluid Foundation is here in 32 shades!"},
        {"brand": "Glossier", "tweet": "Dewy skin, meet Phase 2 set ✨"},
        
        # Rare Beauty
        {"brand": "Rare Beauty", "tweet": "Kind Words matte lipsticks restocked today."},
        {"brand": "Rare Beauty", "tweet": "Selena’s fav combo: Positive Light Tinted Moisturizer + Brightener"},
        
        # Miscellaneous
        {"brand": "ILIA", "tweet": "True Skin Serum Foundation is back — natural finish lovers rejoice."},
        {"brand": "MAC", "tweet": "Studio Fix just got a shade expansion!"},
        {"brand": "e.l.f.", "tweet": "Halo Glow is *that* girl. TikTok’s #1 skin tint now at Target."},
    ]

    # Randomize for freshness
    return random.sample(all_tweets, 6)
