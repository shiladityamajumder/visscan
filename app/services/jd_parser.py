# File: app/services/jd_parser.py
# Description: Service for parsing job descriptions using OpenAI's GPT model to extract structured hiring requirements.

import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def parse_jd_with_openai(jd_text: str) -> dict:
    """
    Sends job description text to OpenAI and returns structured fields as a dictionary.
    """
    prompt = f"""
                You are an AI that extracts structured hiring requirements from job descriptions.

                Extract the following fields from the JD:
                - Job Title
                - Years of Experience Required
                - Skills Required
                - Location
                - Employment Type (e.g., Full-time, Contract)
                - Education Requirements
                - Key Responsibilities
                - Preferred Qualifications (if any)
                - Benefits (if mentioned)

                Return the result strictly in JSON format without markdown or explanation.

                Job Description:
                \"\"\"
                {jd_text}
                \"\"\"
            """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.endswith("```"):
        raw = raw[:-3]

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse OpenAI response as JSON: {e}\nRaw:\n{raw}")