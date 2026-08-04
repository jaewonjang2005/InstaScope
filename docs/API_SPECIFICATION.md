# InstaScope API 명세서 (API Specification)

이 문서는 프론트엔드(React)와 백엔드(FastAPI)가 통신하는 API의 규격과 실제 JSON 응답 예시(Mock Data)를 정의합니다.

---

## 1. 파일 청크 업로드 API

대용량 ZIP 파일을 브라우저에서 분할하여 서버로 전송합니다. 마지막 청크 전송 시 백엔드가 분석을 시작합니다.

* **URL**: `/api/upload/chunk`
* **Method**: `POST`
* **Content-Type**: `multipart/form-data`

### Request Data (Form Data)
| 파라미터명 | 타입 | 설명 | 필수 여부 |
|---|---|---|---|
| `file` | File (Blob) | 쪼개진 ZIP 파일 조각 (Chunk) | O |
| `chunkIndex` | Integer | 현재 전송 중인 조각의 순서 (0부터 시작) | O |
| `totalChunks` | Integer | 분할된 전체 조각의 개수 | O |
| `fileName` | String | 원본 ZIP 파일의 이름 | O |
| `jobId` | String | 세션을 식별하는 고유 UUID | O |

### Response (마지막 청크 완료 후 분석 성공 시)
* **Status Code**: `200 OK`
```json
{
  "status": "success",
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "message": "File completely received and analysis started."
}
```

### Error Response (용량 초과 또는 파싱 에러)
* **Status Code**: `500 Internal Server Error`
```json
{
  "error": "Memory limit exceeded during parsing or invalid ZIP format."
}
```

---

## 2. 작업 상태 조회 API (Polling)

프론트엔드 `LoadingPage`에서 백엔드의 분석 작업이 끝났는지 확인하기 위해 주기적으로 호출합니다. 서버리스 구조상 비동기 워커를 쓰기 어려울 때 활용하는 폴링 패턴입니다.

* **URL**: `/api/status/{job_id}`
* **Method**: `GET`
* **URL Params**: `job_id=[string]` (업로드 시 발급받은 UUID)

### Response (분석 진행 중)
* **Status Code**: `200 OK`
```json
{
  "status": "processing",
  "message": "Data is still being parsed and analyzed..."
}
```

### Response (분석 완료 - 최종 취향 데이터 반환)
* **Status Code**: `200 OK`
* **특이사항**: 분석이 완료되면 `status`가 `success`로 변경되고, `data` 필드에 최종 결과가 담겨 옵니다. 프론트엔드는 이 데이터를 그대로 렌더링에 사용합니다.

```json
{
  "status": "success",
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "data": {
    "sfw": {
      "main_keyword": "#동기부여",
      "related_tags": ["#자기계발", "#독서", "#명언", "#성공"],
      "recommendations": [
        { "title": "성공하는 사람들의 아침 루틴", "url": "https://instagram.com/p/..." },
        { "title": "부자들의 생각법", "url": "https://instagram.com/p/..." }
      ]
    },
    "secret": {
      "main_keyword": "#일잘러",
      "related_tags": ["#엑셀꿀팁", "#PPT템플릿", "#직장인스타그램"],
      "recommendations": [
        { "title": "야근을 줄여주는 엑셀 단축키", "url": "https://instagram.com/p/..." }
      ]
    },
    "spicy": {
      "main_keyword": "#해운대바캉스",
      "related_tags": ["#다이어트자극", "#운동하는여자", "#여름준비"],
      "recommendations": [
        { "title": "올여름 비키니 준비 끝", "url": "https://instagram.com/p/..." }
      ]
    }
  }
}
```

---
> **💡 활용 팁**: 프론트엔드 개발자는 이 Mock Data를 복사하여 백엔드 API가 아직 완성되지 않았을 때에도 UI(네온 뱃지, 추천 링크 카드 등)를 미리 개발하고 테스트할 수 있습니다.
