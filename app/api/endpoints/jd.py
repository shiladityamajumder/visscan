# File: app/api/endpoints/jd.py
# Description: API endpoint for parsing job descriptions using OpenAI's GPT model.


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.jd_parser import parse_jd_with_openai

router = APIRouter()


class JDRequest(BaseModel):
    text: str


@router.post("/jd/parse")
async def parse_job_description(payload: JDRequest):
    """
    Parse raw job description text and extract structured hiring requirements.
    """
    jd_text = payload.text.strip()

    if not jd_text:
        raise HTTPException(status_code=400, detail="Job description text is empty")

    try:
        structured_data = parse_jd_with_openai(jd_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "message": "Job description parsed successfully",
        "code": 200,
        "data": structured_data
    }
