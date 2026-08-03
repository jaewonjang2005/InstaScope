# 📋 InstaScope 3단계 페이지 전환 & 초슬림 데이터셋 개편 계획서

## 🎯 목표
1. **사용자 경험(UX) 극대화**: 업로드 후 멍하니 기다리지 않고, **탐정/프로파일러 스타일의 몰입감 넘치는 3단계 전용 화면(업로드 ➡️ 탐정 스캐닝 로딩 ➡️ 프로파일링 대시보드)**으로 서비스 완성도 업그레이드.
2. **초슬림 필수 데이터셋 정의 (< 1MB)**: Vercel 서버리스 4.5MB 업로드 제한을 완벽하게 준수할 수 있도록 **필수 핵심 JSON 파일**로 데이터 규격을 슬림화하고 백엔드 유연한 예외 처리 강화.

---

## 📐 1. 3단계 서비스 페이지 구조 설계

```
[Page 1: 업로드 랜딩]  ──(파일 드롭)──>  [Page 2: 탐정 프로파일링 로딩]  ──(분석 완료)──>  [Page 3: 결과 대시보드]
 - 타이틀 & 4대 리포트 소개               - 네온 탐정 그래픽 + 프로그레스 바              - 4대 도파민 탭 리포트
 - 초슬림 ZIP 준비 가이드                 - 단계별 실시간 파싱 상태 릴레이               - Confetti 폭죽 연출
 - ZIP 드롭존                            - 펄스 스캐너 애니메이션                     - 결과 공유 & 재분석
```

---

## 🧱 2. 세부 컴포넌트 및 백엔드 파서 변경 계획

### [MODIFY] [App.jsx](file:///c:/Users/jjaew/OneDrive/바탕 화면/2026 2학기 부트캠프 스터디/7-8월 토이프로젝트(인스타 알고리즘 분석)/frontend/src/App.jsx)
- 상태값 `step` 관리 (`'upload'` | `'loading'` | `'results'`)
- `loading` 모드일 때 `LoadingSection` 컴포넌트 렌더링.
- 분석 완료 시 `'results'` 모드로 전환 및 결과 데이터 전달.

### [NEW] [LoadingSection.jsx](file:///c:/Users/jjaew/OneDrive/바탕 화면/2026 2학기 부트캠프 스터디/7-8월 토이프로젝트(인스타 알고리즘 분석)/frontend/src/components/LoadingSection.jsx)
- AI로 생성한 탐정 프로파일러 이미지 (`public/detective.png`) 렌더링
- 사이버펑크 펄스 애니메이션 + 프로그레스 바 (0% ➡️ 100%)

---

## 🚀 3. Ver 2.0 (your_instagram_activity 전용 개편)

### 📌 개편 목적 및 변경 사항
- **광고(`ads_information`) 및 커넥션(`connections`) 배제**: 사용자가 여러 폴더를 복잡하게 챙길 필요 없이, **내 활동 전용 폴더(`your_instagram_activity`)만 집중 파싱**하도록 변경.
- **활동 데이터셋 파싱 대상**:
  1. `your_instagram_activity/likes/liked_posts.json` (좋아요 게시물)
  2. `your_instagram_activity/saved/saved_posts.json` (저장한 게시물)
  3. `your_instagram_activity/saved/saved_collections.json` (저장 컬렉션)
  4. `your_instagram_activity/story_interactions/story_likes.json` (스토리 좋아요)
  5. `your_instagram_activity/story_interactions/stories_viewed.json` (스토리 시청 이력)
- **알고리즘 및 가중치 업데이트**: 커넥션 파일이 없어도 좋아요/저장/스토리 반응 계정 주소를 역추적하여 이상형 후보 및 관심 분야 카테고리를 100% 자체 산출.
