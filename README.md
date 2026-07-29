# 🔍 InstaScope (인스타스코프)

> **"인스타가 당신에 대해 아는 모든 것을 해부합니다"**  
> 사용자가 인스타그램 데이터 다운로드(ZIP)를 업로드하면, 자동 파싱 및 알고리즘 교차 검증을 통해 **취향 DNA · 비밀 컬렉션 · 이상형 계정/게시물 추천 · 알고리즘 프로파일링 폭로** 결과를 실시간 시각화해주는 웹 서비스입니다.

---

## ✨ 주요 기능 (Features)

### 🌶️ 1. 취향 DNA 리포트 (부드러움 ↔ 매콤함 ↔ 불닭)
- **매운맛 측정기**: 상호작용 깊이, 새벽 소비 비율, 저장/좋아요 비율 기반 0~100점 점수 산출
- **카테고리 레이더 차트**: 애니/덕질, 자기계발, 여행, 유머, 동물, 패션 등 6대 영역 분류
- **시간대별 소비 히트맵**: 00시~06시 심야 야간 활동 패턴 시각화

### 🔒 2. 비밀 컬렉션 해부
- **비밀 저장 교차 분석**: 저장 O + 좋아요 X 콘텐츠 추적 (남에게 들키지 않은 내적 취향)
- **비밀 저장 키워드 태그 클라우드**: 숨겨진 핫 키워드 추출
- **비공개 컬렉션 요약**: 컬렉션별 구성 및 샘플 메타데이터 렌더링

### 💕 3. 이상형 계정 & 게시물 추천 (MAIN)
- **관심 점수 공식**: `(좋아요×2) + (저장×3) + (스토리 시청×1) + (스토리 좋아요×4)`
- **이상형 관심 프로필 TOP 10**: 무의식 알고리즘이 가리키는 상위 관심 계정 순위
- **취향 맞춤 추천 게시물**: 저장 및 반응도가 높은 대표 게시물 타임라인 추천

### 🕵️ 4. 알고리즘 프로파일링 폭로
- **Meta 타겟팅 태그 클라우드**: 인스타 광고 알고리즘이 나에게 부여한 카테고리 폭로
- **위치 & 기기 추적 현황**: 파악된 관심 위치(양산, 부산, 대구 등) 및 디바이스 추적 내역
- **프라이버시 노출 지수**: 타겟팅 노출 수준 시각화

---

## 🛠️ 기술 스택 (Tech Stack)

- **Frontend**: React 18, Vite 5, Chart.js, Lucide React, Canvas Confetti, Vanilla CSS (Glassmorphism)
- **Backend**: Python 3.12+, FastAPI, Pandas, APScheduler
- **Database / Serverless**: Supabase (PostgreSQL), Vercel Serverless Functions

---

## 🚀 로컬 실행 방법 (Local Setup)

### 1. 백엔드 (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```

### 2. 프론트엔드 (React Vite)
```bash
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:5173/` 접속 후 사용 가능합니다.
