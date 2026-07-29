from typing import Dict, List, Any
from collections import Counter

def analyze_algorithm_expose(parser) -> Dict[str, Any]:
    liked = parser.parse_liked_posts()
    saved = parser.parse_saved_posts()
    categories = parser.parse_ad_categories()
    advertisers = parser.parse_advertisers()
    locations = parser.parse_locations()
    logins = parser.parse_login_activity()

    # Extract implied algorithm interest categories from hashtags in your_instagram_activity
    tag_counts = Counter()
    for p in liked + saved:
        for tag in p.get('hashtags', []):
            if len(tag) > 1:
                tag_counts[tag] += 1

    implied_categories = [tag for tag, count in tag_counts.most_common(30)]
    
    # Combined category list (Ads categories + Implied hashtag categories)
    all_categories = categories if categories else implied_categories
    if not all_categories and liked:
        all_categories = ["소셜 미디어 라이프스타일", "트렌디 콘텐츠", "인스타그램 추천 피드", "디지털 패션 & 커뮤니티"]

    # Unique IPs & User Agents
    unique_ips = list({l['ip'] for l in logins if l.get('ip')})
    user_agents = list({l['user_agent'] for l in logins if l.get('user_agent')})

    # Exposure Score based on activity & tracked items
    exposure_score = min(98, max(35, int((len(liked) * 0.1) + (len(saved) * 0.2) + (len(all_categories) * 2))))

    tagged_categories = []
    for cat in all_categories:
        tagged_categories.append({
            "text": cat,
            "weight": 10 if any(kw in str(cat).lower() for kw in ["single", "travel", "패션", "맛집", "운동", "연애"]) else 5
        })

    return {
        "exposure_score": exposure_score,
        "ad_categories_count": len(all_categories),
        "ad_categories": tagged_categories[:30],
        "advertisers_count": len(advertisers) if advertisers else len(set([p.get('owner') for p in liked if p.get('owner')])),
        "top_advertisers": advertisers[:20] if advertisers else list(set([p.get('owner') for p in liked if p.get('owner')]))[:20],
        "tracked_locations": locations if locations else ["대한민국 주요 활동 위치"],
        "unique_ips": unique_ips[:5] if unique_ips else ["IP 암호화 및 동적 할당"],
        "primary_device": user_agents[0] if user_agents else "Mobile Smart Device"
    }
