import re
from typing import List
from app.models.candidate import Candidate
from app.models.job import JobOpening

def extract_keywords(text: str) -> set:
    if not text:
        return set()
    
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    stopwords = {
        'a', 'o', 'e', 'de', 'do', 'da', 'em', 'para', 'com', 'por', 'ao', 'as', 'os',
        'um', 'uma', 'uns', 'umas', 'no', 'na', 'nos', 'nas', 'que', 'é', 'são',
        'ser', 'ter', 'atuar', 'como', 'em', 'na', 'no', 'pelo', 'pela'
    }
    words = text.split()
    return {word for word in words if len(word) > 2 and word not in stopwords}

def calculate_compatibility(candidate: Candidate, job: JobOpening) -> float:
    cand_kw = extract_keywords(candidate.career_objective)
    job_kw = extract_keywords(job.requirements or "") | extract_keywords(job.description)
    
    if not job_kw:
        return 0.0
    
    common = cand_kw & job_kw
    score = len(common) / len(job_kw)
    
    # Bônus se palavra do título está no objetivo
    title_kw = extract_keywords(job.title)
    if title_kw & cand_kw:
        score = min(1.0, score + 0.2)
    
    return round(score, 2)