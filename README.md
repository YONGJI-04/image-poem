# Image Poem

이미지를 업로드하면 **Claude Vision**이 이미지에서 영감을 받아 시를 창작해주는 API

---

## 프로젝트 개요

시각 예술과 언어 예술을 연결하는 프로젝트입니다. Claude Vision이 이미지의 분위기, 색감, 구성 요소를 감성적으로 해석하여 하이쿠, 자유시, 소네트 형식의 시를 창작합니다.

---

## 아키텍처

```
이미지 파일 업로드 + 시 스타일 선택
            ↓
    Base64 인코딩
            ↓
    [ Claude Vision API ]
    claude-sonnet-4-6
    이미지 감성적 해석 + 시 창작
            ↓
    선택한 형식의 시 반환 (한국어/영어)
```

---

## 지원 시 스타일

| 스타일 파라미터 | 형식 | 설명 |
|----------------|------|------|
| `haiku` | 하이쿠 | 5-7-5 음절 구조의 일본 전통 시 형식 |
| `free` | 자유시 | 형식 제약 없는 현대 자유시 (기본값) |
| `sonnet` | 소네트 | 14행 구조의 서양 고전 시 형식 |

---

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 서버 상태 확인 |
| `POST` | `/generate` | 이미지 → 시 생성 |
| `GET` | `/docs` | Swagger UI |

---

## 요청 / 응답 예시

```bash
# 하이쿠 (한국어)
curl -X POST "http://localhost:8000/generate?style=haiku&language=ko" \
  -F "file=@sunset.jpg"

# 자유시 (영어)
curl -X POST "http://localhost:8000/generate?style=free&language=en" \
  -F "file=@city.jpg"
```

**응답 (하이쿠):**

```json
{
  "style": "haiku",
  "language": "ko",
  "poem": "붉은 노을이\n바다를 물들이며\n하루가 저문다"
}
```

---

## 지원 형식

- **파일 형식**: JPG, PNG, GIF, WEBP
- **언어**: `ko` (한국어), `en` (영어)

---

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8005
```

## 환경 변수

| 변수 | 설명 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API 키 |
