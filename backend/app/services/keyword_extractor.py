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

    # === [START_DYNAMIC_ROUTING_LOGIC] ===
    # [작성 조건 및 가이드라인]
    # 1. 카테고리 사전 정의: 애니메이션, 게임, 아이돌 등 특정 서브컬처 카테고리 키워드들을 정의하세요.
    # 2. 가중치 점수 합산: tag_scores를 순회하면서, 어떤 카테고리의 점수(Affinity Score)가 가장 높은지 계산하세요.
    # 3. 임계값(Threshold) 판별: 1위 카테고리의 점수가 일정 기준치를 넘으면, 해당 취향에 맞춘 특화된 검색 쿼리 리스트를 반환하도록 if/elif 라우팅 로직을 만드세요.
    # 4. 폴백(Fallback) 및 안전성 유지: 특화 취향이 아니면 기본 sfw_tags를 사용하게 하고, 민감한(19금) 단어는 반드시 기존의 get_safe_tag()를 타서 건전한 단어로 우회되도록 방어 코드를 남겨두세요. 직접적인 19금 검색이 이루어지지 않도록 주의해야 합니다.

   # --- [데이터 전처리 및 분류 파트] ---

    STOP_WORDS = {"일상", "소통", "맞팔", "선팔", "좋아요반사", "f4f", "ootd", "좋아요", "팔로우"}
    # 기존 파일 최상단에 있는 HIDDEN_MAPPING 키워드들을 명시적 숨겨진(Hidden) 키워드로 활용합니다.
    POWERFUL_ADULT_QUERIES = [
    # 한국어
    "야한 동영상", "성인 콘텐츠", "야동", "에로틱 영상", "섹시한 영상",
    "노브라 노팬티", "망사 의상", "섹시 브라", "섹시 팬티", "예쁜 엉덩이",
    "레즈비언 영상", "게이 콘텐츠", "BDSM 콘텐츠",
    # 영어
    "erotic video", "adult video", "adult movie", "sex scene", "porn video",
    "lingerie model", "sexy body", "lesbian scene", "gay content", "BDSM content"
]
    EXPLICIT_HIDDEN_KEYWORDS = set(HIDDEN_MAPPING.keys())
    IMPLICIT_HIDDEN_KEYWORDS = {"반캠", "직캠", "섹시", "요가", "비키니", "룩북", "화보", "바디프로필"}

    def classify_tag_type(tag: str) -> str:
        t = tag.lower()
        if any(bad in t for bad in EXPLICIT_HIDDEN_KEYWORDS):
            return "EXPLICIT_HIDDEN"
        elif any(imp in t for imp in IMPLICIT_HIDDEN_KEYWORDS):
            return "IMPLICIT_HIDDEN"
        else:
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
        route: str,
        explicit_hidden_tags: Dict[str, int],
        implicit_hidden_tags: Dict[str, int],
        sfw_tags: Dict[str, int],
        num_queries: int = 5
    ) -> List[str]:
        """
        라우팅 결과와 분류된 태그들을 바탕으로, 최종적인 검색어 리스트를 생성합니다.
        HIDDEN 라우팅 시, 강력한 19금 검색어를 우선적으로 사용합니다.
        """
        final_queries = []
        if route == "HIDDEN":
            # '숨겨진 취향(Hidden)' 콘텐츠 파이프라인
            print("라우팅: 숨겨진 취향(Hidden) 콘텐츠 파이프라인을 탑니다.")
            
            # 1. 사용자의 태그에서 직접 추출한 잠재적 키워드 (예: '직캠', '섹시')
            sorted_implicit = sorted(implicit_hidden_tags.items(), key=lambda x: x[1], reverse=True)
            user_implicit_queries = [tag for tag, score in sorted_implicit]

            # 2. 강력한 19금 검색어 리스트와 사용자 키워드를 조합
            # 사용자의 취향을 반영하면서도, 검색 성공률을 높이기 위해 강력한 검색어를 우선적으로 배치
            combined_queries = POWERFUL_ADULT_QUERIES + user_implicit_queries
            
            # 3. 중복 제거 및 상위 num_queries개 선택
            final_queries = list(dict.fromkeys(combined_queries))[:num_queries]

        elif route == "SFW":
            # '맞춤(SFW) 콘텐츠' 파이프라인 (기존 로직 유지)
            print("라우팅: 동적 토픽 파이프라인을 탑니다.")
            sorted_general = sorted(sfw_tags.items(), key=lambda x: x[1], reverse=True)
            if sorted_general:
                top_keywords = [tag for tag, score in sorted_general[:3]]
                dynamic_topic_query = " ".join(top_keywords)
                print(f"👉 발견된 유저만의 동적 토픽: [{dynamic_topic_query}]")
                final_queries = [dynamic_topic_query] + [tag for tag, score in sorted_general[:num_queries-1]]
                final_queries = list(dict.fromkeys(final_queries))[:num_queries]
            else:
                final_queries = []

        else: # "FALLBACK"
            # '폴백' 파이프라인 (기존 로직 유지)
            print("라우팅: 폴백 파이프라인을 탑니다. 기본 검색어를 사용합니다.")
            final_queries = ["인기 있는 이미지", "추천 콘텐츠"]

        # 최종 안전장치 (기존 로직 유지)
        if not final_queries:
            print("경고: 생성된 검색어가 없습니다. 기본 검색어로 폴백합니다.")
            return ["인기 있는 이미지"]

        return final_queries

    # --- [사용 예시] ---
    if __name__ == '__main__':
        # 이전 단계에서 분류된 가상의 데이터와 라우팅 결과라고 가정합니다.
        sample_explicit_hidden = {"포르노": 5, "브라": 12}
        sample_implicit_hidden = {"섹시": 25, "직캠": 30, "요가": 15}
        sample_sfw_tags = {"게임": 20, "캠핑": 18}

        # --- 시나리오 1: HIDDEN 라우팅 ---
        print("===== 시나리오 1: HIDDEN 라우팅 =====")
        route_1 = "HIDDEN"
        final_queries_1 = generate_final_queries(route_1, sample_explicit_hidden, sample_implicit_hidden, sample_sfw_tags)
        print(f"최종 검색어: {final_queries_1}\n")
        # 예상 출력: ['직캠', '섹시', '요가', '야한 동영상', '섹시 브라']

        # --- 시나리오 2: SFW 라우팅 ---
        print("===== 시나리오 2: SFW 라우팅 =====")
        route_2 = "SFW"
        final_queries_2 = generate_final_queries(route_2, sample_explicit_hidden, sample_implicit_hidden, sample_sfw_tags)
        print(f"최종 검색어: {final_queries_2}\n")
        # 예상 출력: ['게임', '캠핑']

        # --- 시나리오 3: FALLBACK 라우팅 ---
        print("===== 시나리오 3: FALLBACK 라우팅 =====")
        route_3 = "FALLBACK"
        final_queries_3 = generate_final_queries(route_3, {}, {}, {})
        print(f"최종 검색어: {final_queries_3}\n")
        # 예상 출력: ['인기 있는 이미지', '추천 콘텐츠']
            
        # === [END_DYNAMIC_ROUTING_LOGIC] ===

    # --- [실제 실행 로직 및 기존 API 포맷에 맞춘 Return 매핑] ---
    explicit_hidden, implicit_hidden, sfw = preprocess_and_classify_tags(tag_scores)
    affinity_scores = calculate_affinity_scores(explicit_hidden, implicit_hidden, sfw)
    route = route_by_affinity(affinity_scores)
    
    final_queries = generate_final_queries(route, explicit_hidden, implicit_hidden, sfw)
    
    # 프론트엔드 호환성을 위해 SFW와 Hidden 쿼리를 분리
    search_sfw_queries = []
    search_hidden_queries = []
    if route == "HIDDEN":
        search_hidden_queries = final_queries
    else:
        search_sfw_queries = final_queries

    # 화면에 보여주기 위한 raw tags 정렬
    sorted_sfw = sorted(sfw.items(), key=lambda x: x[1], reverse=True)
    sorted_hidden = sorted(list(explicit_hidden.items()) + list(implicit_hidden.items()), key=lambda x: x[1], reverse=True)

    return {
        "raw_sfw_tags": [t[0] for t in sorted_sfw[:10]],
        "raw_hidden_tags": [t[0] for t in sorted_hidden[:10]],
        "search_sfw_queries": search_sfw_queries,
        "search_hidden_queries": search_hidden_queries,
        "total_tags_found": len(tag_scores)
    }
