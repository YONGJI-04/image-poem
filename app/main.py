import base64
import os
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = FastAPI(title="Image Poem API")
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
STYLES = {"haiku": "하이쿠 (5-7-5 음절)", "free": "자유시", "sonnet": "소네트"}


@app.get("/")
def root():
    return {"status": "running", "message": "Image Poem API"}


@app.post("/generate")
async def generate_poem(
    file: UploadFile = File(...),
    style: str = Query(default="free", description="haiku / free / sonnet"),
    language: str = Query(default="ko", description="ko / en"),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="JPG, PNG, GIF, WEBP만 지원합니다")

    image_bytes = await file.read()
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

    style_desc = STYLES.get(style, "자유시")
    lang_instruction = "한국어로" if language == "ko" else "in English"

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": file.content_type, "data": image_data},
                },
                {
                    "type": "text",
                    "text": f"이 이미지를 보고 영감을 받아 {style_desc} 형식으로 {lang_instruction} 시를 써주세요. 시만 출력해주세요."
                },
            ],
        }]
    )

    return JSONResponse(content={
        "style": style,
        "language": language,
        "poem": message.content[0].text,
    })
