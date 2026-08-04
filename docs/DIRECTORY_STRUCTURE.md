# InstaScope 폴더 트리 및 파일 명세서 (Directory Cheat Sheet)

이 문서는 프로젝트의 전체 구조를 시각화한 폴더 트리와, 각 파일이 어떤 역할을 담당하는지 한 줄 요약으로 설명하는 치트시트입니다. 특정 기능을 수정하고 싶을 때 어디를 열어야 할지 직관적으로 찾을 수 있습니다.

---

## 🌳 전체 디렉토리 트리 (Directory Tree)

```text
InstaScope-Project/
├── 📁 frontend/                     # React (Vite) 프론트엔드 코드
│   ├── 📁 src/
│   │   ├── 📁 assets/               # 이미지, 아이콘, 폰트 파일
│   │   ├── 📁 components/           # 재사용 가능한 UI 컴포넌트 (버튼, 네온 뱃지 등)
│   │   ├── 📁 pages/                # 라우팅되는 메인 페이지들
│   │   │   ├── UploadPage.jsx       # ZIP 파일 드래그 앤 드롭 및 청크 분할 전송
│   │   │   ├── LoadingPage.jsx      # 백엔드 작업 대기 및 상태 폴링(Polling) 화면
│   │   │   ├── ResultPage.jsx       # 일반(SFW) 취향 결과 렌더링 화면
│   │   │   └── SecretPickPage.jsx   # 서브/매운맛 취향 (토글 State 전환) 화면
│   │   ├── App.jsx                  # React Router 컨트롤 타워
│   │   ├── index.css                # Tailwind CSS 및 전역 스타일 (Glassmorphism)
│   │   └── main.jsx                 # React 앱 진입점 (Entry Point)
│   ├── package.json                 # 프론트엔드 의존성 및 빌드 스크립트
│   └── vite.config.js               # Vite 빌드 설정
│
├── 📁 backend/                      # Python (FastAPI) 백엔드 코드
│   ├── 📁 app/
│   │   ├── 📁 api/
│   │   │   └── routes.py            # 프론트엔드와 통신하는 엔드포인트 및 메모리 조립
│   │   ├── 📁 services/
│   │   │   ├── parser.py            # 인스타 JSON (likes, saved_posts) 구조 분해 및 리스트화
│   │   │   ├── keyword_extractor.py # 💡 핵심 엔진 (동시 출현, 시간 감쇠 기반 취향 추출)
│   │   │   ├── search_service.py    # DuckDuckGo(DDGS) 실시간 검색 및 Safe Mapping (우회)
│   │   │   └── db_service.py        # Supabase 저장 로직 및 Memory Fallback 방어막
│   │   ├── 📁 utils/
│   │   │   └── cleanup.py           # 메모리 찌꺼기 정리 유틸 (OOM 방지)
│   │   └── main.py                  # FastAPI 앱 초기화 및 라우터 등록
│   └── requirements.txt             # 백엔드 Python 패키지 의존성 명세
│
├── 📁 api/                          # Vercel Serverless 배포용 진입점
│   └── index.py                     # Vercel이 FastAPI(backend/app/main.py)를 읽을 수 있게 래핑
│
├── 📁 docs/                         # 기획, 구조, 발표 스크립트 등 문서 보관소
│   ├── PROJECT_ARCHITECTURE.md      # 전체 아키텍처 및 재현 가이드
│   ├── ARCHITECTURE_DIAGRAM.md      # 시각적 설계도 (Mermaid 플로우차트)
│   ├── API_SPECIFICATION.md         # API 엔드포인트 및 JSON 통신 규약
│   └── 발표준비.md                    # 비전공자 대상 PT 대본
│
└── vercel.json                      # 프론트엔드 및 백엔드 라우팅 리다이렉트 통합 설정 파일
```

---

## 🔎 유지보수 퀵 가이드 (수정 시 참조)

만약 프로젝트를 개선하거나 수정하고 싶다면 아래 파일을 바로 열어보세요.

1. **"프론트엔드 디자인(색상, 테마)을 고치고 싶어요"**
   ➡️ `frontend/src/index.css` (테일윈드 유틸) 및 `pages/ResultPage.jsx`의 클래스 수정
2. **"매운맛 버튼을 눌렀을 때 화면이 부자연스러워요"**
   ➡️ `frontend/src/pages/SecretPickPage.jsx`의 `useState` 렌더링 로직 수정
3. **"Vercel 서버가 용량 초과로 뻗어요"**
   ➡️ `backend/app/api/routes.py` 의 메모리 스트리밍 및 `BytesIO` 삭제(`del`) 부분 점검
4. **"취향 키워드가 너무 엉뚱하게 묶여서 나와요 (로직 개선)"**
   ➡️ `backend/app/services/keyword_extractor.py` 내의 `weight(가중치)` 수식 계산 부분 튜닝
5. **"특정 매운맛 단어가 검색 엔진에서 차단(Block) 당해요"**
   ➡️ `backend/app/services/search_service.py` 내의 `Safe Mapping Dictionary`에 대체 단어 추가
