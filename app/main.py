import os
import base64
import anthropic
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

app = FastAPI(title="Image Poem API", description="이미지를 보고 시를 창작합니다", version="1.1.0")

STYLE_PROMPTS = {
    "haiku": lambda lang, lines: f"이미지를 보고 {'한국어' if lang=='ko' else 'English'} 하이쿠를 작성해주세요 (5-7-5 음절). 제목도 붙여주세요.",
    "free": lambda lang, lines: f"이미지에서 영감받아 {'한국어' if lang=='ko' else 'English'} 자유시를 작성해주세요. {lines}행 내외로 작성하세요. 제목도 붙여주세요.",
    "sonnet": lambda lang, lines: f"이미지를 보고 {'한국어' if lang=='ko' else 'English'} 소네트 형식의 시를 작성해주세요. 14행으로 구성해주세요. 제목도 붙여주세요.",
    "lyric": lambda lang, lines: f"이미지에서 영감받아 {'한국어' if lang=='ko' else 'English'} 노래 가사 형식의 시를 작성해주세요 (verse-chorus-verse). {lines}행 내외. 제목도 붙여주세요.",
}

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

@app.get("/")
def root():
    return {"status": "running", "message": "Image Poem API - Claude Vision"}

@app.post("/generate")
async def generate_poem(
    file: UploadFile = File(...),
    style: Literal["haiku", "free", "sonnet", "lyric"] = Query("free"),
    language: Literal["ko", "en"] = Query("ko"),
    lines: int = Query(12, ge=4, le=30),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다")
    contents = await file.read()
    b64 = base64.standard_b64encode(contents).decode("utf-8")
    prompt_fn = STYLE_PROMPTS.get(style, STYLE_PROMPTS["free"])
    prompt = prompt_fn(language, lines)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": file.content_type, "data": b64}},
            {"type": "text", "text": prompt}
        ]}]
    )
    return {"style": style, "language": language, "lines": lines, "poem": response.content[0].text}

@app.get("/styles")
def get_styles():
    return {"styles": ["haiku", "free", "sonnet", "lyric"]}
