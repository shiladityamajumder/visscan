# File: app/api/endpoints/match.py
# Description: API endpoint for matching resumes to job descriptions using relevance checking.


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.services.relevance_checker import compare_resume_and_jd

router = APIRouter()


class MatchRequest(BaseModel):
    resume: Dict[str, Any]
    jd: Dict[str, Any]


@router.post("/match")
async def match_resume_to_jd(payload: MatchRequest):
    try:
        result = compare_resume_and_jd(payload.resume, payload.jd)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing relevance: {str(e)}")

    return {
        "status": "success",
        "message": "Relevance computed",
        "code": 200,
        "data": result
    }
