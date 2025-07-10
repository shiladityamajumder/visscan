# VisScan 🔍

**VisScan** is a FastAPI-based resume analysis and job matching API that leverages OCR, face detection, OpenAI's language model, and semantic similarity techniques to intelligently parse resumes and job descriptions, then score relevance between them.

---

## ✨ Objective

To automate and improve resume screening by:

* Extracting structured data from resumes in **PDF**, **DOCX**, and **image** formats
* Parsing **job descriptions** from raw text
* Matching resume content to job criteria using **semantic similarity (SentenceTransformers)**

This allows recruiters to:

* Quickly extract candidate insights
* Score candidate-job relevance with AI
* Save time on manual resume filtering

---

## 🌐 API Endpoints

### 1. **Parse Resume (Upload)**

**`POST /api/v1/resume/parse`**

Upload a resume file (PDF, DOCX, JPG, PNG) and get structured data using OpenAI.

#### Request (multipart/form-data):

```http
file=<UploadFile>
```

#### Response:

```json
{
  "status": "success",
  "message": "Resume parsed successfully",
  "code": 200,
  "data": {
    "Full Name": "...",
    "Email": "...",
    "Phone Number": "...",
    "Skills": ["Python", "Django", ...],
    "Projects": [ { "Name": "...", "Description": "..." }, ... ]
  }
}
```

---

### 2. **Parse Job Description (Text Input)**

**`POST /api/v1/jd/parse`**

Submit plain JD text in a JSON payload. Returns structured job role, skills, experience, etc.

#### Request (JSON):

```json
{
  "text": "We are hiring a Python Developer with 4+ years experience in FastAPI, Docker..."
}
```

#### Response:

```json
{
  "status": "success",
  "message": "Job description parsed successfully",
  "code": 200,
  "data": {
    "Job Title": "Python Developer",
    "Skills Required": ["FastAPI", "Docker", ...],
    "Years of Experience Required": "4-5 years"
  }
}
```

---

### 3. **Match Resume & Job Description**

**`POST /api/v1/match`**

Compares resume and JD (already parsed JSONs) to determine relevance using semantic embeddings.

#### Request (JSON):

```json
{
  "resume": { ... },
  "jd": { ... }
}
```

#### Response:

```json
{
  "status": "success",
  "message": "Relevance computed",
  "code": 200,
  "data": {
    "score": 0.78,
    "verdict": "Moderately relevant",
    "highlights": [
      "Experience match: 4 vs 4-5 years",
      "Skills matched: 6 out of 12",
      "Overlapping skills: python, django, docker"
    ]
  }
}
```

---

## 📁 Project Structure

```
VisScan/
├── app/                             # Core application logic
│   ├── __init__.py                  # Makes 'app' a package (important for imports)
│
│   ├── api/                         # API route definitions
│   │   ├── __init__.py
│   │   ├── api_v1.py                # Combines all API routers (v1)
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── resume.py            # POST /resume/parse - parse CV from file (PDF, DOCX, image)
│   │       ├── jd.py                # POST /jd/parse - parse job description from text input
│   │       └── match.py             # POST /match - compare parsed resume and JD (semantic match)
│
│   ├── core/                        # Configs, logging
│   │   ├── __init__.py
│   │   ├── config.py                # App/env settings using Pydantic
│   │   └── logger.py                # Logger setup for structured logs
│
│   ├── models/                      # Request/response schemas
│   │   ├── __init__.py
│   │   └── schemas.py               # Pydantic models (input/output format)
│
│   ├── services/                    # Business logic
│   │   ├── __init__.py
│   │   ├── resume_parser.py         # Coordinates OCR + section extraction + OpenAI parsing
│   │   ├── face_detector.py         # Detects/validates face in resume image
│   │   ├── jd_parser.py             # Parses job description text using OpenAI
│   │   └── relevance_checker.py     # Compares resume and JD using semantic search
│
│   ├── utils/                       # Helper utilities
│   │   ├── __init__.py
│   │   ├── file_utils.py            # Handle uploads, file validation
│   │   ├── ocr_utils.py             # OCR wrapper (EasyOCR/Tesseract)
│   │   ├── nlp_utils.py             # Extract name, email, skills from text
│   │   ├── section_checker.py       # Check if required sections are present
│   │   └── similarity_utils.py      # Semantic vector encoding + cosine similarity (using MiniLM)
│
│   ├── constants/                   # Shared constants
│   │   ├── __init__.py
│   │   └── constants.py             # Keywords, regex patterns, section list
│
│   ├── exceptions/                  # Custom error handling
│   │   ├── __init__.py
│   │   └── handlers.py              # Global exception handlers for validation and HTTP errors
│
├── tests/                           # Unit + integration tests
│   └── test_resume.py               # Tests for resume parsing logic
│
├── main.py                          # FastAPI app entrypoint, CORS setup, exception wiring
├── README.md                        # Project overview and documentation
├── requirements.txt                 # Python dependencies (OpenAI, FastAPI, SentenceTransformers, etc.)
├── Dockerfile                       # Docker container config (if needed for deployment)
```

---

## ⚖️ Tech Stack

* **FastAPI** for API layer
* **OpenAI GPT-4o** for parsing resumes and JDs
* **pdfplumber**, **docx2txt**, **PIL**, **easyocr** for file handling
* **sentence-transformers** (`all-MiniLM-L6-v2`) for semantic similarity
* **Pydantic** for models

---

## ⚡ Setup Instructions

```bash
git clone https://github.com/your-username/VisScan.git
cd VisScan
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Set OpenAI Key:**

```bash
export OPENAI_API_KEY=your-key-here
```

**Run the app:**

```bash
uvicorn main:app --reload
```

---

## 🚀 Coming Soon

* Frontend dashboard (React/Vue)
* Candidate ranking across multiple JDs
* Support for bulk resume uploads

---

## ✉️ Author

**Shiladitya Majumder**
Backend Developer | AI Integrator
[LinkedIn](https://www.linkedin.com/in/shiladitya-majumder/) | [GitHub](https://github.com/shiladityamajumder)

---

## ⚖ License

MIT