# STUDY_NOTES.md — 발표 준비용 코드 해설

## ⚠️ 발표 전에 꼭 짚고 가야 할 오해 하나

**실제 코드는 DuckDuckGo를 호출하지 않습니다.**

`README.md`나 `docs/` 문서에는 "DuckDuckGo(ddgs)로 실시간 스크래핑한다"고 적혀 있지만, 실제로 배포되는 `backend/app/services/search_service.py`를 열어보면 `ddgs`/`duckduckgo` 관련 코드가 전혀 없습니다. 이 파일이 실제로 하는 일은:

```python
all_recommendations.append({
    "title": f"#{safe_kw} 연관 인기 게시물 둘러보기",
    "url": f"https://www.instagram.com/explore/tags/{safe_kw}/",
    ...
})
```

즉 **분석된 키워드를 가지고 `instagram.com/explore/tags/<키워드>` 링크를 그냥 직접 만들어주는 것**뿐입니다. `docs/오류.md`를 보면 초반에는 실제로 DuckDuckGo 검색 API를 썼다가, 민감한 키워드가 검색엔진 필터에 걸려 빈 결과(`[]`)만 돌아오는 문제를 겪었고, 그 우회용으로 "안전 치환 사전(Safe Mapping)"을 만든 기록이 남아있습니다. 지금 코드에는 그 사전(`HIDDEN_MAPPING`)은 남아있지만, **검색 자체를 걷어내고 인스타그램 탐색 링크 생성으로 대체된 상태**로 보입니다.

→ 발표에서는 "DuckDuckGo API를 호출해서 추천한다"라고 하면 틀린 설명이 됩니다. **"사용자의 상호작용 데이터를 통계적으로 분석해 취향 키워드를 뽑고, 그 키워드로 인스타그램 탐색(explore) 링크를 생성해 추천한다"**가 정확한 설명입니다.

---

## 1. 폴더/파일 구조 한 줄 요약

### 루트
| 파일 | 역할 |
|---|---|
| `package.json` | Vercel이 실행하는 빌드 스크립트만 정의 (`cd frontend && npm install && npm run build`) |
| `vercel.json` | `/api/*` 요청은 `api/index.py`로, 나머지는 프론트 SPA(`frontend/dist`)로 라우팅. Python 함수 최대 실행시간 60초 설정 |
| `requirements.txt` | `backend/requirements.txt`와 동일 내용의 사본 (Vercel이 루트에서 찾기 때문에 복사해둔 것으로 보임) |
| `api/index.py` | Vercel 서버리스 함수 진입점. `backend/`를 `sys.path`에 넣고 FastAPI 앱을 import만 함 |

### `backend/app/` (FastAPI 백엔드)
| 파일 | 역할 |
|---|---|
| `main.py` | FastAPI 앱 생성, CORS 전체 허용(`allow_origins=["*"]`), `/api` 프리픽스로 라우터 연결 |
| `api/routes.py` | 실제 엔드포인트 4개(`/upload-chunk`, `/upload-payload`, `/upload`, `/results/{job_id}`) + zip에서 필요한 파일만 뽑아내는 함수 |
| `services/parser.py` | 인스타그램 export json → 좋아요/저장/스토리 리스트로 변환. 디스크용(`InstaParser`)과 메모리 dict용(`InstaMemoryParser`) 두 버전 |
| `services/keyword_extractor.py` | **이 프로젝트의 핵심 알고리즘.** 해시태그 점수화 + SFW/HIDDEN/SPICY 분류 |
| `services/search_service.py` | 키워드 → `instagram.com/explore/tags/...` 링크 생성 (DuckDuckGo 아님, 위 경고 참고) |
| `services/db_service.py` | 분석 결과를 Supabase에 저장/조회, Supabase 설정이 없으면 메모리로 자동 대체(fallback) |
| `services/one_pick.py` | 계정별 상호작용 순위를 매기는 로직인데, **어느 라우터에서도 호출되지 않는 죽은 코드** |
| `utils/cleanup.py` | `job_id`별 분석 결과를 메모리 딕셔너리(`JOBS_STORE`)에 저장, 1시간(TTL) 지나면 삭제 |
| `utils/encoding.py` | 인스타 export json의 한글 깨짐(latin1↔utf8) 복구 함수 |
| `test_run.py` | 로컬 실제 데이터셋 폴더를 넣고 파서+키워드추출을 수동으로 돌려보는 스크립트 (자동 테스트 아님) |

### `frontend/src/` (React + Vite)
| 파일 | 역할 |
|---|---|
| `main.jsx` | React 진입점, `App`을 DOM에 마운트 |
| `App.jsx` | 라우터 정의 (`/`, `/loading`, `/result`, `/secret`) + Vercel Analytics/SpeedInsights 삽입 |
| `pages/UploadPage.jsx` | zip 파일 선택 UI. 여기서는 업로드를 하지 않고, 선택한 File 객체를 `/loading`으로 그대로 넘김 |
| `pages/LoadingPage.jsx` | **실제 업로드 로직이 있는 곳.** 파일을 2MB 청크로 나눠 순차 전송 + 진행률 표시 + 완료 후 결과 폴링(polling) |
| `pages/ResultPage.jsx` | 일반(SFW) 추천 결과 화면. 컨페티 애니메이션, "진짜 숨겨진 취향 보기" 버튼으로 `/secret` 이동 |
| `pages/SecretPickPage.jsx` | Secret(hidden) / Spicy 두 모드를 토글로 전환해 보여주는 화면 |
| `components/Header.jsx` | 상단 로고/배지 (정적 UI) |
| `components/Recommendations.jsx` | 추천 리스트 카드를 렌더링하는 공통 컴포넌트 (SFW/Hidden/Spicy 세 화면에서 재사용) |
| `components/TopPickCard.jsx`, `RunnerUpList.jsx` | `one_pick` 기능(계정 랭킹)용 컴포넌트인데, **어느 페이지에서도 import되지 않는 죽은 코드** |
| `App.css` / `index.css` | 전역 스타일 (글래스모피즘 + 네온 느낌, CSS 프레임워크 없이 직접 작성) |
| `vite.config.js` | Vite + React 플러그인 설정만 있음 |
| `.oxlintrc.json` | lint 규칙 정의는 있지만 `package.json`에 `lint` 스크립트로 연결되어 있지 않음 (사용 안 됨) |

---

## 2. 전체 데이터 흐름 (텍스트 다이어그램)

```
[1] 사용자가 인스타그램 "내 정보 다운로드"로 받은 ZIP을 UploadPage에서 선택
        │  (여기서는 파일 검증만 하고, 실제 전송은 안 함)
        ▼
[2] LoadingPage.jsx
    - 파일을 2MB 단위 청크로 분할
    - 청크마다 POST /api/upload-chunk (upload_id, chunk_index, total_chunks 포함)
    - 실패하면 최대 3회까지 재시도(backoff)
        ▼
[3] routes.py: upload_chunk()
    - 청크들을 임시 디렉터리에 chunk_0, chunk_1... 로 저장
    - 마지막 청크가 도착하면 전부 이어붙여 merged_upload.zip 생성
        ▼
[4] extract_and_parse_zip()
    - zip 전체를 풀지 않고, 필요한 JSON 5개만 골라서 디스크에 복사
      (liked_posts.json, saved_posts.json, stories_viewed.json,
       story_likes.json, saved_collections.json)
        ▼
[5] parser.py: InstaParser
    - 5개 JSON을 읽어서 각 게시물/스토리에서
      timestamp, hashtags, caption, owner를 뽑아 표준화된 리스트로 변환
    - 한글 깨짐은 encoding.py의 decode_insta_text()로 복구
        ▼
[6] keyword_extractor.py: extract_taste_keywords()
    - 좋아요=public, 저장=private로 나눠서 해시태그별 가중치 누적
      (최근 게시물일수록 가중치 ↑, 저장은 좋아요보다 가중치 ↑)
    - TF-IDF로 "너무 흔한 태그"는 점수 깎기
    - 게시물 하나에 태그가 너무 많으면(15개 초과) 어뷰징으로 보고 감점
    - 같은 게시물에 같이 등장한 태그끼리 co-occurrence(연관성) 기록
    - 사전 기반으로 SFW / IMPLICIT_HIDDEN / EXPLICIT_HIDDEN 3단계로 분류
    - 대표 카테고리(main_category) 선정 후, 연관 태그를 co-occurrence로 채워
      최종 검색 키워드 5개씩(SFW/Hidden/Spicy) 생성
        ▼
[7] search_service.py: get_recommendations_for_keywords()
    - (DuckDuckGo 호출 없음!) 각 키워드를 그대로
      https://www.instagram.com/explore/tags/<키워드>/ 링크로 변환
        ▼
[8] db_service.py: save_analysis_result()
    - 분석 결과 전체를 job_id로 Supabase에 저장 (설정 없으면 메모리 JOBS_STORE에만 저장)
        ▼
[9] LoadingPage.jsx가 1.5초마다 GET /api/results/{job_id} 폴링
    - 결과가 준비되면 /result 페이지로 이동하며 데이터를 넘김
        ▼
[10] ResultPage.jsx / SecretPickPage.jsx
    - main_category, search_sfw_queries, sfw_recommendations 등을 화면에 렌더링
    - "진짜 숨겨진 취향 보기" 클릭 시 hidden/spicy 데이터를 SecretPickPage로 전달
```

---

## 3. 가상 예시로 전체 흐름 따라가기

**가상 입력**: 사용자가 최근 30일 안에 헬스 관련 게시물에 **좋아요 20개**(해시태그: `#헬스 #다이어트 #홈트` 3개씩 동일하게), 요리 관련 게시물을 **저장 5번**(해시태그: `#집밥 #레시피 #집밥스타그램 #요리` 4개씩 동일하게) 했다고 가정합니다. 스토리 시청/반응은 없음.

### 3-1. 파싱 결과 (`parser.py`)
```
liked  = [ {timestamp: 최근, hashtags: [헬스,다이어트,홈트]} ] x 20개
saved  = [ {timestamp: 최근, hashtags: [집밥,레시피,집밥스타그램,요리]} ] x 5개
stories_viewed = [], story_likes = []
total_posts = 20 + 5 = 25
```

### 3-2. 태그별 가중치 집계 (`extract_taste_keywords`의 `process_posts`)
"최근 30일 이내"라 `time_weight = 3.0`이 전부 적용됩니다. 좋아요는 `public`에, 저장은 `public`이 아니라 `private`에 **`time_weight × 3.0`**(저장 기본 가중치)으로 쌓입니다.

| 태그 | doc_count | public | private | weighted_count | 평균 형제 태그 수 |
|---|---|---|---|---|---|
| 헬스/다이어트/홈트 | 20 | 20×3.0=**60** | 0 | 60 | 3 (패널티 없음) |
| 집밥/레시피/집밥스타그램/요리 | 5 | 0 | 5×(3.0×3.0)=**45** | 15 | 4 (패널티 없음) |

동시에 같은 게시물 안에서 나온 태그끼리 co-occurrence 점수도 쌓입니다. 예: `헬스`-`다이어트`는 20번 같이 나왔으니 `co_occurrences[헬스][다이어트] += 3.0` 이 20번 반복되어 **60**이 됩니다. (집밥 계열도 서로 15점씩)

### 3-3. TF-IDF + 패널티 적용
`idf = log10((25+1) / doc_count)`
- 헬스 계열: `idf = log10(26/20) ≈ 0.114` → `final_public = 60 × 0.114 ≈ 6.84`
- 집밥 계열: `idf = log10(26/5) ≈ 0.716` → `final_private = 45 × 0.716 ≈ 32.2`

→ **저장(5회)이 좋아요(20회)보다 최종 점수가 더 높게 나옵니다.** ("저장"에 가중치 3배를 주고, doc_count가 적을수록 idf가 커지기 때문에 소수의 저장 행동이 다수의 좋아요보다 "진짜 취향"으로 더 강하게 반영되는 구조입니다.)

`median_private`(private 점수의 중앙값)은 32.2(집밥 계열 4개가 전부 같은 값)로 계산됩니다.

### 3-4. Hidden 후보 판별
상위 SFW 5개(`집밥, 레시피, 집밥스타그램, 요리, 헬스`)에 못 든 태그(`다이어트`, `홈트`) 중에서 `private ≥ median_private`인 것만 "비밀 취향 후보"가 되는데, 이 예시에서는 `다이어트`/`홈트`의 private가 0이라 조건을 못 넘습니다. → **hidden 후보 없음.**

### 3-5. 사전 매칭 (`HIDDEN_MAPPING` / `IMPLICIT_HIDDEN_KEYWORDS`)
7개 태그 전부 성인/민감 키워드 사전에 걸리지 않으므로 전부 `SFW`로 분류됩니다. → `explicit_hidden = {}`, `implicit_hidden = {}`.

### 3-6. 대표 카테고리 & 연관 키워드 뽑기
`weighted_count` 기준 1등은 `헬스`(60) → `main_category = "헬스"`.
`co_occurrences["헬스"]`에는 `{다이어트: 60, 홈트: 60}`이 있으므로 이 둘을 먼저 채우고, 5칸이 다 안 차면 나머지 SFW 태그(집밥, 레시피, 집밥스타그램, 요리)를 순서대로 채웁니다.

`filter_similar_tags()`가 **비슷한 문자열은 중복 제거**합니다(`"집밥"`이 이미 있으면 `"집밥스타그램"`은 부분 문자열이라 걸러짐). 그리고 **최대 5개**까지만 담습니다.

```
[헬스, 다이어트, 홈트, 집밥, 레시피]  ← 5칸이 다 차서
집밥스타그램, 요리는 여기서 탈락!
```

→ `search_sfw_queries = ["헬스", "다이어트", "홈트", "집밥", "레시피"]`

**여기서 보여줄 수 있는 재미있는 포인트**: 요리 관련 게시물을 저장까지 했는데도, "5개 캡 + 유사 태그 제거" 로직 때문에 `요리`라는 원래 단어는 최종 추천에서 빠지고 `집밥`, `레시피`만 살아남습니다. → 알고리즘의 한계/트레이드오프를 보여주는 좋은 예시입니다.

### 3-7. Hidden / Spicy 파이프라인
3-4에서 hidden 후보가 없었으므로:
```
hidden_category = "비밀의 방" (기본값)
search_hidden_queries = []
spicy_category = "은밀한 욕망" (기본값)
raw_hidden_tags = []
```

### 3-8. 추천 링크 생성 (`search_service.py`)
```python
get_recommendations_for_keywords(["헬스","다이어트","홈트","집밥","레시피"])
```
→ 5개의 `{"title": "#헬스 연관 인기 게시물 둘러보기", "url": "https://www.instagram.com/explore/tags/헬스/", ...}` 형태 객체 생성. hidden/spicy는 입력 리스트가 비어있으니 결과도 `[]`.

### 3-9. 최종 화면
- `ResultPage`: **"#헬스 마니아"** 타이틀 + 키워드 뱃지 `#헬스 #다이어트 #홈트 #집밥 #레시피` + 인스타 탐색 링크 5개 카드
- `SecretPickPage`: hidden/spicy 둘 다 비어있으므로 **"특별한 취향 태그가 없습니다"**, **"이 취향과 관련된 콘텐츠를 충분히 찾지 못했습니다"** 메시지가 뜸 (정상적인 "숨길 게 없는" 사용자 케이스를 잘 처리하는 예)

> 참고: 실제 코드에서 같은 게시물 안의 태그들을 묶을 때 `list(set(...))`을 쓰기 때문에, 완전히 동점인 태그끼리의 순서는 Python 실행마다 살짝 달라질 수 있습니다(해시 기반). 이 예시는 이해를 돕기 위해 특정 순서를 가정한 것이고, 점수 자체(6.84, 32.2 등)와 "5칸 캡에 걸려 요리/집밥스타그램이 탈락한다"는 결론은 코드 로직상 항상 동일하게 성립합니다.

---

## 4. 핵심 로직 라인별 설명

### 4-1. `backend/app/utils/encoding.py` (가장 먼저 이해해야 하는 이유)
```python
def decode_insta_text(text: str) -> str:
    if not isinstance(text, str) or not text:
        return ""
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text
```
- 인스타그램이 export하는 JSON은 한글(UTF-8 바이트)을 **Latin-1로 잘못 디코딩한 문자열**로 저장해 놓습니다. 그래서 `"í•¬ìŠ¤"`처럼 깨진 문자열이 들어있습니다.
- 이 함수는 그 반대로 **다시 UTF-8 바이트로 인코딩(`encode('latin-1')`)한 다음 UTF-8로 디코딩**해서 원래 한글을 복원합니다. 이게 실패하면(진짜 다른 인코딩 문제) 원본 그대로 반환합니다.
- `decode_obj()`는 dict/list를 재귀적으로 순회하며 문자열 값마다 위 함수를 적용합니다. **모든 인스타 JSON 파싱은 이 함수를 거치지 않으면 한글이 깨진 채로 나옵니다.**

### 4-2. `backend/app/services/parser.py` — `InstaParser._extract_posts_list`
- 인스타 export json 구조는 고정된 필드가 아니라 `label_values` 리스트 안에 `label`/`value`/`title`/`dict`가 중첩되는, 매우 범용적이고 깊이가 들쑥날쑥한 구조입니다.
- `for lv in label_values:` 로 각 항목을 보면서:
  - `label == 'URL'` → 게시물 URL
  - `label == '캡션'` → 캡션 텍스트
  - `title == '해시태그'` → 그 안의 `dict` → `dict`를 또 파고들어가서 `label == '이름'`인 값을 해시태그로 수집 (해시태그 하나가 이렇게 3중 중첩으로 들어있음)
  - `label`이나 `title`에 "이름/소유자/작성자"가 들어있으면 그 안에서 게시물 작성자(owner)를 뽑음
- `if caption: found_tags = re.findall(r'#(\w+)', caption)` — 캡션 텍스트 안에 `#해시태그` 형태로 직접 적힌 것도 정규식으로 한 번 더 긁어옵니다 (label_values 안의 해시태그 필드와는 별도 경로).
- `hashtags = set(...)` 로 중복 제거 후 `list()`로 변환해서 반환합니다.
- `InstaMemoryParser`는 디스크 대신 업로드된 dict(`files_dict`)에서 파일명을 대소문자 무시 + 뒷부분 일치로 찾아서 읽는 것만 다르고, 나머지 파싱 로직은 부모 클래스(`InstaParser`)를 그대로 상속해서 씁니다.

### 4-3. `backend/app/services/keyword_extractor.py` — 이 프로젝트의 알고리즘 (가장 중요)

**(1) 시간 가중치 (Time Decay)**
```python
if days_ago <= 30: time_weight = 3.0
elif days_ago <= 180: time_weight = 1.5
elif days_ago >= 365: time_weight = 0.2
```
최근 활동일수록 "지금 취향"을 더 잘 대표한다고 보고 가중치를 높입니다. (30~180일/180~365일 사이 구간은 코드에 명시적으로 안 정의돼서 기본값 1.0이 적용됨 — 이런 빈틈이 있다는 것도 발표에서 언급할 수 있는 포인트입니다.)

**(2) public / private 분리**
```python
if action_type in ['liked', 'story']:
    tag_stats[tag_clean]['public'] += time_weight
else:  # saved
    tag_stats[tag_clean]['private'] += (time_weight * 3.0)
```
좋아요/스토리는 "남들도 보는 공개적 반응"(public), 저장은 "혼자만 보는 사적인 반응"(private)으로 분리하고, 저장에는 3배 가중치를 줍니다. → **"저장"이 "진짜 취향"의 강한 신호**라는 이 프로젝트의 핵심 가정입니다.

**(3) co-occurrence 기록**
```python
unique_valid = list(set(valid_tags))
for i in range(len(unique_valid)):
    for j in range(i+1, len(unique_valid)):
        ...
        co_occurrences[t1][t2] = co_occurrences[t1].get(t2, 0) + time_weight
```
한 게시물에 같이 등장한 태그 쌍마다 점수를 쌓아서, 나중에 "이 태그와 자주 같이 나오는 다른 태그"를 찾을 수 있는 그래프를 만듭니다.

**(4) TF-IDF**
```python
idf = math.log10((total_posts + 1) / doc_count)
tf_idf_public = stats['public'] * idf
tf_idf_private = stats['private'] * idf
```
검색엔진에서 쓰는 TF-IDF 아이디어를 그대로 가져온 것입니다. `doc_count`(이 태그가 등장한 게시물 수)가 클수록(=너무 흔한 태그일수록) `idf`가 작아져서 점수가 깎입니다. 즉 "모든 게시물에 다 붙어있는 뻔한 태그"보다 "가끔이지만 확실하게 등장하는 태그"를 더 취향으로 인정합니다.

**(5) Sibling penalty (어뷰징 방지)**
```python
avg_siblings = stats.get('total_siblings', 0) / doc_count
if avg_siblings > 15:
    sibling_penalty = 15 / avg_siblings
```
게시물 하나에 해시태그를 15개 넘게 도배하는 경우(광고/스팸성 게시물 특징) 그 태그들의 점수를 깎습니다. 하드코딩된 불용어 리스트 대신, **통계적으로 "너무 태그가 많은 게시물"을 걸러내는 방식**을 택한 부분입니다.

**(6) Hidden 후보 산출**
```python
if tag in top_sfw[:5]:
    continue
if stats['private'] >= median_private:
    ratio = stats['private'] / (stats['public'] + 1.0)
    hidden_candidates.append((tag, ratio))
```
가장 대중적인 취향(top 5)은 제외하고, 그 사용자의 private 점수 중앙값 이상인 태그들만 후보로 삼습니다. 그리고 `private/(public+1)` 비율이 높은(=거의 저장으로만 반응한) 순서로 정렬해서 "은밀한 서브 취향"을 뽑습니다.

**(7) 사전 기반 분류 (`classify_tag_type`)**
`HIDDEN_MAPPING`(19금/노출 등 명시적 단어)와 `IMPLICIT_HIDDEN_KEYWORDS`(코스프레, 비키니 등 약한 성인성 단어) 두 사전에 태그가 포함되는지 검사합니다. 재미있는 부분은 **오탐(false positive) 방지 예외 처리**들입니다. 예:
```python
if bad == '가슴' and any(x in t for x in ['닭가슴살', '가슴뛰는', ...]): continue
if bad == '자위' and '자위대' in t: continue
if bad == '엉덩이' and '엉덩이탐정' in t: continue
```
`"자위대"`(일본 자위대)나 `"엉덩이탐정"`(애니메이션) 같은 정상 단어가 민감 키워드로 잘못 분류되는 것을 막기 위한 수동 예외 리스트입니다. → 실전 데이터를 돌려보면서 하나씩 발견해 추가한 흔적으로 보입니다.

**(8) `filter_similar_tags` — 문자열 유사도로 중복 제거**
```python
def is_similar(a, b):
    if a_low in b_low or b_low in a_low:
        return True
    return difflib.SequenceMatcher(None, a_low, b_low).ratio() >= 0.7
```
부분 문자열 포함관계이거나, `difflib`의 시퀀스 유사도가 0.7 이상이면 "같은 취향의 변형"으로 보고 최종 추천 리스트에서 하나만 남깁니다(예: `집밥`/`집밥스타그램`). 이 프로젝트에서 "유사도 계산"이라고 부를 수 있는 부분이 바로 여기입니다 — 임베딩 기반 의미 유사도가 아니라 **문자열 표층 유사도**입니다.

**(9) `get_related_tags_by_cooccurrence` — 연관 태그 추천**
대표 카테고리와 실제로 같은 게시물에 자주 같이 등장했던 태그들을(co_occurrences 그래프에서) 점수순으로 뽑아서, 완전히 무관한 태그가 추천에 섞이는 것을 방지합니다. 부족하면(4개 미만) 전체 순위표로 채우는 fallback이 있습니다.

### 4-4. `backend/app/api/routes.py` — 업로드 파이프라인
- `extract_and_parse_zip()`: `zip_ref.namelist()`로 zip 안의 전체 파일 목록을 가져온 뒤, 필요한 5개 파일 경로와 **대소문자 무시 + 뒤에서부터 일치**(`endswith`)로만 찾습니다. 인스타 export의 폴더 구조가 버전/언어별로 조금씩 다를 수 있어서 정확한 절대경로 대신 이런 유연한 매칭을 쓴 것으로 보입니다.
- `upload_chunk()`: `CHUNK_STORAGE` 딘셔너리(메모리)에 `upload_id`별로 받은 청크 인덱스를 `set()`으로 추적하다가, `len(received_chunks) == total_chunks`가 되면 그 순간 파일들을 순서대로 이어붙입니다. 이어붙인 뒤엔 즉시 `os.remove`/`shutil.rmtree`로 청크 원본과 zip을 지워서 디스크를 비웁니다 (Vercel의 500MB `/tmp` 제한 때문).
- 청크 업로드가 끝나면 그 요청 안에서 곧바로 파싱 → 키워드 추출 → 추천 생성까지 다 해버리고 `job_id`만 응답합니다. **비동기 작업 큐 같은 건 없고, 마지막 청크를 받은 그 HTTP 요청이 분석까지 통째로 처리**합니다.

### 4-5. `backend/app/services/search_service.py`
- `is_valid_instagram_url()`이라는, HTTP 요청을 보내 계정이 비공개/삭제 상태인지 확인하는 함수가 있지만 **어느 라우터에서도 호출되지 않습니다** (죽은 코드). 아마 one_pick 기능과 함께 만들었다가 안 쓰게 된 것으로 보입니다.
- `get_recommendations_for_keywords()`는 정말 짧습니다: 키워드마다 공백만 제거하고 그대로 URL에 꽂아넣는 문자열 포매팅이 전부입니다. 여기에 실제 "검색"이나 "스크래핑"은 없습니다 (문서 상단 경고 참고).

---

## 5. 기술 스택 선택 이유

| 선택 | 이유 (추정 근거: 코드/문서에서 드러나는 제약) | 대안이었을 것 |
|---|---|---|
| **Vercel Serverless (Python 함수 1개 + 정적 SPA)** | 백엔드/프론트를 별도 서버 없이 무료/저비용으로 배포. `vercel.json`에 함수 최대 60초, 기본 `/tmp` 500MB라는 제약이 명시되어 있고, 이 제약이 코드 전체(청크 업로드, 선택적 zip 추출)의 설계를 이끌었음 | 별도 VPS/EC2에 FastAPI 상시 구동 — 관리 비용과 서버비가 발생 |
| **FastAPI** | Python으로 빠르게 REST API를 짜기 좋고, `UploadFile`/`Form` 기반 멀티파트 업로드 지원이 내장돼 있어 zip/청크 업로드 구현이 짧아짐. 데이터 분석 로직(정규식, 통계)도 Python이 유리 | Flask(비동기 지원이 약함), Node/Express(파일 파싱 라이브러리 생태계가 Python보다 약함) |
| **인메모리 스트리밍 파싱 (Vector DB 미사용)** | `docs/오류.md`에 pgvector/FAISS를 쓰려다 메모리 폭발을 겪었다는 기록이 있음. 사용자 데이터를 임베딩해 유사도 검색을 하려면 무거운 벡터 인덱스가 필요한데, Serverless 환경의 메모리/시간 제약상 유지가 불가능해서 포기하고, 대신 "그때그때 압축 안 풀고 필요한 json만 읽어서 즉석 통계 분석" 방식으로 전환 | pgvector, FAISS, Pinecone 같은 임베딩 기반 추천 — 더 "의미적으로 정확한" 추천이 가능했겠지만 이 프로젝트의 서버리스/무료 티어 제약에는 안 맞음 |
| **TF-IDF + 통계 기반 키워드 분류 (ML 모델 미사용)** | 학습 데이터도, GPU도, 지연시간 여유도 없는 서버리스 환경에서 "적당히 설명 가능하고 즉시 계산 가능한" 방법이 필요했음. TF-IDF는 라이브러리 설치 없이 `math.log10` 몇 줄로 구현 가능하고, 결과를 "왜 이 태그가 뽑혔는지" 숫자로 설명하기도 쉬움 | 사전학습된 임베딩 모델로 해시태그 클러스터링 — 더 정교하지만 모델 로딩/추론 비용, 콜드스타트 문제 발생 |
| **DuckDuckGo 검색 → (실제로는) 직접 링크 생성으로 대체** | 원래는 실시간 트렌드를 가져오려고 검색엔진을 썼지만, 민감 키워드가 자꾸 차단당해서(`오류.md` 기록) 안정성을 위해 결국 "인스타그램 자체 탐색 URL을 그냥 만들어주는" 훨씬 단순하고 실패할 일이 없는 방식으로 대체된 것으로 보임 | 실제 스크래핑/공식 API 유지 — 더 "다양한" 추천이 가능하지만 차단·요금·안정성 리스크가 큼 |
| **Supabase (+ 메모리 fallback)** | Postgres를 직접 운영하지 않고도 관리형 DB를 무료 티어로 붙일 수 있고, `db_service.py`에서 보듯 연결 실패 시 자동으로 메모리 저장으로 넘어가게 만들어서, DB 설정 없이도(로컬 개발/데모) 앱이 죽지 않도록 방어함 | 자체 Postgres/MongoDB 운영 — 서버리스 환경엔 커넥션 관리가 더 번거로움 |
| **React + Vite (SPA) + react-router-dom v7** | 업로드→로딩→결과→비밀결과의 4단계 화면 전환이 명확한 SPA 라우팅으로 표현하기 쉬움. Vite는 CRA보다 훨씬 빠른 dev 서버/빌드 속도 제공 | Next.js(SSR) — 이 앱은 검색엔진 노출이 중요한 서비스가 아니라 순수 클라이언트 인터랙션 위주라 SSR의 이점이 크지 않음 |
| **클라이언트 청크 분할 업로드 (2MB)** | Vercel 서버리스 함수의 요청 바디/시간 제한 안에서 대용량(수백MB) zip을 안전하게 올리기 위한 선택. 청크 단위 재시도(최대 3회)까지 프론트에 구현되어 있어 네트워크가 불안정해도 전체를 다시 올릴 필요가 없음 | 한 번에 전체 파일 업로드 — 구현은 단순하지만 대용량 zip에서 타임아웃/413 에러 위험 |
| **axios / lucide-react / canvas-confetti** | axios는 인터셉터·에러 처리가 fetch보다 편해서 재시도 로직 구현에 유리, lucide-react는 가벼운 아이콘 세트, canvas-confetti는 결과 화면의 축하 애니메이션을 몇 줄로 구현 | fetch API, 다른 아이콘 라이브러리 — 기능적으로 큰 차이는 없고 개발 편의성 선택으로 보임 |

**참고 — 설치돼 있지만 실제로 안 쓰이는 것들** (발표에서 "이건 왜 있냐"는 질문 나올 수 있음):
- `chart.js` / `react-chartjs-2`: 프론트엔드 어디에서도 import되지 않음 (차트 화면을 만들려다 취소된 것으로 추정)
- `apscheduler`: 백엔드 requirements에는 있지만 실제 코드에서 import된 적이 없음. 정리 작업은 `apscheduler` 대신 FastAPI의 `BackgroundTasks` + 수동 TTL 체크(`cleanup.py`)로 처리됨
- `one_pick.py`와 `TopPickCard.jsx`/`RunnerUpList.jsx`: "가장 많이 상호작용한 계정 랭킹"이라는 별도 기능으로 만들어졌지만 현재 라우터/페이지 어디에도 연결되어 있지 않음

---

## 📌 발표 시 가장 중요하게 짚어야 할 5가지 (요약)

1. **핵심은 "저장 = 진짜 취향"이라는 가중치 설계다.** 좋아요보다 저장(3배)·스토리반응(4배)에 더 높은 점수를 줘서, 공개적 반응과 사적 반응을 분리해 "숨겨진 취향"을 찾아낸다.
2. **TF-IDF + 형제태그(sibling) 패널티로 "흔한 태그/스팸 태그"를 통계적으로 걸러낸다.** 하드코딩 불용어 리스트가 아니라 수식으로 걸러내는 게 이 프로젝트의 차별점이다.
3. **DuckDuckGo 검색은 실제로 호출되지 않는다.** 지금은 분석된 키워드로 인스타그램 탐색(`explore/tags`) 링크를 직접 생성하는 구조이며, 이는 검색엔진 차단 문제를 피하기 위한 설계 변경이었다.
4. **Vercel 서버리스의 제약(500MB `/tmp`, 실행시간 제한)이 아키텍처 전체를 결정했다.** 2MB 청크 업로드, zip 전체를 안 풀고 필요한 5개 json만 추출, Vector DB 대신 즉석 통계 분석 — 전부 이 제약에서 나온 선택이다.
5. **`one_pick.py`, `TopPickCard`, `chart.js`, `apscheduler` 등 미사용 코드가 남아있다.** AI에게 위임해 짜다 보니 생긴 흔적이며, 질문이 나오면 "초기 기획엔 있었지만 최종 흐름엔 연결되지 않은 실험적 기능"이라고 답하면 된다.
