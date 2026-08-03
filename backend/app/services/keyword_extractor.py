import re
from typing import Dict, Any, List, Tuple

# 19금 및 선정적 단어 필터링 및 우회 사전 (Hidden Dictionary & Safe Mapping)
HIDDEN_MAPPING = {
    "야동": "야동",
    "포르노": "포르노",
    "섹스": "섹스",
    "19금": "19금",
    "노출": "노출",
    "섹시": "섹시",
    "가슴": "가슴",
    "엉덩이": "엉덩이",
    "av": "av",
    "오나홀": "오나홀",
    "자위": "자위",
    "은꼴": "은꼴",
    "야한": "야한",
    "porn": "porn",
    "sex": "sex",
    "nsfw": "nsfw",
    "nude": "nude",
    "그라비아": "그라비아",
    "gravure": "gravure",
    "코스프레": "코스프레",
    "cosplay": "cosplay",
    "수영복": "수영복",
    "맥심": "맥심",
    "란제리": "란제리",
    "속옷": "속옷"
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
    
    import time
    current_time = time.time()
    
    def process_posts(posts: List[Dict[str, Any]], action_type: str):
        for p in posts:
            ts = p.get('timestamp', 0)
            tags = p.get('hashtags', [])
            
            # Time Decay Weighting 복원
            time_weight = 1.0
            if ts > 0:
                days_ago = (current_time - ts) / (60 * 60 * 24)
                if days_ago <= 30:
                    time_weight = 3.0
                elif days_ago <= 180:
                    time_weight = 1.5
                elif days_ago >= 365:
                    time_weight = 0.2  # 1년 넘은 옛날 데이터는 대폭 축소
            
            tag_len = len(tags)
            for t in tags:
                if len(t) < 2:
                    continue
                tag_clean = t.lower()
                
                if tag_clean not in tag_stats:
                    tag_stats[tag_clean] = {'public': 0.0, 'private': 0.0, 'doc_count': 0, 'total_siblings': 0}
                
                tag_stats[tag_clean]['doc_count'] += 1
                tag_stats[tag_clean]['total_siblings'] += tag_len
                
                # Public: 좋아요, 스토리 / Private: 저장, 컬렉션
                if action_type in ['liked', 'story']:
                    tag_stats[tag_clean]['public'] += time_weight
                else:
                    tag_stats[tag_clean]['private'] += (time_weight * 3.0)  # 저장(Save) 기본 가중치
                
    process_posts(liked, 'liked')
    process_posts(saved, 'saved')
    process_posts(stories_viewed, 'story')
    process_posts(story_likes, 'story')

    try:
        collections = parser.parse_saved_collections()
        for col in collections:
            col_tags = col.get('hashtags', [])
            tag_len = len(col_tags)
            for t in col_tags:
                if len(t) < 2:
                    continue
                tag_clean = t.lower()
                if tag_clean not in tag_stats:
                    tag_stats[tag_clean] = {'public': 0.0, 'private': 0.0, 'doc_count': 0, 'total_siblings': 0}
                
                tag_stats[tag_clean]['doc_count'] += 1
                tag_stats[tag_clean]['total_siblings'] += tag_len
                tag_stats[tag_clean]['private'] += 5.0  # 컬렉션은 시간 정보가 없으므로 고정 가중치 5.0
    except Exception as e:
        print(f"Collection parse error: {e}")

    # === [다층적 상호작용 기반 '찐 취향(True Affinity)' 산출] ===
    # 하드코딩된 STOP_WORDS 대신 TF-IDF와 동시 출현(Sibling) 맥락을 활용하여 범용 태그를 수학적으로 필터링합니다.
    
    total_posts = len(liked) + len(saved) + len(stories_viewed) + len(story_likes)
    if total_posts == 0:
        total_posts = 1
        
    import statistics
    import math

    private_scores = []
    tag_scores = {}  # SFW(대중적 취향) 정렬을 위한 최종 볼륨 저장용
    
    for tag, stats in tag_stats.items():
        doc_count = stats.get('doc_count', 1)
        # IDF (Inverse Document Frequency): 태그가 여러 게시물에 너무 널리(범용적으로) 쓰일수록 가중치 감소
        idf = math.log10((total_posts + 1) / doc_count)
        
        # 기본 점수에 IDF를 곱하여 최종 TF-IDF 점수 도출
        tf_idf_public = stats['public'] * idf
        tf_idf_private = stats['private'] * idf
        
        # Sibling Penalty: 한 게시물에 해시태그가 너무 많으면(평균 15개 이상) 어뷰징/범용 태그일 확률이 높음
        avg_siblings = stats.get('total_siblings', 0) / doc_count
        sibling_penalty = 1.0
        if avg_siblings > 15:
            sibling_penalty = 15 / avg_siblings
            
        final_public = tf_idf_public * sibling_penalty
        final_private = tf_idf_private * sibling_penalty
        
        # 내부 구조 갱신
        stats['public'] = final_public
        stats['private'] = final_private
        
        total = final_public + final_private
        tag_scores[tag] = total
        
        if final_private > 0:
            private_scores.append(final_private)
            
    median_private = statistics.median(private_scores) if private_scores else 0

    # 2. SFW(대중적 취향) Top 10 추출
    sorted_by_total = sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)
    top_sfw = [t[0] for t in sorted_by_total[:15]]

    # 3. Mathematical Hidden (수학적 은밀한 취향) 도출
    hidden_candidates = []
    for tag, stats in tag_stats.items():
        # Top 5 SFW(완전 대중적인 메인 취향)이면 제외
        if tag in top_sfw[:5]:
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
    
    # 19금은 아니지만 다소 매운맛(노출 등)을 띠는 키워드 유지. 
    # (애니메이션, 게임 등 건전한 서브컬처 키워드는 사전에서 삭제하여 오직 수학적 계산에 맡김)
    IMPLICIT_HIDDEN_KEYWORDS = {
        "반캠", "직캠", "섹시", "요가", "비키니", "룩북", "화보", "바디프로필", "레이싱모델", "피팅모델", "풀빌라"
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


    def generate_final_queries(
        explicit_hidden_tags: Dict[str, float],
        implicit_hidden_tags: Dict[str, float],
        sfw_tags: Dict[str, float],
        secret_picks: List[str] = [],
        num_queries: int = 5
    ) -> Tuple[List[str], List[str]]:
        """
        분류된 태그들을 바탕으로 SFW 및 HIDDEN 검색어 리스트를 각각 5개까지 생성합니다.
        """
        # --- SFW 쿼리 생성 (최대 5개) ---
        search_sfw_queries = []
        sorted_general = sorted(sfw_tags.items(), key=lambda x: x[1], reverse=True)
        for tag, score in sorted_general:
            if tag not in search_sfw_queries:
                search_sfw_queries.append(tag)
                
        search_sfw_queries = search_sfw_queries[:num_queries]

        # --- HIDDEN 쿼리 생성 (최대 5개, SFW와 유사도 차단) ---
        search_hidden_queries = []
        combined_hidden = list(secret_picks[:3]) 
        
        all_hidden_tags = list(implicit_hidden_tags.items()) + list(explicit_hidden_tags.items())
        if all_hidden_tags:
            sorted_hidden = sorted(all_hidden_tags, key=lambda x: x[1], reverse=True)
            for tag, score in sorted_hidden:
                # 점수가 1 이하인 노이즈 태그로 억지로 5개를 채우지 않도록 방지
                if score > 1 and tag not in combined_hidden:
                    combined_hidden.append(tag)
                    
        for tag in secret_picks[3:]:
            if tag not in combined_hidden:
                combined_hidden.append(tag)
        
        # 중복/유사 태그 방지 로직 (SFW와의 유사도 차단)
        for tag in combined_hidden:
            is_overlap = False
            for sfw_tag in search_sfw_queries:
                if is_similar(tag, sfw_tag):
                    is_overlap = True
                    break
            
            # 카테고리 내에서 이미 추가된 태그들과도 유사하면 제외
            for added_tag in search_hidden_queries:
                if is_similar(tag, added_tag):
                    is_overlap = True
                    break
                    
            if not is_overlap and len(search_hidden_queries) < num_queries:
                search_hidden_queries.append(tag)
                
        return search_sfw_queries, search_hidden_queries


    def is_similar(a: str, b: str) -> bool:
        a_low = a.lower().replace(" ", "")
        b_low = b.lower().replace(" ", "")
        if a_low in b_low or b_low in a_low:
            return True
        import difflib
        return difflib.SequenceMatcher(None, a_low, b_low).ratio() >= 0.7

    def filter_similar_tags(tags_list, compare_against_lists=[], max_len=5):
        filtered = []
        for tag in tags_list:
            is_overlap = False
            for compare_list in compare_against_lists:
                for c_tag in compare_list:
                    if is_similar(tag, c_tag):
                        is_overlap = True
                        break
                if is_overlap: break
            
            for f_tag in filtered:
                if is_similar(tag, f_tag):
                    is_overlap = True
                    break
                    
            if not is_overlap and len(filtered) < max_len:
                filtered.append(tag)
        return filtered

    # --- [실제 실행 로직 및 기존 API 포맷에 맞춘 Return 매핑] ---
    explicit_hidden, implicit_hidden, sfw = preprocess_and_classify_tags(tag_scores)
    
    search_sfw_queries, search_hidden_queries = generate_final_queries(explicit_hidden, implicit_hidden, sfw, secret_picks)
    
    # 화면에 보여주기 위한 raw tags 정렬 (중복 방지 필터링)
    raw_sfw_tags = filter_similar_tags([t[0] for t in sorted(sfw.items(), key=lambda x: x[1], reverse=True)], max_len=5)
    
    # Spicy Mode를 위한 찐 매운맛 키워드: 하드코딩 19금 키워드 + 수학적 극단치(Spicy Picks)
    explicit_tags = [t[0] for t in sorted(explicit_hidden.items(), key=lambda x: x[1], reverse=True)]
    spicy_picks = [t[0] for t in sorted_by_ratio[:10]] # 극단적 Private Ratio
    raw_spicy_candidates = list(dict.fromkeys(explicit_tags + spicy_picks))
    
    raw_spicy_tags = filter_similar_tags(raw_spicy_candidates, compare_against_lists=[search_sfw_queries], max_len=5)
    return {
        "raw_sfw_tags": raw_sfw_tags,
        "raw_hidden_tags": raw_spicy_tags,
        "search_sfw_queries": search_sfw_queries,
        "search_hidden_queries": search_hidden_queries,
        "total_tags_found": len(tag_scores)
    }
