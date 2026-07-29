# 📊 Instagram 전체 데이터 분석 보고서
### `instagram-lex_xelop-전체데이터(7.28.2026 기준).zip`
> 분석일: 2026-07-29 | 데이터 기준일: 7.28.2026 | 총 용량: ~868MB

---

## 📑 목차
1. [전체 디렉토리 구조](#1-전체-디렉토리-구조)
2. [각 폴더별 세부 구조 및 JSON 스키마 분석](#2-각-폴더별-세부-구조-및-json-스키마-분석)
3. [데이터 단위 구조 패턴](#3-데이터-단위-구조-패턴)
4. [2차 가치 창출 아이디어 — 도파민 극대화 에디션](#4-2차-가치-창출-아이디어--도파민-극대화-에디션)

---

## 1. 전체 디렉토리 구조

```
instagram-lex_xelop-전체데이터(7.28.2026 기준)/
├── 📁 ads_information/                    # 광고 및 콘텐츠 소비 이력
│   ├── 📁 ads_and_topics/                 # 광고/게시물/영상 시청 기록
│   │   ├── ads_viewed.json                (3.2MB, 55,247줄) ← 본 광고 전체
│   │   ├── posts_viewed.json              (8.9MB, 135,339줄) ← 본 게시물 전체
│   │   ├── posts_you're_interested_or_not_interested_in.json (293KB)
│   │   ├── posts_you're_not_interested_in.json (30KB)
│   │   ├── profiles_you're_not_interested_in.json (491B)
│   │   ├── suggested_profiles_viewed.json (10KB)
│   │   └── videos_watched.json            (8.2MB, 146,243줄) ← 본 영상(릴스) 전체
│   └── 📁 instagram_ads_and_businesses/   # 광고주 정보
│       ├── advertisers_using_your_activity_or_information.json (570KB)
│       ├── information_you've_submitted_to_advertisers.json (2.8KB)
│       └── other_categories_used_to_reach_you.json (3KB)
│
├── 📁 apps_and_websites_off_of_instagram/ # 외부 앱/웹사이트 활동
│   └── 📁 apps_and_websites/
│       └── your_activity_off_meta_technologies_settings.json (1.7KB)
│
├── 📁 connections/                        # 팔로워/팔로잉 관계
│   └── 📁 followers_and_following/
│       ├── close_friends.json             (19KB) ← ⭐ 친한 친구 목록
│       ├── followers_1.json               (76KB) ← 팔로워 전체
│       ├── following.json                 (142KB) ← 팔로잉 전체
│       ├── pending_follow_requests.json   (3.4KB)
│       ├── profiles_you've_favorited.json (13KB) ← ⭐ 즐겨찾기 프로필
│       ├── recent_follow_requests.json    (8.8KB)
│       ├── recently_unfollowed_profiles.json (2.9KB) ← ⭐ 최근 언팔
│       └── removed_suggestions.json       (44KB)
│
├── 📁 logged_information/                 # 활동 로그
│   ├── 📁 link_history/
│   │   ├── link_history.json              (97KB) ← 클릭한 외부 링크
│   │   └── your_link_history_settings.json (497B)
│   ├── 📁 past_instagram_insights/        # 크리에이터 인사이트
│   │   ├── audience_insights.json         (5.2KB)
│   │   ├── content_interactions.json      (5.1KB)
│   │   ├── live_videos.json               (1.1KB)
│   │   ├── posts.json                     (2.5KB)
│   │   └── profiles_reached.json          (2.2KB)
│   └── 📁 recent_searches/
│       └── recent_searches.json           (1.9KB) ← ⭐ 최근 검색어
│
├── 📁 media/                              # 업로드한 미디어 파일
│   ├── 📁 other/ (1개 이미지)
│   ├── 📁 posts/ (90개 파일: jpg, webp, heic, mp4)
│   └── 📁 stories/ (39개 월별 폴더: 202104 ~ 202607)
│
├── 📁 personal_information/               # 개인정보
│   ├── 📁 autofill_information/
│   │   └── autofill_information.json      (13KB)
│   ├── 📁 device_information/
│   │   └── camera_information.json        (22KB) ← 카메라/기기 정보
│   ├── 📁 information_about_you/
│   │   ├── locations_of_interest.json     (2.2KB) ← ⭐ 관심 위치(부산, 양산 등)
│   │   └── profile_based_in.json          (518B)
│   └── 📁 personal_information/
│       ├── instagram_friend_map.json      (3KB)
│       ├── instagram_profile_information.json (5KB)
│       ├── note_and_repost_interactions.json (67KB) ← 노트/리포스트 상호작용
│       ├── notes.json                     (770B)
│       ├── personal_information.json      (2.9KB)
│       └── profile_changes.json           (25KB) ← ⭐ 프로필 변경 이력
│
├── 📁 preferences/                        # 환경설정
│   ├── 📁 settings/
│   │   ├── consents.json                  (782B)
│   │   └── notification_preferences.json  (4.4KB)
│   └── 📁 your_topics/
│       └── 📁 your_ads_see_more/
│           └── see_less_topics.json       (3KB) ← 덜 보기 설정한 토픽
│
├── 📁 security_and_login_information/     # 보안/로그인
│   └── 📁 login_and_profile_creation/
│       ├── last_known_location.json       (1.1KB)
│       ├── login_activity.json            (135KB) ← ⭐ 로그인 기록(IP, UA, 시간)
│       ├── logout_activity.json           (9.8KB)
│       ├── password_change_activity.json  (553B)
│       ├── profile_activity.json          (325KB) ← 프로필 활동 로그
│       ├── profile_privacy_changes.json   (533B)
│       ├── profile_status_changes.json    (1.2KB)
│       └── signup_details.json            (1.2KB) ← 가입 정보
│
└── 📁 your_instagram_activity/            # 핵심 활동 데이터
    ├── 📁 avatars_store/
    │   └── avatar_items.json              (8.1KB)
    ├── 📁 comments/
    │   ├── hype.json                      (1KB)
    │   ├── post_comments_1.json           (83KB) ← 작성한 댓글
    │   └── reels_comments.json            (21KB) ← 릴스 댓글
    ├── 📁 likes/
    │   ├── liked_comments.json            (4.7KB)
    │   └── liked_posts.json               (25.7MB, 511,272줄) ← ⭐⭐⭐ 좋아요 전체
    ├── 📁 media/                          # 내가 올린 콘텐츠 메타데이터
    │   ├── archived_posts.json            (40KB)
    │   ├── other_content.json             (84KB)
    │   ├── posts.json                     (584KB)
    │   ├── posts_1.json                   (777B)
    │   ├── profile_photos.json            (331B)
    │   ├── reposts.json                   (173KB) ← 리포스트 기록
    │   └── stories.json                   (385KB)
    ├── 📁 messages/                       # DM 메시지
    │   ├── 📁 broadcast/ (8개 채널)
    │   ├── 📁 inbox/ (268개 DM 대화방) ← ⭐⭐⭐
    │   ├── 📁 message_requests/
    │   ├── 📁 photos/
    │   ├── secret_conversations.json      (420B)
    │   └── your_chat_information.json     (497KB)
    ├── 📁 monetization/
    │   └── eligibility.json               (582B)
    ├── 📁 other_activity/
    │   ├── your_information_download_requests.json (4.8KB)
    │   └── your_ownership_of_digital_items.json (24KB)
    ├── 📁 posts/
    │   └── 📁 media/
    ├── 📁 saved/
    │   ├── saved_collections.json         (1.1MB) ← ⭐ 저장 컬렉션
    │   ├── saved_music.json               (7.8KB)
    │   └── saved_posts.json               (60.3MB, 1,142,238줄) ← ⭐⭐⭐ 저장 전체
    ├── 📁 shopping/
    │   ├── checkout_payment_information.json (3.7KB)
    │   └── recently_viewed_items.json     (564B)
    ├── 📁 story_interactions/
    │   ├── avatar_story_reactions.json    (15KB)
    │   ├── emoji_sliders.json             (15KB) ← 이모지 슬라이더 반응
    │   ├── polls.json                     (1.1MB) ← ⭐ 투표 참여 기록
    │   ├── question_media_response.json   (8.6KB)
    │   ├── questions.json                 (136KB) ← 질문 응답
    │   ├── quizzes.json                   (7.5KB)
    │   ├── stories_viewed.json            (9.6MB, 165,832줄) ← ⭐ 본 스토리
    │   ├── story_likes.json               (1.1MB) ← 스토리 좋아요
    │   └── story_reaction_sticker_reactions.json (8.9KB)
    └── 📁 subscriptions/
        └── reels.json                     (767B)
```

---

## 2. 각 폴더별 세부 구조 및 JSON 스키마 분석

### 2.1 `ads_information/` — 광고 정보

#### 2.1.1 `ads_and_topics/ads_viewed.json`
> 사용자에게 노출된 광고 기록. **55,247줄**, 수천 개의 광고 항목.

```json
[
  {
    "timestamp": 1784687356,           // Unix timestamp (광고 노출 시각)
    "media": [],                        // 미디어 (보통 비어있음)
    "label_values": [
      { "label": "광고 라이브러리 공개 URL", "value": "https://facebook.com/ads/library/?id=...", "href": "..." },
      { "label": "브랜드 파트너", "vec": [] },
      { "label": "브랜드 파트너의 프로필", "vec": [] },
      { "label": "URL", "value": "https://www.instagram.com/p/...", "href": "..." },
      { "label": "캡션", "value": "광고 캡션 텍스트" },
      { "label": "제목", "value": "" },
      { "dict": [{ "dict": [{ "label": "이름", "value": "광고주명" }], "title": "" }], "title": "해시태그" }
    ]
  }
]
```

#### 2.1.2 `ads_and_topics/posts_viewed.json` & `videos_watched.json`
> 각각 본 게시물(135,339줄)과 본 영상/릴스(146,243줄). **스키마는 ads_viewed와 동일.**

#### 2.1.3 `ads_and_topics/posts_you're_interested_or_not_interested_in.json`
> 관심 있음/없음 표시한 게시물. 피드백 타입(더보기/관심없음), 화면(릴스/피드), 출처(게시물) 등 메타데이터 포함.

```json
{
  "label_values": [
    { "label": "피드백", "value": "더 보기" },
    { "label": "화면", "value": "릴스" },
    { "label": "출처", "value": "게시물" },
    { "dict": [{ "dict": [{ "label": "URL" }, { "label": "캡션" }] }] }
  ]
}
```

#### 2.1.4 `instagram_ads_and_businesses/advertisers_using_your_activity_or_information.json`
> 사용자를 타겟팅한 광고주 목록. **570KB**, 수백 개 광고주.

```json
{
  "label_values": [
    {
      "label": "타겟 리스트를 업로드한 광고주",
      "vec": [
        { "value": "카페24 마케팅센터" },
        { "value": "29CM" },
        { "value": "CLASS101" }
        // ... 수백 개
      ]
    }
  ]
}
```

#### 2.1.5 `instagram_ads_and_businesses/other_categories_used_to_reach_you.json`
> **인스타가 추론한 사용자 광고 카테고리** ← 🔥 핵심 데이터

```json
{
  "label_values": [{
    "label": "이름",
    "vec": [
      { "value": "Birthday in October" },
      { "value": "Frequent international travelers" },
      { "value": "Friends of Soccer fans" },
      { "value": "결혼/연애 상태: single" },
      { "value": "Facebook access (mobile): Samsung Android mobile devices" }
      // ...
    ]
  }]
}
```

---

### 2.2 `connections/followers_and_following/` — 인간관계

| 파일 | 설명 | 레코드 수 (추정) |
|------|------|-------------------|
| `followers_1.json` | 팔로워 전체 | ~330명 |
| `following.json` | 팔로잉 전체 | ~510명 |
| `close_friends.json` | 친한 친구 | ~40명 |
| `profiles_you've_favorited.json` | 즐겨찾기 | ~27명 |
| `recently_unfollowed_profiles.json` | 최근 언팔 | 6명 |
| `pending_follow_requests.json` | 대기 중 요청 | 소수 |
| `recent_follow_requests.json` | 최근 팔로우 요청 | 소수 |
| `removed_suggestions.json` | 제거한 추천 | ~200+ |

**followers_1.json 단위 구조:**
```json
{
  "title": "",
  "media_list_data": [],
  "string_list_data": [
    { "href": "https://www.instagram.com/username", "value": "username", "timestamp": 1784958294 }
  ]
}
```

**following.json 단위 구조:**
```json
{
  "relationships_following": [
    {
      "title": "username",
      "string_list_data": [
        { "href": "https://www.instagram.com/_u/username", "timestamp": 1785131744 }
      ]
    }
  ]
}
```

**recently_unfollowed_profiles.json 단위 구조:**
```json
{
  "timestamp": 1785063487,
  "media": [],
  "label_values": [
    { "label": "URL", "value": "" },
    { "label": "이름", "value": "실명" },
    { "label": "사용자 이름", "value": "username" }
  ],
  "fbid": "17841439235292543"
}
```

---

### 2.3 `logged_information/` — 활동 로그

#### `link_history.json` — 클릭한 외부 링크
```json
{
  "timestamp": 1785217734,
  "label_values": [
    { "label": "방문한 웹사이트 링크", "value": "https://docs.google.com/..." },
    { "label": "방문한 웹사이트 페이지의 제목", "value": "생성형 AI 대화 기록 제출 참여 신청서" },
    { "label": "웹사이트 세션 시작 시간", "value": "7월 27, 2026 10:48:07오후" },
    { "label": "웹사이트 세션 종료 시간", "value": "7월 27, 2026 10:48:54오후" }
  ]
}
```

#### `recent_searches.json` — 최근 검색어
```json
{
  "timestamp": 1785068736,
  "label_values": [
    { "label": "검색어", "value": "하코즈메" },
    { "label": "업데이트 시간", "timestamp_value": 1785068736 }
  ]
}
```

---

### 2.4 `personal_information/` — 개인정보

#### `locations_of_interest.json` — 인스타가 추적한 관심 위치
```json
{
  "label_values": [{
    "label": "관심 위치",
    "vec": [
      { "value": "Yangsan, Gyeongsangnam-do" },
      { "value": "Busan, Busan" },
      { "value": "Daegu" },
      { "value": "Incheon" }
    ]
  }]
}
```

#### `profile_changes.json` — 프로필 변경 이력
```json
{
  "title": "프로필 변경 사항",
  "string_map_data": {
    "변경됨": { "value": "Profile Bio Text" },
    "이전 값": { "value": "" },
    "새 값": { "value": "Hello 👋👋" },
    "날짜 변경": { "timestamp": 1612518335 }
  }
}
```

---

### 2.5 `security_and_login_information/` — 보안/로그인

#### `login_activity.json` — 로그인 기록
```json
{
  "title": "2026-07-29T00:55:55+00:00",
  "string_map_data": {
    "쿠키 이름": { "value": "*************************zL7" },
    "IP 주소": { "value": "14.44.120.103" },
    "포트": { "value": "53848" },
    "언어 코드": { "value": "en" },
    "시간": { "timestamp": 1785286555 },
    "사용자 에이전트": { "value": "Mozilla/5.0 (Linux; Android 16; SM-S928N Build/BP4A.251205.006; wv)..." }
  }
}
```

---

### 2.6 `your_instagram_activity/` — 핵심 활동 데이터

#### `likes/liked_posts.json` — 좋아요 누른 게시물 (⭐ 최대 파일)
> **25.7MB**, 511,272줄. 수만 개의 좋아요 기록.

```json
{
  "timestamp": 1785284876,
  "label_values": [
    { "label": "URL", "value": "https://www.instagram.com/reel/...", "href": "..." },
    { "label": "캡션", "value": "게시물 캡션 텍스트 + 해시태그" },
    { "label": "제목", "value": "" },
    { "dict": [{ "dict": [{ "label": "이름", "value": "해시태그명" }], "title": "" }], "title": "해시태그" }
  ]
}
```

#### `saved/saved_posts.json` — 저장한 게시물
> **60.3MB**, 1,142,238줄. 가장 큰 파일. liked_posts와 동일한 구조.

#### `saved/saved_collections.json` — 저장 컬렉션
```json
{
  "timestamp": 1642952323,
  "label_values": [
    { "label": "이름", "value": "귀여운 고양이 및 동물" },   // 컬렉션 이름
    { "label": "유형", "value": "기본" },
    { "label": "공개 범위", "value": "비공개" },
    { "label": "업데이트 시간", "timestamp_value": 1652161683 },
    { "dict": [/* 컬렉션 내 게시물 목록 */] }
  ]
}
```

#### `comments/post_comments_1.json` — 작성한 댓글
```json
{
  "media_list_data": [{ "uri": "" }],
  "string_map_data": {
    "Comment": { "value": "댓글 내용" },
    "Media Owner": { "value": "게시물 주인 username" },
    "Time": { "timestamp": 1785214415 }
  }
}
```

#### `messages/inbox/{conversation_name}/message_1.json` — DM
> 268개 대화방, 각각 `message_1.json` + `/photos/`, `/videos/`, `/gifs/`

```json
{
  "participants": [
    { "name": "Lionel OH" },
    { "name": "장재원" }
  ],
  "messages": [
    {
      "sender_name": "장재원",
      "timestamp_ms": 1784553906690,
      "content": "메시지 내용",
      "is_geoblocked_for_viewer": false,
      "is_unsent_image_by_messenger_kid_parent": false
    },
    {
      // 리액션이 있는 경우
      "reactions": [
        { "reaction": "🧘🏻‍♂️", "actor": "Lionel OH" }
      ]
    }
  ]
}
```

#### `story_interactions/` — 스토리 상호작용

| 파일 | 스키마 핵심 | 레코드 규모 |
|------|------------|-------------|
| `stories_viewed.json` | URL + 캡션 + 해시태그 | 165,832줄 (~수만 개) |
| `story_likes.json` | URL + 작성자 정보 | 37,858줄 |
| `polls.json` | 옵션1~4 + 선택한 옵션 + 작성자 | 20,888줄 |
| `questions.json` | 질문 내용 + 답변 텍스트 | 136KB |
| `emoji_sliders.json` | 슬라이더 이모지 + 위치 값 | 15KB |
| `quizzes.json` | 퀴즈 문제 + 선택 답변 | 7.5KB |

---

## 3. 데이터 단위 구조 패턴

### 3.1 공통 패턴 (Meta Data Download Format)

인스타그램 데이터 다운로드는 크게 **2가지 JSON 스키마 패턴**을 사용합니다:

#### 📌 Pattern A — `label_values` 기반 (대다수 파일)
```json
{
  "timestamp": <unix_timestamp>,
  "media": [],
  "label_values": [
    { "label": "<필드명(한글)>", "value": "<값>" },
    { "label": "<필드명>", "timestamp_value": <unix_timestamp> },
    { "label": "<필드명>", "vec": [{ "value": "<항목>" }, ...] },
    { "dict": [{ "dict": [{ "label": "...", "value": "..." }] }], "title": "<그룹명>" }
  ],
  "fbid": "<meta_internal_id>"
}
```

#### 📌 Pattern B — `string_map_data` 기반 (댓글, 로그인, 프로필 변경 등)
```json
{
  "title": "<항목 제목>",
  "media_map_data": {},
  "string_map_data": {
    "<필드명>": { "href": "", "value": "<값>", "timestamp": <unix_timestamp> }
  }
}
```

#### 📌 Pattern C — DM 메시지 전용
```json
{
  "participants": [{ "name": "..." }],
  "messages": [{
    "sender_name": "...",
    "timestamp_ms": <unix_ms>,
    "content": "...",
    "reactions": [{ "reaction": "...", "actor": "..." }],
    "share": { "link": "..." },
    "photos": [{ "uri": "..." }],
    "videos": [{ "uri": "..." }]
  }]
}
```

### 3.2 인코딩 특이사항

> [!WARNING]
> 모든 한글 텍스트가 **Latin-1 → UTF-8 이중 인코딩**되어 있음.
> 예: `\u00ec\u009e\u00a5\u00ec\u009e\u00ac\u00ec\u009b\u0090` = `장재원`
> 
> 분석 시 반드시 `value.encode('latin-1').decode('utf-8')` 디코딩 필요.

### 3.3 데이터 규모 요약

| 데이터 카테고리 | 파일 수 | 핵심 행(줄) 수 | 비고 |
|---|---|---|---|
| 저장한 게시물 | 1 | 1,142,238 | 🥇 최대 파일 |
| 좋아요 누른 게시물 | 1 | 511,272 | 🥈 |
| 본 스토리 | 1 | 165,832 | |
| 본 영상(릴스) | 1 | 146,243 | |
| 본 게시물 | 1 | 135,339 | |
| 본 광고 | 1 | 55,247 | |
| 스토리 좋아요 | 1 | 37,858 | |
| 투표 참여 | 1 | 20,888 | |
| DM 대화방 | 268 | 수만~수십만 메시지 | |
| 팔로잉 | 1 | ~510명 | |
| 팔로워 | 1 | ~330명 | |
| 친한 친구 | 1 | ~40명 | |

---

## 4. 2차 가치 창출 아이디어 — 도파민 극대화 에디션

### 🧠 Tier 1: 인간관계 해부 — "나를 둘러싼 사람들의 진실"

#### 💔 1-1. 언팔 탐정 — "누가 나를 버렸는가?"
**데이터**: `followers_1.json` × `following.json` × `recently_unfollowed_profiles.json`

- **맞팔 여부 교차 분석**: 내가 팔로잉 중인데 나를 팔로우 안 하는 사람 = **짝사랑 리스트**
- **언팔한 타임라인**: 언팔 시점과 나의 게시물/스토리 업로드 시점을 교차 → "내가 뭘 올렸길래 떠났나?"
- **유령 팔로워**: 나를 팔로우하지만 내 게시물에 좋아요/댓글을 한 번도 안 남긴 사람 (liked_posts, comments와 교차)

> 🔥 **도파민 포인트**: "나를 팔로우만 하고 안 보는 사람 TOP 10" vs "내가 짝사랑하고 있는 계정 TOP 10"

#### 👀 1-2. 스토킹 지수 — "내가 가장 많이 들여다본 사람"
**데이터**: `stories_viewed.json` + `story_likes.json` + `liked_posts.json`

- 스토리를 가장 많이 본 계정 Top 20 (URL에서 username 추출)
- 좋아요를 가장 많이 누른 계정 Top 20
- 스토리 좋아요까지 준 계정 = **진심 관심 계정**
- 이들 중 `close_friends.json`에 없는 사람 = **비밀 관심사**

> 🔥 **도파민 포인트**: "당신이 무의식적으로 가장 스토킹하는 사람은 OOO입니다"

#### 💕 1-3. 친밀도 랭킹 — "DM으로 보는 진짜 관계"
**데이터**: `messages/inbox/*/message_1.json`

- 268개 대화방의 총 메시지 수 / 마지막 메시지 날짜 / 평균 응답 속도
- **내가 먼저 보낸 비율** vs **상대가 먼저 보낸 비율** → 관계의 에너지 방향
- 리액션 이모지 빈도 분석 → 감정 온도계
- 공유한 릴스/게시물 링크 분석 → "어떤 콘텐츠로 소통하는가"

> 🔥 **도파민 포인트**: "상대가 나에게 보내는 관심 점수 vs 내가 보내는 관심 점수" 불균형 시각화

---

### 🎯 Tier 2: 알고리즘 프로파일링 — "인스타가 나를 어떻게 보고 있는가"

#### 🏷️ 2-1. 나의 광고 페르소나 — "인스타가 규정한 나"
**데이터**: `other_categories_used_to_reach_you.json` + `advertisers_using_your_activity_or_information.json`

- 인스타가 나에게 부여한 카테고리: "Birthday in October", "single", "Frequent international travelers" 등
- 나를 타겟팅한 광고주 수백 개 분석 → 카테고리별 분류
- **인스타가 생각하는 나의 연애상태, 소비패턴, 관심사**를 시각화

> 🔥 **도파민 포인트**: "인스타는 당신을 '싱글, 10월생, 삼성폰 유저, 해외여행 자주 가는 축구팬의 친구'로 봅니다"

#### 🕳️ 2-2. 관심사 딥다이브 — "내 무의식의 지도"
**데이터**: `liked_posts.json` + `saved_posts.json` + `videos_watched.json`

- **해시태그 빈도 분석**: 좋아요/저장한 게시물의 해시태그를 전부 추출 → 워드클라우드
- **캡션 텍스트 감성 분석**: 어떤 감정/주제의 콘텐츠에 반응하는지
- **시간대별 소비 패턴**: 새벽에 어떤 콘텐츠를 보는지 vs 낮에 보는 콘텐츠 차이
- **"더 보기" vs "관심없음" 분석**: `posts_you're_interested_or_not_interested_in.json`에서 적극적으로 좋다/싫다 표시한 것만 추출

> 🔥 **도파민 포인트**: "새벽 2시의 당신은 낮의 당신과 다릅니다" — 시간대별 관심사 대비 차트

#### 🗺️ 2-3. 위치 프로파일링 — "인스타가 추적한 나의 동선"
**데이터**: `locations_of_interest.json` + `login_activity.json` + `link_history.json`

- 관심 위치: 양산, 부산, 대구, 대전, 인천, 광주, 울산, 창원
- 로그인 IP 기반 위치 추적 → 시간대별 이동 패턴
- 인스타 내부에서 클릭한 외부 링크의 도메인 분석

> 🔥 **도파민 포인트**: "인스타가 당신의 동선을 이렇게까지 추적하고 있었습니다" 지도 시각화

---

### 🔞 Tier 3: 은밀한 패턴 분석 — "남들이 건드리지 않는 영역"

#### 🌙 3-1. 심야 활동 분석 — "새벽의 나"
**데이터**: 모든 timestamp 기반 데이터

- 00:00~05:00 사이의 활동 집중 분석
- 심야 좋아요/저장/DM 대상 패턴 → 낮과 다른 관심사 추출
- 심야 검색어 분석 (`recent_searches.json`)
- **"잠 못 드는 밤에 무엇을 보는가"** 타임라인

> 🔥 **도파민 포인트**: "당신의 새벽 인스타 평균 사용시간: X분, 가장 많이 본 계정: OOO"

#### 🔥 3-2. 저장 컬렉션 해부 — "남에게 보여주지 않는 취향"
**데이터**: `saved_collections.json` + `saved_posts.json`

- 비공개 저장 컬렉션 이름 분석 ("귀여운 고양이 및 동물" 등)
- 저장했지만 좋아요는 안 누른 게시물 = **"좋아하지만 들키고 싶지 않은 것"**
- 저장 빈도의 시간적 추세 → 관심사의 진화 과정
- 가장 오래된 저장 vs 최신 저장 비교 → "과거의 나 vs 현재의 나"

> 🔥 **도파민 포인트**: "저장만 하고 좋아요는 안 누른 게시물 — 당신의 비밀 취향 TOP 20"

#### 💬 3-3. DM 감정 분석 — "관계의 온도"
**데이터**: `messages/inbox/*/message_1.json` (268개 대화방)

- 특정 사람과의 대화 빈도 변화 → 관계의 시작/소멸 타임라인
- 공유한 게시물/릴스 URL 분석 → "이 사람에게는 어떤 콘텐츠를 보내는가"
- **대화 공백 기간 분석**: 한참 안 연락하다 갑자기 연락한 패턴 → "무슨 일이 있었나"
- 이모지/리액션 사용 패턴으로 감정 온도 측정

> 🔥 **도파민 포인트**: "6개월 만에 연락한 사람 리스트 + 그 시점에 당신이 올린 게시물"

#### 🎭 3-4. 투표/질문 응답 분석 — "내 성격의 데이터화"
**데이터**: `polls.json` + `questions.json` + `quizzes.json` + `emoji_sliders.json`

- 투표에서 항상 어떤 성향의 답변을 고르는지 (보수적 vs 도전적)
- 질문 스토리에 답변한 내용 텍스트 분석 → 성격 프로파일
- 이모지 슬라이더 평균 위치 → 적극성/소극성 지표

> 🔥 **도파민 포인트**: "당신의 MBTI를 인스타 데이터로 재분석합니다"

---

### 🚀 Tier 4: 종합 킬러 분석 — "데이터가 말하는 당신의 모든 것"

#### 👁️ 4-1. "내가 좋아하는 걸 모아봤더니" — 취향 DNA 리포트
**필요 데이터**: liked_posts + saved_posts + videos_watched + stories_viewed + comments

모든 상호작용 데이터를 종합하여:
- **사람 카테고리**: 친구/연예인/일러스트레이터/인플루언서/브랜드
- **콘텐츠 카테고리**: 밈/패션/여행/음식/애니메이션/자기계발
- **감정 카테고리**: 웃긴 것/감동적인 것/섹시한 것/영감 주는 것
- **반응 강도**: 그냥 봄 < 좋아요 < 저장 < 댓글 < DM 공유

> 🔥 **도파민 포인트**: "당신의 인스타그램 취향 DNA 분석표 — 피라미드 시각화"

#### ⏰ 4-2. "인스타 중독 리포트" — 사용 패턴 분석
**필요 데이터**: login_activity + 모든 timestamp 데이터

- 일일 평균 사용시간 추정 (로그인/활동 로그 기반)
- 가장 활발한 요일/시간대 히트맵
- 한 세션에서 평균 몇 개의 게시물을 보는지
- **"인스타 없이 가장 오래 버틴 기간"** 계산

> 🔥 **도파민 포인트**: "당신은 지난 1년간 약 XXX시간을 인스타에 사용했습니다 (그것은 OOO편의 영화를 볼 수 있는 시간입니다)"

#### 🕵️ 4-3. "프로필 변천사" — 당신의 진화
**필요 데이터**: `profile_changes.json` + `media/posts` + `stories`

- 바이오, 유저네임, 프로필 사진 변경 타임라인
- 게시물 스타일의 시대별 변화
- 스토리 업로드 빈도의 증감 추세

> 🔥 **도파민 포인트**: "2021년의 당신 vs 2026년의 당신 — 인스타 페르소나 변천사"

---

### 💎 Bonus: 실행 가능한 프로젝트 아이디어

| # | 프로젝트명 | 핵심 데이터 | 예상 임팩트 |
|---|-----------|------------|------------|
| 1 | **"누가 나를 버렸나" 대시보드** | followers × following | ⭐⭐⭐⭐⭐ |
| 2 | **심야 인스타 프로파일러** | 전체 timestamp 데이터 | ⭐⭐⭐⭐⭐ |
| 3 | **저장만 하고 좋아요 안 누른 비밀 취향** | saved × liked | ⭐⭐⭐⭐⭐ |
| 4 | **DM 관계 온도 히트맵** | messages/inbox | ⭐⭐⭐⭐ |
| 5 | **인스타가 규정한 나의 페르소나** | ad categories | ⭐⭐⭐⭐ |
| 6 | **스토킹 지수 차트** | stories_viewed × likes | ⭐⭐⭐⭐⭐ |
| 7 | **취향 DNA 피라미드** | 전체 interaction 데이터 | ⭐⭐⭐⭐ |
| 8 | **인스타 중독 리포트** | login + all timestamps | ⭐⭐⭐⭐ |

---

> [!TIP]
> **가장 빠르게 임팩트를 만들 수 있는 조합**:
> 1. 먼저 `followers × following` 교차 분석으로 **짝사랑/유령팔로워** 추출
> 2. `liked_posts`에서 **username별 좋아요 빈도** 집계 → 스토킹 지수
> 3. 심야 시간대 필터링으로 **새벽 컨텐츠 패턴** 추출
> 4. 이 세 가지를 하나의 웹 대시보드로 시각화

> [!NOTE]
> 모든 텍스트 데이터는 Latin-1 이중 인코딩 디코딩이 필수이며, timestamp는 Unix 기준입니다.
> DM 메시지는 `timestamp_ms` (밀리초 단위)를 사용합니다.
