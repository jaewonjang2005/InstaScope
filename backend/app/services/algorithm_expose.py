from typing import Dict, List, Any

def analyze_algorithm_expose(parser) -> Dict[str, Any]:
    categories = parser.parse_ad_categories()
    advertisers = parser.parse_advertisers()
    locations = parser.parse_locations()
    logins = parser.parse_login_activity()

    # Unique IPs & User Agents
    unique_ips = list({l['ip'] for l in logins if l.get('ip')})
    user_agents = list({l['user_agent'] for l in logins if l.get('user_agent')})

    # Privacy exposure score (0-100)
    exposure_score = min(100, int((len(categories) * 3) + (len(advertisers) * 0.1) + (len(locations) * 5) + (len(unique_ips) * 10)))

    # Categorize ad categories for tag cloud
    tagged_categories = []
    for cat in categories:
        tagged_categories.append({
            "text": cat,
            "weight": 10 if ("single" in cat.lower() or "birthday" in cat.lower() or "travel" in cat.lower()) else 5
        })

    return {
        "exposure_score": exposure_score,
        "ad_categories_count": len(categories),
        "ad_categories": tagged_categories[:30],
        "advertisers_count": len(advertisers),
        "top_advertisers": advertisers[:20],
        "tracked_locations": locations,
        "unique_ips": unique_ips[:5],
        "primary_device": user_agents[0] if user_agents else "Android Device"
    }
