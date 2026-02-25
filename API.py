from fastapi import FastAPI
from pydantic import BaseModel

from lasotuvi.App import lapDiaBan
from lasotuvi.DiaBan import diaBan

app = FastAPI()


class BirthInput(BaseModel):
    day: int
    month: int
    year: int
    hour: int
    gender: int
    solar: bool
    timezone: int = 7


@app.post("/generate-chart")
def generate_chart(data: BirthInput):

    # Tạo địa bàn
    db = lapDiaBan(
        diaBan,
        data.day,
        data.month,
        data.year,
        data.hour,
        data.gender,
        data.solar,
        data.timezone
    )

    result = {}

    # Lặp 12 cung (bỏ index 0 vì list tạo từ 0–12)
    for i in range(1, 13):
        cung = db.thapNhiCung[i]

        result[f"cung_{i}"] = {
            "ten": cung.cungTen,
            "sao": cung.cungSao
        }

    return result
import google.generativeai as genai
import os
from fastapi import Request

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

@app.post("/chat")
async def chat(request: Request, body: dict):
    message = body.get("message")
    chart_data = body.get("chart_data")

    prompt = f"""
    Bạn là chuyên gia tử vi.
    Đây là dữ liệu lá số: {chart_data}
    Câu hỏi của người dùng: {message}
    Hãy trả lời chi tiết nhưng dễ hiểu.
    """

    response = model.generate_content(prompt)

    return {"response": response.text}