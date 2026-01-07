from sqlalchemy.orm import Session
from app.models.job import JobOpening
from app.schemas.job import JobCreate
from app.models.candidate import Candidate
from app.services.matching import calculate_compatibility

def create_job(db: Session, job: JobCreate) -> JobOpening:
    db_job = JobOpening(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session):
    return db.query(JobOpening).all()

def get_job(db: Session, job_id: int):
    return db.query(JobOpening).filter(JobOpening.id == job_id).first()

def get_job_matches(db: Session, job_id: int):
    job = get_job(db, job_id)
    if not job:
        return []
    
    candidates = db.query(Candidate).all()
    matches = []
    for cand in candidates:
        score = calculate_compatibility(cand, job)
        if score > 0:
            matches.append({
                "candidate_id": cand.id,
                "first_name": cand.first_name,
                "career_objective": cand.career_objective[:100] + "..." if len(cand.career_objective) > 100 else cand.career_objective,
                "compatibility_score": score
            })
    return sorted(matches, key=lambda x: x["compatibility_score"], reverse=True)

def uptate_job(db: Session, job_id: int, job_data: JobCreate):
    job = get_job(db, job_id)
    if not job:
        return None
    for key, value in job_data.model_dump().items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job