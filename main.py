"""
main.py

Entry point for the VisuScan FastAPI application.
Initializes the app, sets up routing, CORS, and exception handlers.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.api.api_v1 import api_router
from app.exceptions import handlers as exception_handlers  # custom handlers

# Initialize FastAPI app instance
app = FastAPI(
    title="VisScan - Resume Analysis API",
    description="OCR + Face Validation + NLP resume parser",
    version="1.0.0"
)

# Allow frontend / external calls (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include versioned API router
app.include_router(api_router, prefix="/api/v1")

# Register global error handlers
app.add_exception_handler(HTTPException, exception_handlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, exception_handlers.validation_exception_handler)
app.add_exception_handler(Exception, exception_handlers.generic_exception_handler)

# Health check endpoint
@app.get("/", tags=["Health"])
def root():
    return {"message": "VisuScan API is running successfully!"}
