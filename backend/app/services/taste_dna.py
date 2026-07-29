from typing import Dict, List, Any
from datetime import datetime, timezone

CATEGORY_KEYWORDS = {
    "애니/덕질": ["anime", "manga", "vtuber", "hololive", "frieren", "cosplay", "art", "character", "illustration", "만화", "애니", "덕질", "일러스트"],
    "여행/풍경": ["travel", "japan", "trip", "tokyo", "busan", "cafe", "풍경", "여행", "카페", "맛집", "스냅"],
    "자기계발/지식": ["study", "motivation", "book", "ai", "tech", "growth", "성공", "자기계발", "공부", "지식", "꿀팁", "뉴스", "재테크"],
    "패션/뷰티": ["fashion", "ootd", "beauty", "style", "fit", "코디", "패션", "옷", "메이크업"],
    "동물/반려동물": ["cat", "dog", "animal", "pet", "cute", "고양이", "강아지", "동물", "귀여운"],
    "유머/엔터": ["meme", "lol", "humor", "funny", "유머", "웃긴", "릴스", "밈"]
}

def analyze_taste_dna(parser) -> Dict[str, Any]:
    liked = parser.parse_liked_posts()
    saved = parser.parse_saved_posts()
    videos = parser.parse_videos_watched()
    posts_viewed = parser.parse_posts_viewed()
    stories_viewed = parser.parse_stories_viewed()
    story_likes = parser.parse_story_likes()

    # 1. Category Radar Chart Analysis
    category_counts = {cat: 0 for cat in CATEGORY_KEYWORDS}
    all_hashtags = {}
    
    all_records = liked + saved + videos
    for item in all_records:
        tags = item.get('hashtags', [])
        caption = (item.get('caption', '') or '').lower()
        
        for tag in tags:
            tag_l = tag.lower()
            all_hashtags[tag_l] = all_hashtags.get(tag_l, 0) + 1
            for cat, keywords in CATEGORY_KEYWORDS.items():
                if any(kw in tag_l for kw in keywords):
                    category_counts[cat] += 1
                    
        for cat, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in caption for kw in keywords):
                category_counts[cat] += 1

    total_cat = sum(category_counts.values()) or 1
    radar_data = [
        {"category": cat, "score": min(100, int((count / total_cat) * 300))}
        for cat, count in category_counts.items()
    ]

    # Top Hashtags
    sorted_hashtags = sorted(all_hashtags.items(), key=lambda x: x[1], reverse=True)[:15]
    top_hashtags = [{"tag": tag, "count": count} for tag, count in sorted_hashtags]

    # 2. Time-of-Day Distribution (Hourly: 0..23)
    time_dist = {f"{h:02d}": 0 for h in range(24)}
    for item in liked + saved + stories_viewed + story_likes:
        ts = item.get('timestamp', 0)
        if ts > 0:
            try:
                dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                hour_str = f"{dt.hour:02d}"
                time_dist[hour_str] += 1
            except Exception:
                pass

    total_time = sum(time_dist.values()) or 1
    dawn_count = sum(time_dist[f"{h:02d}"] for h in range(0, 6))
    night_count = sum(time_dist[f"{h:02d}"] for h in range(18, 24))
    dawn_ratio = (dawn_count + night_count) / total_time

    # 3. Mild vs Spicy vs Fire Meter
    # Fire factors: High saved-to-liked ratio, high dawn activity ratio, niche subculture tags
    saved_len = len(saved)
    liked_len = len(liked)
    save_like_ratio = (saved_len / (liked_len + 1))
    
    # Calculate Spicy Level 0-100
    spicy_score = int(min(100, max(10, (save_like_ratio * 30) + (dawn_ratio * 40) + (len(sorted_hashtags) * 2))))
    
    if spicy_score < 40:
        spicy_level = "순한맛 (Mild 🥛)"
        spicy_desc = "대중적이고 평화로운 취향을 가진 순수한 보스턴백 스타일!"
    elif spicy_score < 75:
        spicy_level = "매콤함 (Spicy 🌶️)"
        spicy_desc = "자신만의 뚜렷한 취향과 알고리즘을 구축한 취향 명사수!"
    else:
        spicy_level = "불닭 (Fire 🔥)"
        spicy_desc = "새벽녘 비밀 취향과 은밀한 컬렉션을 대량 보유한 자타공인 불닭 알고리즘 마스터!"

    # 4. Interaction Pyramid
    pyramid = [
        {"stage": "게시물/릴스 시청", "count": len(posts_viewed) + len(videos)},
        {"stage": "스토리 시청", "count": len(stories_viewed)},
        {"stage": "좋아요 반응", "count": len(liked) + len(story_likes)},
        {"stage": "비밀 저장", "count": len(saved)},
    ]

    return {
        "spicy_score": spicy_score,
        "spicy_level": spicy_level,
        "spicy_desc": spicy_desc,
        "radar_data": radar_data,
        "top_hashtags": top_hashtags,
        "time_distribution": time_dist,
        "interaction_pyramid": pyramid
    }
