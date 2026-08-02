import re
from typing import Dict, Any, List, Tuple

# 19금 및 선정적 단어 필터링 및 우회 사전 (Hidden Dictionary & Safe Mapping)
HIDDEN_MAPPING = {
    "야동": "화보",
    "포르노": "룩북",
    "섹스": "로맨스",
    "19금": "성인",
    "노출": "비키니",
    "섹시": "매력적인",
    "가슴": "바디프로필",
    "엉덩이": "애플힙",
    "av": "화보",
    "오나홀": "성인용품",
    "자위": "힐링",
    "은꼴": "섹시",
    "야한": "매력적인",
    "porn": "lookbook",
    "sex": "romance",
    "nsfw": "model",
    "nude": "bikini"
}

def is_hidden(tag: str) -> bool:
    """단어가 HIDDEN 목록에 있는지 확인"""
    for bad_word in HIDDEN_MAPPING.keys():
        if bad_word in tag.lower():
            return True
    return False

def get_safe_tag(tag: str) -> str:
    """HIDDEN 단어를 SFW 대체 단어로 매핑 (검색 우회용)"""
    for bad_word, safe_word in HIDDEN_MAPPING.items():
        if bad_word in tag.lower():
            return safe_word
    return tag

def extract_taste_keywords(parser) -> Dict[str, Any]:
    """유저의 상호작용(좋아요, 저장, 스토리 등)에서 해시태그를 추출해 취향을 분석"""
    liked = parser.parse_liked_posts()
    saved = parser.parse_saved_posts()
    stories_viewed = parser.parse_stories_viewed()
    story_likes = parser.parse_story_likes()

    tag_scores = {}
    
    def add_tags(posts: List[Dict[str, Any]], weight: int):
        for p in posts:
            tags = p.get('hashtags', [])
            for t in tags:
                if len(t) < 2:  # 너무 짧은 태그 무시
                    continue
                tag_clean = t.lower()
                tag_scores[tag_clean] = tag_scores.get(tag_clean, 0) + weight

    # 가중치 (1-Pick과 동일하게 적용)
    add_tags(stories_viewed, 1)
    add_tags(liked, 2)
    add_tags(saved, 3)
    add_tags(story_likes, 4)

    # 분류
    sfw_tags = {}
    hidden_tags = {}

    for tag, score in tag_scores.items():
        if is_hidden(tag):
            hidden_tags[tag] = score
        else:
            sfw_tags[tag] = score

    # 점수순 정렬 후 상위 추출
    sorted_sfw = sorted(sfw_tags.items(), key=lambda x: x[1], reverse=True)
    sorted_hidden = sorted(hidden_tags.items(), key=lambda x: x[1], reverse=True)

    top_sfw = [t[0] for t in sorted_sfw[:5]]
    
    # Hidden의 경우 우회된 태그로 변환하여 저장
    top_hidden = []
    for t, score in sorted_hidden[:5]:
        safe = get_safe_tag(t)
        if safe not in top_hidden:
            top_hidden.append(safe)

    return {
        "raw_sfw_tags": [t[0] for t in sorted_sfw[:10]],
        "raw_hidden_tags": [t[0] for t in sorted_hidden[:10]],
        "search_sfw_queries": top_sfw,
        "search_hidden_queries": top_hidden,
        "total_tags_found": len(tag_scores)
    }
