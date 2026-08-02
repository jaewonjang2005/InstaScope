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
    "nude": "bikini",
    "그라비아": "화보",
    "gravure": "model",
    "코스프레": "패션",
    "cosplay": "fashion",
    "수영복": "여름",
    "맥심": "잡지",
    "란제리": "패션",
    "속옷": "패션"
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

    tag_stats = {}
    tag_to_urls = {}
    
    import time
    current_time = time.time()
    
    def process_posts(posts: List[Dict[str, Any]], action_type: str):
        for p in posts:
            ts = p.get('timestamp', 0)
            tags = p.get('hashtags', [])
            url = p.get('url', '')
            
            # Time Decay Weighting 복원
            time_weight = 1.0
            if ts > 0:
                days_ago = (current_time - ts) / (60 * 60 * 24)
                if days_ago <= 30:
                    time_weight = 3.0
                elif days_ago <= 180:
                    time_weight = 1.5
            
            for t in tags:
                if len(t) < 2:
                    continue
                tag_clean = t.lower()
                
                if tag_clean not in tag_stats:
                    tag_stats[tag_clean] = {'public': 0.0, 'private': 0.0}
                
                # Public: 좋아요, 스토리 / Private: 저장, 컬렉션
                if action_type in ['liked', 'story']:
                    tag_stats[tag_clean]['public'] += time_weight
                else:
                    tag_stats[tag_clean]['private'] += (time_weight * 3.0)  # 저장(Save) 기본 가중치
                
                if url:
                    if tag_clean not in tag_to_urls:
                        tag_to_urls[tag_clean] = set()
                    if len(tag_to_urls[tag_clean]) < 10:
                        tag_to_urls[tag_clean].add(url)

    process_posts(liked, 'liked')
    process_posts(saved, 'saved')
    process_posts(stories_viewed, 'story')
    process_posts(story_likes, 'story')

    try:
        collections = parser.parse_saved_collections()
        for col in collections:
            col_tags = col.get('hashtags', [])
            for t in col_tags:
                if len(t) < 2:
                    continue
                tag_clean = t.lower()
                if tag_clean not in tag_stats:
                    tag_stats[tag_clean] = {'public': 0.0, 'private': 0.0}
                tag_stats[tag_clean]['private'] += 5.0  # 컬렉션은 시간 정보가 없으므로 고정 가중치 5.0
    except Exception as e:
        print(f"Collection parse error: {e}")

    # === [다층적 상호작용 기반 '찐 취향(True Affinity)' 산출] ===
    STOP_WORDS = {"일상", "소통", "맞팔", "선팔", "좋아요반사", "f4f", "ootd", "좋아요", "팔로우", "데일리"}
    
    # 1. 태그별 Total Volume 계산 및 Private Score 중앙값(Median) 도출
    private_scores = []
    tag_scores = {}  # SFW(대중적 취향) 정렬을 위한 총 볼륨 저장용
    
    for tag, stats in tag_stats.items():
        total = stats['public'] + stats['private']
        tag_scores[tag] = total
        
        if tag not in STOP_WORDS and stats['private'] > 0:
            private_scores.append(stats['private'])
            
    import statistics
    median_private = statistics.median(private_scores) if private_scores else 0

    # 2. SFW(대중적 취향) Top 10 추출
    sorted_by_total = sorted([t for t in tag_scores.items() if t[0] not in STOP_WORDS], key=lambda x: x[1], reverse=True)
    top_sfw = [t[0] for t in sorted_by_total[:15]]

    # 3. Mathematical Hidden (수학적 은밀한 취향) 도출
    hidden_candidates = []
    for tag, stats in tag_stats.items():
        # Top 5 SFW(완전 대중적인 메인 취향)이거나 불용어면 제외
        if tag in STOP_WORDS or tag in top_sfw[:5]:
            continue
            
        # 해당 사용자의 Private 중앙값 이상인 태그들만 대상 (노이즈 제거)
        if stats['private'] >= median_private:
            ratio = stats['private'] / (stats['public'] + 1.0)
            hidden_candidates.append((tag, ratio))
            
    # Private Ratio가 높은 순서대로 정렬하여 Secret Picks 선정
    sorted_by_ratio = sorted(hidden_candidates, key=lambda x: x[1], reverse=True)
    secret_picks = [t[0] for t in sorted_by_ratio[:10]]



    # --- [데이터 전처리 및 분류 파트] ---
    # 기존 파일 최상단에 있는 HIDDEN_MAPPING 키워드들을 명시적 숨겨진(Hidden) 키워드로 활용합니다.
    EXPLICIT_HIDDEN_KEYWORDS = set(HIDDEN_MAPPING.keys())
    IMPLICIT_HIDDEN_KEYWORDS = {
        "반캠", "직캠", "섹시", "요가", "비키니", "룩북", "화보", "바디프로필",
        "애니", "anime", "버튜버", "vtuber", "홀로라이브", "hololive", 
        "미소녀", "otaku", "오타쿠", "만화", "manga", "원신", "블루아카이브", "니케",
        "코믹월드", "일러스트", "레이싱모델", "피팅모델", "풀빌라", "씹덕", "2d"
    }

    def classify_tag_type(tag: str) -> str:
        t = tag.lower()
        
        for bad in EXPLICIT_HIDDEN_KEYWORDS:
            # False positive 방지 규칙 (영어)
            if bad == 'av' and t != 'av':
                continue
            if bad == 'porn' and t.endswith('porn') and t not in ('porn', 'pornhub'):
                continue
            if bad == 'sex' and t != 'sex':
                continue
            # False positive 방지 규칙 (한국어)
            if bad == '가슴' and any(x in t for x in ['닭가슴살', '가슴뛰는', '가슴아픈', '가슴속', '가슴뭉클']):
                continue
            if bad == '야한' and any(x in t for x in ['해야한', '다양한', '유리한', '불리한', '피곤한', '미안한', '치열한', '야한다', '야한데', '야한지']):
                continue
            if bad == '야동' and '심야동' in t:
                continue
            if bad == '노출' and any(x in t for x in ['장노출', '이중노출', '노출콘크리트', '과다노출']):
                continue
            if bad == '엉덩이' and '엉덩이탐정' in t:
                continue
            if bad == '자위' and '자위대' in t:
                continue
            if bad == '섹스' and '섹스피어' in t:
                continue
            if bad == '은꼴' and '닮은꼴' in t:
                continue
            if bad == '섹시' and '섹시야마' in t:
                continue
            
            if bad in t:
                return "EXPLICIT_HIDDEN"
                
        for imp in IMPLICIT_HIDDEN_KEYWORDS:
            # False positive 방지 규칙
            if imp == '비키니' and '비키니시티' in t:
                continue
            if imp == '섹시' and '섹시야마' in t:
                continue
            if imp == '화보' and '패션화보' in t:
                continue
            if imp == '반캠' and any(x in t for x in ['반캠핑', '반캠프']):
                continue
            if imp == '직캠' and any(x in t for x in ['직캠프', '직캠핑']):
                continue
                
            if imp in t:
                return "IMPLICIT_HIDDEN"
                
        return "SFW"

    def preprocess_and_classify_tags(tag_scores: Dict[str, int]) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int]]:
        """
        입력된 태그 점수 데이터를 불용어, 명시적 숨겨진(Hidden), 잠재적 숨겨진(Hidden), 맞춤(SFW) 태그로 분류합니다.

        Args:
            tag_scores (Dict[str, int]): {태그: 점수} 형태의 원본 데이터

        Returns:
            Tuple[Dict, Dict, Dict]: 
                (명시적 숨겨진(Hidden) 태그 딕셔너리, 잠재적 숨겨진(Hidden) 태그 딕셔너리, 맞춤(SFW) 태그 딕셔너리)
        """
    
        # 분류된 태그들을 담을 빈 딕셔너리들을 초기화합니다.
        explicit_hidden_tags = {}
        implicit_hidden_tags = {}
        sfw_tags = {}

        # 원본 태그 점수 딕셔너리를 하나씩 순회합니다.
        for tag, score in tag_scores.items():
        
            # 1. 불용어인지 먼저 확인합니다. 불용어라면 분류 과정을 건너뜁니다.
            if tag in STOP_WORDS:
                continue
        
            # 2. 불용어가 아니면, 태그의 종류를 판별합니다.
            tag_type = classify_tag_type(tag)
        
            # 3. 판별된 종류에 따라 알맞은 딕셔너리에 태그와 점수를 저장합니다.
            if tag_type == "EXPLICIT_HIDDEN":
                explicit_hidden_tags[tag] = score
            elif tag_type == "IMPLICIT_HIDDEN":
                implicit_hidden_tags[tag] = score
            else:
                sfw_tags[tag] = score
            
        # 분류가 완료된 세 개의 딕셔너리를 튜플 형태로 반환합니다.
        return explicit_hidden_tags, implicit_hidden_tags, sfw_tags

    # --- [사용 예시] ---
    if __name__ == '__main__':
        # 가상의 태그 점수 데이터
        sample_tag_scores = {
            "일상": 10, "소통": 8, "섹시": 25, "직캠": 30, "포르노": 5, 
            "요가": 15, "게임": 20, "브라": 12, "캠핑": 18
        }
    
        # 함수를 호출하여 태그들을 분류합니다.
        explicit_hidden, implicit_hidden, sfw = preprocess_and_classify_tags(sample_tag_scores)
    
        # 결과 출력
        print("--- 명시적 숨겨진(Hidden) 태그 ---")
        print(explicit_hidden)
        print("\n--- 잠재적 숨겨진(Hidden) 태그 ---")
        print(implicit_hidden)
        print("\n--- 맞춤(SFW) 태그 ---")
        print(sfw)

        # --- [선호도 점수 계산 파트] ---

    def calculate_affinity_scores(
        explicit_hidden_tags: Dict[str, int], 
        implicit_hidden_tags: Dict[str, int], 
        sfw_tags: Dict[str, int]
    ) -> Dict[str, float]:
        """
        분류된 태그 딕셔너리들을 바탕으로 각 토픽(카테고리)별 선호도 점수를 계산합니다.
        '숨겨진 취향(Hidden)' 점수는 명시적과 잠재적 점수를 합산하여 산출합니다.

        Args:
            explicit_hidden_tags (Dict[str, int]): 명시적 숨겨진(Hidden) 태그와 점수
            implicit_hidden_tags (Dict[str, int]): 잠재적 숨겨진(Hidden) 태그와 점수
            sfw_tags (Dict[str, int]): 맞춤(SFW) 태그와 점수

        Returns:
            Dict[str, float]: {카테고리 이름: 총 점수} 형태의 선호도 점수 딕셔너리
        """
    
        # 1. 각 카테고리별 점수를 합산합니다.
        total_explicit_score = sum(explicit_hidden_tags.values())
        total_implicit_score = sum(implicit_hidden_tags.values())
        total_general_score = sum(sfw_tags.values())

        # 2. '숨겨진 취향(Hidden)' 점수는 명시적과 잠재적 점수를 합산하여 계산합니다.
        hidden_affinity_score = total_explicit_score + total_implicit_score
    
        # 3. 최종 선호도 점수 딕셔너리를 구성합니다.
        affinity_scores = {
            "HIDDEN": hidden_affinity_score,
            "SFW": total_general_score
        }
    
        # 4. 점수가 0인 카테고리는 결과에서 제외하여 불필요한 계산을 방지합니다.
        # (filter를 사용하여 딕셔너리 컴프리헨션을 깔끔하게 처리합니다)
        final_scores = {category: score for category, score in affinity_scores.items() if score > 0}
    
        return final_scores

    # --- [사용 예시] ---
    if __name__ == '__main__':
        # 이전 단계에서 분류된 가상의 데이터라고 가정합니다.
        sample_explicit_hidden = {"포르노": 5, "브라": 12}
        sample_implicit_hidden = {"섹시": 25, "직캠": 30, "요가": 15}
        sample_sfw_tags = {"게임": 20, "캠핑": 18}

        # 함수를 호출하여 선호도 점수를 계산합니다.
        affinity_scores = calculate_affinity_scores(
            explicit_hidden_tags=sample_explicit_hidden,
            implicit_hidden_tags=sample_implicit_hidden,
            sfw_tags=sample_sfw_tags
        )
    
        # 결과 출력
        print("--- 최종 선호도 점수 ---")
        print(affinity_scores)
        # 예상 출력: {'HIDDEN': 87, 'SFW': 38}
        # (HIDDEN: 5+12+25+30+15 = 87, SFW: 20+18 = 38)

        # --- [임계값 기반 동적 라우팅 파트] ---

    def route_by_affinity(affinity_scores: Dict[str, float], threshold: float = 0.4) -> str:
        """
        계산된 선호도 점수를 바탕으로, 임계값에 따라 검색 파이프라인을 결정합니다.

        Args:
            affinity_scores (Dict[str, float]): calculate_affinity_scores 함수가 반환한 점수 딕셔너리
            threshold (float): '숨겨진 취향(Hidden)'을 지배적으로 판단할 최소 비중 (0.0 ~ 1.0)

        Returns:
            str: 결정된 검색 파이프라인 이름 ("HIDDEN", "SFW", "FALLBACK")
        """
    
        # 1. 선호도 점수 데이터가 비어있는지 확인 (가장 먼저 할 일)
        if not affinity_scores:
            return "FALLBACK"  # 분석할 데이터가 없으면 안전한 기본 파이프라인으로 라우팅

        # 2. 전체 취향 점수의 합계를 계산합니다.
        total_score = sum(affinity_scores.values())

        # 3. 'HIDDEN' 카테고리의 점수를 가져옵니다. 만약 없으면 0으로 처리합니다.
        hidden_score = affinity_scores.get("HIDDEN", 0)

        # 4. 'HIDDEN' 취향의 점수 비중(비율)을 계산합니다.
        hidden_ratio = hidden_score / total_score if total_score > 0 else 0

        # 5. 임계값과 비교하여 최종 라우팅을 결정합니다.
        if hidden_ratio >= threshold:
            # '숨겨진 취향(Hidden)'이 지배적이라고 판단되면 HIDDEN 파이프라인으로 라우팅
            return "HIDDEN"
        else:
            # 그렇지 않으면 일반적인 콘텐츠 파이프라인으로 라우팅
            return "SFW"

    # --- [사용 예시] ---
    if __name__ == '__main__':
        # 이전 단계에서 계산된 가상의 선호도 점수라고 가정합니다.
        sample_affinity_scores_1 = {"HIDDEN": 87, "SFW": 38}  # 숨겨진 취향(Hidden)이 강한 경우
        sample_affinity_scores_2 = {"HIDDEN": 20, "SFW": 80}  # 일반 취향이 강한 경우
        sample_affinity_scores_3 = {}                           # 데이터가 없는 경우

        # 함수를 호출하여 라우팅 결과를 확인합니다. (기본 임계값 0.4 사용)
        route_1 = route_by_affinity(sample_affinity_scores_1)
        route_2 = route_by_affinity(sample_affinity_scores_2)
        route_3 = route_by_affinity(sample_affinity_scores_3)
    
        # 결과 출력
        print("--- 라우팅 결과 (숨겨진 취향(Hidden) 강함) ---")
        print(f"점수: {sample_affinity_scores_1}, 라우팅: {route_1}") # 예상: "HIDDEN"
    
        print("\n--- 라우팅 결과 (일반 취향 강함) ---")
        print(f"점수: {sample_affinity_scores_2}, 라우팅: {route_2}") # 예상: "SFW"
    
        print("\n--- 라우팅 결과 (데이터 없음) ---")
        print(f"점수: {sample_affinity_scores_3}, 라우팅: {route_3}") # 예상: "FALLBACK"

        # --- [최종 검색어 생성 및 폴백 파트] ---

    def generate_final_queries(
        explicit_hidden_tags: Dict[str, float],
        implicit_hidden_tags: Dict[str, float],
        sfw_tags: Dict[str, float],
        secret_picks: List[str] = [],
        num_queries: int = 10
    ) -> Tuple[List[str], List[str]]:
        """
        분류된 태그들을 바탕으로 SFW 및 HIDDEN 검색어 리스트를 각각 10개까지 생성합니다.
        """
        # --- HIDDEN 쿼리 생성 (19금 포함, 5~10개) ---
        search_hidden_queries = []
        combined_hidden = list(secret_picks[:2]) # 전체 최상위 찐 취향은 2개만 할당하여 공간 확보
        
        # 1. 19금/민감한 키워드(explicit) 및 잠재적(implicit) 키워드를 우선순위로 활용
        all_hidden_tags = list(implicit_hidden_tags.items()) + list(explicit_hidden_tags.items())
        if all_hidden_tags:
            sorted_hidden = sorted(all_hidden_tags, key=lambda x: x[1], reverse=True)
            for tag, score in sorted_hidden:
                if tag not in combined_hidden:
                    combined_hidden.append(tag)
                    
        # 2. 남은 secret_picks 채워넣기
        for tag in secret_picks[2:]:
            if tag not in combined_hidden:
                combined_hidden.append(tag)
        
        # 2. 숨겨진 태그가 부족할 경우, 일반 태그(SFW) 중에서 차출
        sorted_general = sorted(sfw_tags.items(), key=lambda x: x[1], reverse=True)
        for tag, score in sorted_general:
            if tag not in combined_hidden and len(combined_hidden) < num_queries:
                combined_hidden.append(tag)
        
        search_hidden_queries = list(dict.fromkeys(combined_hidden))[:num_queries]

        # --- SFW 쿼리 생성 (5~10개) ---
        search_sfw_queries = []
        for tag, score in sorted_general:
            if tag not in search_sfw_queries:
                search_sfw_queries.append(tag)
                
        search_sfw_queries = search_sfw_queries[:num_queries]

        # --- 폴백 안전장치 ---
        if not search_sfw_queries and not search_hidden_queries:
            search_sfw_queries = ["일상", "소통", "데일리"]

        return search_sfw_queries, search_hidden_queries

    # --- [사용 예시] ---
    if __name__ == '__main__':
        # 이전 단계에서 분류된 가상의 데이터와 라우팅 결과라고 가정합니다.
        sample_explicit_hidden = {"포르노": 5, "브라": 12}
        sample_implicit_hidden = {"섹시": 25, "직캠": 30, "요가": 15}
        sample_sfw_tags = {"게임": 20, "캠핑": 18}

        # --- 시나리오 1: HIDDEN 라우팅 ---
        print("===== 시나리오 1: HIDDEN 라우팅 =====")
        final_queries_1 = generate_final_queries(sample_explicit_hidden, sample_implicit_hidden, sample_sfw_tags, ["ITZY"])
        print(f"최종 검색어: {final_queries_1}\n")
        # 예상 출력: ['ITZY', 'ITZY 추천', '직캠 모델', '직캠 화보', '직캠']

        # --- 시나리오 2: SFW 라우팅 ---
        print("===== 시나리오 2: SFW 라우팅 =====")
        final_queries_2 = generate_final_queries(sample_explicit_hidden, sample_implicit_hidden, sample_sfw_tags)
        print(f"최종 검색어: {final_queries_2}\n")
        # 예상 출력: ['게임', '캠핑']

        # --- 시나리오 3: FALLBACK 라우팅 ---
        print("===== 시나리오 3: FALLBACK 라우팅 =====")
        final_queries_3 = generate_final_queries({}, {}, {})
        print(f"최종 검색어: {final_queries_3}\n")
        # 예상 출력: ['인기 있는 이미지', '추천 콘텐츠']
            
        # === [END_DYNAMIC_ROUTING_LOGIC] ===

    # --- [실제 실행 로직 및 기존 API 포맷에 맞춘 Return 매핑] ---
    explicit_hidden, implicit_hidden, sfw = preprocess_and_classify_tags(tag_scores)
    
    search_sfw_queries, search_hidden_queries = generate_final_queries(explicit_hidden, implicit_hidden, sfw, secret_picks)
    
    # 화면에 보여주기 위한 raw tags 정렬
    sorted_sfw = sorted(sfw.items(), key=lambda x: x[1], reverse=True)
    sorted_hidden = sorted(list(explicit_hidden.items()) + list(implicit_hidden.items()), key=lambda x: x[1], reverse=True)

    return {
        "raw_sfw_tags": [t[0] for t in sorted_sfw[:10]],
        "raw_hidden_tags": [t[0] for t in sorted_hidden[:10]],
        "search_sfw_queries": search_sfw_queries,
        "search_hidden_queries": search_hidden_queries,
        "tag_to_urls": tag_to_urls,
        "total_tags_found": len(tag_scores)
    }
