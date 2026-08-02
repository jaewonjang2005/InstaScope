# 🔍 Insta Taste Recommender (인스타 취향 분석 추천기)

> **"당신이 가장 끌리는 해시태그와 은밀한 취향은 무엇인가요?"**  
> 사용자가 인스타그램 데이터(ZIP)를 업로드하면, 무의식적으로 반응(좋아요, 저장, 스토리 시청 등)을 남긴 해시태그를 추출하여 당신만의 **맞춤형 취향 콘텐츠를 실시간으로 스크래핑(DuckDuckGo)하여 추천**해주는 웹 서비스입니다.

---

## ✨ 핵심 기능 (Features)

### 👑 1. 심층 키워드 추출 & 가중치 분석
- **취향 점수 공식**: `(스토리 시청×1) + (좋아요×2) + (비밀 저장×3) + (스토리 반응×4)`
- 인스타그램에 남긴 활동 내역을 텍스트 기반(해시태그, 카테고리 라벨)으로 파싱하여, 가장 많이, 가장 깊게 반응한 핵심 키워드(SFW/NSFW)를 도출합니다.

### 🛡️ 2. 우회 스크래핑 기반 콘텐츠 추천 (Vector DB ❌ -> Real-time Search ⭕)
- **19금/선정적 단어 필터링 및 우회 매핑**: 성인인증에 걸리지 않는 대체 단어(예: 야동 -> 화보)로 자동 매핑하여 안전하게 검색을 수행합니다.
- **실시간 DuckDuckGo 스크래핑**: 별도의 무거운 Vector DB(pgvector, FAISS)를 사용하지 않고 `site:instagram.com` 검색 쿼리를 통해 최신 트렌드 인스타 게시물을 실시간으로 가져옵니다. Vercel의 Serverless 환경에 완벽하게 최적화되어 메모리 부담이 적습니다.

### 🚀 3. 대용량 파일 스트리밍 파싱
- **In-Memory ZIP Streaming**: Vercel의 500MB 디스크 제한을 우회하기 위해, 클라이언트가 청크 단위로 업로드한 바이너리를 합친 뒤 압축을 풀지 않고 메모리상에서 필요한 JSON 파일 4개만 추출하여 파싱합니다.

---

## 🛠️ 기술 스택 (Tech Stack)

- **Frontend**: React 18, Vite, React Router DOM v7, Lucide React, Vanilla CSS (Glassmorphism + Neon Glow)
- **Backend**: Python 3.12+, FastAPI, `ddgs` (DuckDuckGo Search)
- **Database / Serverless**: Supabase (PostgreSQL), Vercel Serverless Functions

---

## 🚀 로컬 실행 방법 (Local Setup)

### 1. 백엔드 (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```
*(로컬 엔진 테스트: `python test_run.py`)*

### 2. 프론트엔드 (React Vite)
```bash
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:5173/` 접속 후 사용 가능합니다.
