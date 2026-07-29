from typing import Dict, List, Any

def analyze_secret_collection(parser) -> Dict[str, Any]:
    saved_posts = parser.parse_saved_posts()
    liked_posts = parser.parse_liked_posts()
    collections = parser.parse_saved_collections()

    liked_urls = {p.get('url') for p in liked_posts if p.get('url')}
    
    # Saved but not liked
    secret_posts = [p for p in saved_posts if p.get('url') and p.get('url') not in liked_urls]
    
    total_saved = len(saved_posts) or 1
    secret_ratio = int((len(secret_posts) / total_saved) * 100)

    # Collect hashtags from secret posts
    secret_hashtags = {}
    for p in secret_posts:
        for tag in p.get('hashtags', []):
            t_l = tag.lower()
            secret_hashtags[t_l] = secret_hashtags.get(t_l, 0) + 1

    sorted_secret_tags = [
        {"tag": tag, "count": count}
        for tag, count in sorted(secret_hashtags.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    # Process Collections
    formatted_collections = []
    for c in collections:
        formatted_collections.append({
            "name": c.get('name', '기본 저장'),
            "type": c.get('type', '기본'),
            "privacy": c.get('privacy', '비공개'),
            "posts_count": c.get('posts_count', 0),
            "sample_posts": [
                {
                    "url": p.get('url', ''),
                    "caption": (p.get('caption', '') or '')[:80],
                    "owner": p.get('owner', '')
                }
                for p in c.get('posts', [])[:3]
            ]
        })

    return {
        "total_saved": len(saved_posts),
        "total_liked": len(liked_posts),
        "secret_posts_count": len(secret_posts),
        "secret_ratio_percentage": secret_ratio,
        "secret_hashtags": sorted_secret_tags,
        "collections": formatted_collections
    }
