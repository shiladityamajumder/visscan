# File: app/api/api_v1.py
# Description: API router for version 1 of the application, including endpoints for resume parsing, job description processing, and matching.

from fastapi import APIRouter
from app.api.endpoints import resume, jd, match

api_router = APIRouter()
api_router.include_router(resume.router, tags=["Resume Parser"])
api_router.include_router(jd.router, tags=["Job Description"]) 
api_router.include_router(match.router, tags=["Matching"])