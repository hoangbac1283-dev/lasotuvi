from fastapi import FastAPI, Request
from pydantic import BaseModel
from google import genai
import os

from lasotuvi.App import lapDiaBan
from lasotuvi.DiaBan import diaBan

app = FastAPI()

# =========================
# GEMINI CLIENT
# =========================
client = genai.Client(api_key="AIzaSyCKnQZdOy7r8uinTeTyoZHfHZdIXD11q2Q")

# =========================
# MODEL INPUT
# =========================
class BirthInput(BaseModel):
    day: int
    month: int
    year: int
    hour: int
    gender: int
    solar: bool
    timezone: int = 7

# =========================
# GENERATE CHART
# =========================
@app.post("/generate-chart")
def generate_chart(data: BirthInput):

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

    for i in range(1, 13):
        cung = db.thapNhiCung[i]
        result[f"cung_{i}"] = {
            "ten": cung.cungTen,
            "sao": cung.cungSao
        }

    return result

# =========================
# CHAT WITH GEMINI
# =========================
@app.post("/chat")
async def chat(request: Request, body: dict):

    message = body.get("message")
    chart_data = body.get("chart_data")

    prompt = f"""
Bạn là chuyên gia tử vi chuyên nghiệp.

Đây là dữ liệu lá số:
{chart_data}

Câu hỏi:
{message}

Hãy trả lời chi tiết, dễ hiểu, chuyên sâu nhưng không quá hàn lâm.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "max_output_tokens": 800
        }
    )

    return {"response": response.text}