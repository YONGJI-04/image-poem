# Image Poem

이미지를 업로드하면 Claude Vision이 영감을 받아 시를 작성해주는 API

## 아키텍처

```
이미지 파일 업로드
        ↓
Claude Vision (claude-sonnet-4-6)
        ↓
선택한 스타일로 시 작성 (한국어/영어)
```

## 지원 시 스타일

| 스타일 | 설명 |
|--------|------|
| `haiku` | 하이쿠 (5-7-5 음절) |
| `free` | 자유시 (기본값) |
| `sonnet` | 소네트 형식 |

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 서버 상태 확인 |
| POST | `/generate` | 이미지 → 시 생성 |
| GET | `/docs` | Swagger UI |

## 요청 예시

```bash
curl -X POST "http://localhost:8000/generate?style=haiku&language=ko" \
  -F "file=@sunset.jpg"
```

## 응답 예시

```json
{
  "style": "haiku",
  "language": "ko",
  "poem": "붉은 노을이\n바다를 물들이며\n하루가 저문다"
}
```

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8005
```

## 환경 변수

```
ANTHROPIC_API_KEY=   # Anthropic Claude API 키
```
