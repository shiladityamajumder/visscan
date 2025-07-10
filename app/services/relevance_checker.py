# File: app/services/relevance_checker.py
# Description: Service for comparing parsed resumes and job descriptions to compute relevance scores and insights.


from app.utils.similarity_utils import compute_similarity


def compare_resume_and_jd(resume: dict, jd: dict) -> dict:
    """
    Compare parsed resume and job description using semantic similarity
    and return a match score, verdict, and insightful highlights.
    """

    # Extract fields
    resume_skills = set([skill.lower() for skill in resume.get("Skills", [])])
    jd_skills = set([skill.lower() for skill in jd.get("Skills Required", [])])

    overlapping_skills = resume_skills & jd_skills
    missing_skills = jd_skills - resume_skills

    resume_projects = resume.get("Projects", [])
    resume_text = " ".join([
        resume.get("Total Experience Summary", ""),
        " ".join(resume.get("Skills", [])),
        " ".join([p["Description"] if isinstance(p, dict) else str(p) for p in resume_projects]),
    ])

    jd_text = " ".join([
        " ".join(jd.get("Skills Required", [])),
        " ".join(jd.get("Key Responsibilities", [])),
        " ".join(jd.get("Preferred Qualifications", [])),
    ])

    # Compute semantic similarity
    score = compute_similarity(resume_text, jd_text)

    # Verdict logic
    if score >= 0.85:
        verdict = "Highly relevant"
    elif score >= 0.65:
        verdict = "Moderately relevant"
    else:
        verdict = "Low relevance"

    # Experience comparison (basic)
    candidate_exp = resume.get("Years of Experience", "N/A")
    required_exp = jd.get("Years of Experience Required", "N/A")

    highlights = [
        f"Experience: Candidate has {candidate_exp} years vs required {required_exp}",
        f"Skills matched: {len(overlapping_skills)} out of {len(jd_skills)}",
    ]

    if overlapping_skills:
        highlights.append(f"Overlapping skills: {', '.join(sorted(overlapping_skills))}")
    if missing_skills:
        highlights.append(f"Missing skills: {', '.join(sorted(missing_skills))}")

    if len(resume_projects) > 0:
        highlights.append("Resume includes relevant project experience.")
    else:
        highlights.append("No projects listed in resume.")

    # Final output
    return {
        "score": score,
        "verdict": verdict,
        "highlights": highlights
    }
