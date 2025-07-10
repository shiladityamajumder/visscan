# File: app/services/resume_parser.py
# Description: Service for parsing resumes using OpenAI's GPT model to extract structured resume data.


from openai import OpenAI
from app.core.config import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def parse_resume_with_openai(resume_text: str) -> dict:
    """
    Sends resume text to OpenAI and returns extracted structured data in JSON.
    """
    prompt = f"""
                Extract the following fields from the resume below:
                - Full Name
                - Email
                - Phone Number
                - Years of Experience
                - Total Experience Summary
                - Skills
                - Certifications
                - Degrees and Institutions
                - Companies Worked At
                - Job Titles Held
                - Start and End Years of Each Role (if available)
                - Projects (if mentioned)

                Return the data in JSON format.

                Resume:
                \"\"\"
                {resume_text}
                \"\"\"
            """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw_text = response.choices[0].message.content.strip()

    # Remove ```json code block if present
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]

    try:
        parsed_data = json.loads(raw_text)
        return parsed_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse OpenAI response as JSON: {e}\nRaw:\n{raw_text}")
