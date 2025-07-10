# File: app/utils/file_utils.py
# Description: Utility functions for extracting text from various file types (PDF, DOCX, DOC, images) using appropriate libraries.

import os
import tempfile
from pathlib import Path
from typing import Union
from fastapi import UploadFile, HTTPException

from io import BytesIO
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import docx
import textract


async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extract text from PDF using PyMuPDF (fitz). Robust for all types of PDFs.
    """
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(contents)
        temp.flush()
        temp.close()
        try:
            with fitz.open(temp.name) as doc:
                return "\n".join([page.get_text() for page in doc])
        finally:
            os.remove(temp.name)


async def extract_text_from_docx(file: UploadFile) -> str:
    """
    Extract text from DOCX using python-docx.
    """
    contents = await file.read()
    document = docx.Document(BytesIO(contents))
    return "\n".join([para.text for para in document.paragraphs])


async def extract_text_from_doc(file: UploadFile) -> str:
    """
    Extract text from legacy DOC using textract.
    """
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        temp.flush()
        temp.close()
        try:
            text = textract.process(temp.name).decode("utf-8")
            return text
        finally:
            os.remove(temp.name)


async def extract_text_from_image(file: UploadFile) -> str:
    """
    Extract text from image using pytesseract.
    """
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    return pytesseract.image_to_string(image)


async def extract_text_from_file(file: UploadFile) -> str:
    """
    Determine file type and extract text accordingly.
    Raises HTTPException on unsupported or failed files.
    """
    filename = file.filename.lower()
    try:
        if filename.endswith(".pdf"):
            return await extract_text_from_pdf(file)
        elif filename.endswith(".docx"):
            return await extract_text_from_docx(file)
        elif filename.endswith(".doc"):
            return await extract_text_from_doc(file)
        elif filename.endswith((".jpg", ".jpeg", ".png")):
            return await extract_text_from_image(file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")
