# InstaScope (인스타 취향 추천기) 전체 아키텍처 및 재현 가이드

본 문서는 인스타그램 활동 데이터(ZIP 파일)를 기반으로 사용자의 취향(일반, 서브, 매운맛)을 분석하고 추천하는 **InstaScope** 프로젝트의 전체 구조와 작동 원리를 설명하는 완벽한 개발 명세서입니다. 이 문서 하나만으로 전체 시스템을 이해하고 동일하게 구축할 수 있도록 작성되었습니다.

---

## 1. 프로젝트 개요 및 기술 스택

* **프로젝트명**: Insta Taste Recommender (InstaScope)
* **목적**: 사용자가 다운로드한 인스타그램 개인 데이터(ZIP)를 분석하여 사용자의 자아(취향)를 3가지 카테고리로 나누고, 실시간 인터넷 스크래핑을 통해 관련 콘텐츠를 추천합니다.
* **핵심 기술 스택**:
  * **Frontend**: React, Vite, Tailwind CSS (또는 바닐라 CSS + Glassmorphism UI)
  * **Backend**: Python, FastAPI
  * **Database**: Supabase (PostgreSQL)
  * **Deployment**: Vercel (Frontend Hosting + Serverless Functions)
  * **External API/Tools**: DuckDuckGo Search (DDGS)

---

## 2. 전체 시스템 데이터 흐름도 (Data Flow)

1. **[사용자]** 인스타그램 데이터(ZIP) 약 800MB를 프론트엔드(`UploadPage`)에 드래그 앤 드롭합니다.
2. **[프론트엔드]** 거대한 ZIP 파일을 브라우저에서 10MB 단위의 **Chunk(청크)**로 쪼개어 백엔드 API로 순차 전송합니다. (브라우저 및 서버 뻗음 방지)
3. **[백엔드: 라우터]** `routes.py`에서 청크들을 수신하고, 하드디스크를 거치지 않고 **메모리 스트리밍(Memory Streaming)** 방식으로 ZIP 압축을 풉니다.
4. **[백엔드: 파서]** `parser.py`가 압축 풀린 데이터 중 `likes.json`, `saved_posts.json`, `story_likes.json` 핵심 파일 3개만 추출해 파이썬 객체로 변환합니다.
5. **[백엔드: 엔진]** `keyword_extractor.py`가 **'동시 출현(Co-occurrence)'**과 **'시간 감쇠(Time Decay)'** 알고리즘을 적용하여 유저의 취향 키워드를 3가지(SFW, Secret, Spicy)로 분류하여 추출합니다.
6. **[백엔드: 검색]** `search_service.py`가 추출된 키워드를 DuckDuckGo에 검색해 실제 콘텐츠 URL을 가져옵니다. (민감한 단어는 **Safe Mapping**으로 우회 치환하여 19금 차단을 방지)
7. **[백엔드: DB]** `db_service.py`가 최종 결과를 Supabase에 저장하고 `job_id`를 반환합니다. (DB 에러 시 임시 메모리에 저장하는 **Memory Fallback** 로직 작동)
8. **[프론트엔드]** `LoadingPage`에서 상태를 폴링하다 완료되면 `ResultPage`와 `SecretPickPage`로 이동하여 결과를 예쁜 UI(MBTI 스타일, 네온 효과)로 렌더링합니다.

---

## 3. 프론트엔드 (React) 상세 구조

**위치:** `frontend/src/`

프론트엔드는 사용자 경험(UX)과 대용량 파일 처리의 안정성을 최우선으로 설계되었습니다.

### 3.1. `UploadPage.jsx` (파일 업로드 및 청크 분할)
* **역할**: 대용량 ZIP 파일을 서버로 안전하게 넘기는 우체국 역할.
* **핵심 로직**:
  * 사용자가 파일을 올리면 `FileReader`나 `Blob.slice()`를 이용해 파일을 10MB 크기의 청크(Chunk) 배열로 쪼갭니다.
  * `for` 루프 또는 비동기 병렬 통신을 통해 백엔드 API(`/api/upload/chunk`)로 전송합니다.
  * 마지막 청크를 전송할 때 '완료' 플래그를 보내 백엔드가 병합을 시작하도록 트리거합니다.

### 3.2. `LoadingPage.jsx` (폴링 기반 대기 화면)
* **역할**: 백엔드에서 데이터 분석이 끝날 때까지 유저를 대기시키는 화면.
* **핵심 로직**:
  * `setInterval`을 이용해 주기적(예: 3초)으로 백엔드 API(`/api/status/{job_id}`)를 찔러서(Polling) 진행 상태를 확인합니다.
  * 응답 상태가 'SUCCESS'로 바뀌면 `ResultPage`로 라우팅합니다.

### 3.3. `ResultPage.jsx` & `SecretPickPage.jsx` (결과 렌더링)
* **역할**: 분석된 취향 데이터를 시각화.
* **핵심 로직**:
  * 백엔드에서 넘겨받은 데이터(`SFW`, `Secret`, `Spicy`)를 `useState`에 저장합니다.
  * **상태 관리 (State)**: 서브 취향 페이지(`SecretPickPage`)에는 '매운맛🔥 토글 버튼'이 있습니다. 이 토글 상태(`isSpicyMode`)에 따라 화면을 새로고침하지 않고 일반 서브 취향 데이터와 매운맛 데이터를 즉각적으로 교체하여 렌더링합니다 (조건부 렌더링).

---

## 4. 백엔드 (FastAPI) 상세 구조

**위치:** `backend/app/`

백엔드는 하드코딩된 사전(Dictionary)을 배제하고 수학적 알고리즘과 메모리 관리 효율성을 극대화했습니다.

### 4.1. `api/routes.py` (엔드포인트 및 메모리 스트리밍)
* **역할**: 프론트엔드와의 통신, 데이터 수신.
* **핵심 로직**:
  * Vercel의 Serverless 환경은 디스크 쓰기 용량이 500MB로 제한되어 있습니다.
  * 따라서 전송받은 ZIP 청크들을 디스크에 `open(filename, 'wb')`로 저장하는 대신, 파이썬의 `io.BytesIO`를 활용하여 램(RAM) 위에 띄워놓고 압축을 해제(`zipfile` 모듈)합니다.
  * 필요한 알맹이만 빼낸 뒤 메모리를 즉시 비워(`del`) 서버 폭발(OOM)을 방지합니다.

### 4.2. `services/parser.py` (JSON 파싱)
* **역할**: 복잡한 인스타 폴더 구조 속에서 필요한 데이터 추출.
* **핵심 로직**:
  * `likes.json`, `saved_posts.json`, `story_likes.json` 파일의 트리 구조를 순회하며 정규화된 리스트 객체로 변환합니다.

### 4.3. `services/keyword_extractor.py` (핵심 분석 엔진)
* **역할**: 가장 중요한 취향 분석 알고리즘 작동.
* **핵심 로직**:
  * **1. 동시 출현 네트워크 (Co-occurrence)**: 하나의 게시물(릴스)에 등장한 해시태그들의 쌍(Pair)을 인접 리스트 딕셔너리로 묶어 가중치를 누적합니다. 이를 통해 A태그와 B태그가 함께 자주 쓰인다는 '문맥'을 컴퓨터가 이해합니다.
  * **2. 시간 감쇠 (Time Decay)**: 과거 데이터가 최신 트렌드를 압도하는 것을 막기 위해, 최근 1달 내의 활동은 가중치 3배, 6개월은 1.5배, 1년 이상은 0.2배로 점수를 차등 부여(`weighted_count`)합니다.
  * **결과 추출**: 1등 태그를 '메인 주제'로 잡고, 동시 출현 딕셔너리를 뒤져 메인 태그와 엮여있는 연관 태그 4개를 끌어와 하나의 '취향 묶음(5개)'을 만듭니다.

### 4.4. `services/search_service.py` (검색 및 우회)
* **역할**: 추출된 태그에 맞는 콘텐츠 URL 실시간 수집.
* **핵심 로직**:
  * 외부 라이브러리인 `duckduckgo-search (DDGS)`를 이용해 `site:instagram.com {키워드}` 형식으로 스크래핑합니다.
  * **Safe Mapping**: `hidden_dictionary` 맵을 내부에 두어, '19금/매운맛' 관련 민감 키워드가 검색 필터에 차단되지 않도록 '비키니 ➡️ 해운대 바캉스'처럼 건전한 유사어로 치환하여 검색을 우회합니다.

### 4.5. `services/db_service.py` (데이터베이스 저장 및 무중단 처리)
* **역할**: 최종 결과를 Supabase에 저장.
* **핵심 로직**:
  * **Memory Fallback**: DB 쿼리가 실패(네트워크 오류, RLS 정책 오류 등)하더라도 에러를 발생(`HTTP 500`)시키지 않습니다. 예외(Exception)로 잡은 뒤 서버의 전역 딕셔너리(메모리)에 잠시 데이터를 담아두고 200 OK를 반환합니다. 덕분에 유저는 장애 유무를 모른 채 결과를 정상적으로 확인합니다.

---

## 5. 데이터베이스 (Supabase) 스키마 및 보안

* **테이블명**: `insta_analysis_results`
* **컬럼 구조**:
  * `id` (UUID, Primary Key)
  * `job_id` (String): 프론트엔드와 백엔드가 데이터를 매칭하는 고유 영수증 번호.
  * `result_data` (JSONB): 분석 완료된 SFW, Secret, Spicy 전체 데이터가 통째로 JSON 형태로 들어갑니다.
  * `created_at` (Timestamp)
* **보안 (RLS)**:
  * 프론트엔드에서는 직접 데이터를 Insert할 수 없도록 막고(백엔드 API만 허용), Select 시에는 오직 자신의 `job_id`를 알고 있는 요청만 데이터를 조회할 수 있도록 RLS 정책을 설정해야 합니다.

---

## 6. 배포 환경 (Vercel)

* **프론트엔드**: Vercel에 GitHub 레포지토리를 연결하여 자동 배포(`npm run build`).
* **백엔드 (Serverless)**:
  * 최상위 디렉토리에 `vercel.json`을 만들어 `/api/(.*)` 경로를 백엔드 파이썬 스크립트로 리다이렉트합니다.
  * 루트 경로의 `api/index.py` 파일은 FastAPI 앱(`backend/app/main.py`)을 임포트하여 Vercel Serverless Function이 파이썬 코드를 실행할 수 있도록 진입점(Entrypoint) 역할을 합니다.
  * **환경 변수 (.env)**: Vercel 대시보드에서 `SUPABASE_URL`, `SUPABASE_KEY` 등을 설정합니다.

---

**💡 마치며**
이 가이드를 따라 프론트엔드(청크 업로드) ➡️ 백엔드(메모리 스트리밍 & 동시 출현 알고리즘) ➡️ 외부 연동(DDGS & DB) 순서로 시스템을 조립하면 완벽하게 동일한 InstaScope 애플리케이션을 구축할 수 있습니다.
