# 🔍 Insta 1-Pick (인스타 1픽)

> **"당신의 무의식이 선택한 진짜 최애는 누구일까요?"**  
> 사용자가 인스타그램 데이터(ZIP)를 업로드하면, 알고리즘(좋아요, 저장, 스토리 시청 등)을 분석하여 **내가 가장 집착하는 1명의 계정(1-Pick)**을 찾아내는 웹 서비스입니다.

---

## ✨ 핵심 기능 (Features)

### 👑 1. 무의식 최애 계정(1-Pick) 추적
- **1-Pick 점수 공식**: `(좋아요×2) + (비밀 저장×3) + (스토리 시청×1) + (스토리 반응×4)`
- 인스타그램의 단순한 팔로잉/팔로워 목록이 아닌, 실제 상호작용 빈도와 깊이를 분석하여 가장 점수가 높은 1위 계정을 선별합니다.
- 아깝게 1위를 놓친 2~5위(Runner-Ups) 계정들의 명단과 점수도 함께 제공합니다.

### 🛡️ 2. 안전한 데이터 분석 체계
- **대용량 파일 인메모리 스트리밍 (In-Memory Streaming)**: 서버리스 환경(Vercel)의 하드디스크 한계(500MB)를 극복하기 위해, 기가바이트(GB) 단위의 파일이라도 디스크에 풀지 않고 필요한 JSON 파일 4개만 메모리로 읽어들여 분석합니다.
- **분석 결과 안전 보관**: 분석된 최종 요약(1-Pick 점수 및 순위)만 Supabase 데이터베이스에 안전하게 보관되며, 언제든 결과를 다시 조회할 수 있습니다.

---

## 🛠️ 기술 스택 (Tech Stack)

- **Frontend**: React 18, Vite, React Router DOM v7, Lucide React, Canvas Confetti, Vanilla CSS (Glassmorphism)
- **Backend**: Python 3.12+, FastAPI (메모리 스트리밍 파서 도입)
- **Database / Serverless**: Supabase (PostgreSQL), Vercel Serverless Functions

---

## 🚀 로컬 실행 방법 (Local Setup)

### 1. 백엔드 (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```
*(또는 로컬 엔진 테스트를 위해 `python test_run.py`를 실행할 수 있습니다.)*

### 2. 프론트엔드 (React Vite)
```bash
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:5173/` 접속 후 사용 가능합니다.
