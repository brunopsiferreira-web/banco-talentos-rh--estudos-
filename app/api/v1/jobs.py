from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.job_service import create_job, get_jobs, get_job, get_job_matches
from app.schemas.job import JobCreate, JobResponse, JobSummary
from app.services.job_service import uptate_job

## CRUD de Vagas ##
router = APIRouter(prefix="/jobs", tags=["jobs"])

# Criar uma nova vaga
@router.post("/", response_model=JobResponse)
def create_job_api(job: JobCreate, db: Session = Depends(get_db)):
    return create_job(db, job)

# Ver todas as vagas
@router.get("/", response_model=list[JobSummary])
def read_jobs(db: Session = Depends(get_db)):
    return get_jobs(db)

# Ver uma vaga específica
@router.get("/{job_id}", response_model=JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return job
# Ver candidatos correspondentes a uma vaga
@router.get("/{job_id}/matches")
def read_job_matches(job_id: int, db: Session = Depends(get_db)):
    return get_job_matches(db, job_id)

# Atualizar uma vaga
@router.put("/{job_id}", response_model=JobResponse)
def update_job_api(job_id: int, job_data: JobCreate, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    updated_job = uptate_job(db, job_id, job_data)
    return updated_job

# Deletar uma vaga
@router.delete("/{job_id}")
def delete_job_api(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    db.delete(job)
    db.commit()
    return {"detail": "Vaga deletada com sucesso"}