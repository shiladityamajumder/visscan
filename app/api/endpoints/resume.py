# File: app/api/endpoints/resume.py
# Description: API endpoint for parsing resumes using OpenAI's GPT model.


from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_utils import extract_text_from_file
from app.services.resume_parser import parse_resume_with_openai

router = APIRouter()

@router.post("/resume/parse")
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse uploaded resume file and return structured resume data using OpenAI.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    resume_text = await extract_text_from_file(file)  # ✅ MUST await
    parsed_json = parse_resume_with_openai(resume_text)

    return {
        "status": "success",
        "message": "Resume parsed successfully",
        "code": 200,
        "data": parsed_json
    }