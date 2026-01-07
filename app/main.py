# app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.api.v1.routes import api_router
from app.database import engine, Base, get_db
from app.models import candidate, job  # ← Importa para criar tabelas
from app.models.candidate import Candidate
from app.models.job import JobOpening
from sqlalchemy.orm import Session
from fastapi import Depends

# Cria tabelas (só em desenvolvimento)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Banco de Talentos RH", version="1.0.0")

# Monta pastas estáticas
templates = Jinja2Templates(directory="app/templates")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Inclui rotas da API
app.include_router(api_router, prefix="/api/v1")

# =============== ROTAS FRONTEND ===============
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    from app.services.candidate_service import get_candidates
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        candidates = get_candidates(db)
        return templates.TemplateResponse("index.html", {"request": request, "candidates": candidates})
    finally:
        db.close()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # Contagens simples
    total_candidates = db.query(Candidate).count()
    total_jobs = db.query(JobOpening).count()
    
    # Contagem por status de vaga
    jobs_open = db.query(JobOpening).filter(JobOpening.status == "aberta").count()
    jobs_analysis = db.query(JobOpening).filter(JobOpening.status == "em análise").count()
    jobs_closed = db.query(JobOpening).filter(JobOpening.status == "fechada").count()

    # Dados para o gráfico (Últimos 6 meses - exemplo simplificado)
    # Em um projeto real, você faria uma query de agrupamento por data
    
    metrics = {
        "total_candidates": total_candidates,
        "total_jobs": total_jobs,
        "jobs_open": jobs_open,
        "jobs_analysis": jobs_analysis,
        "jobs_closed": jobs_closed
    }

    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "metrics": metrics
    })

@app.get("/candidates/new", response_class=HTMLResponse)
async def new_candidate_form(request: Request):
    return templates.TemplateResponse("candidate_form.html", {"request": request})

@app.get("/jobs", response_class=HTMLResponse)
async def jobs_list(request: Request):
    from app.services.job_service import get_jobs
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        jobs = get_jobs(db)
        return templates.TemplateResponse("jobs_list.html", {"request": request, "jobs": jobs})
    finally:
        db.close()

@app.get("/jobs/new", response_class=HTMLResponse)
async def new_job_form(request: Request):
    return templates.TemplateResponse("job_form.html", {"request": request})

@app.get("/jobs/{job_id}", response_class=HTMLResponse)
async def job_detail(request: Request, job_id: int):
    from app.services.job_service import get_job, get_job_matches
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        job = get_job(db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Vaga não encontrada")
        matches = get_job_matches(db, job_id)
        return templates.TemplateResponse("job_detail.html", {"request": request, "job": job, "matches": matches})
    finally:
        db.close()

@app.get("/jobs/{job_id}/edit", response_class=HTMLResponse)
async def edit_job_form(request: Request, job_id: int):
    from app.services.job_service import get_job
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        job = get_job(db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Vaga não encontrada")
        return templates.TemplateResponse("job_edit_form.html", {"request": request, "job": job})
    finally:
        db.close()

@app.get("/resume/{candidate_id}")
async def get_resume(candidate_id: int):
    from app.services.candidate_service import get_candidate
    from app.database import SessionLocal
    from fastapi.responses import FileResponse
    import mimetypes
    from pathlib import Path
    
    db = SessionLocal()
    try:
        candidate = get_candidate(db, candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidato não encontrado")
        
        resume_path = Path(candidate.resume_path)
        if not resume_path.is_file():
            raise HTTPException(status_code=404, detail="Currículo não encontrado")
        
        media_type, _ = mimetypes.guess_type(str(resume_path))
        media_type = media_type or "application/octet-stream"
        
        return FileResponse(
            path=resume_path,
            filename=resume_path.name,
            media_type=media_type,
            headers={"Content-Disposition": f"inline; filename*=UTF-8''{resume_path.name}"}
        )   
    finally:
        db.close()

@app.get("/api/candidates/{candidate_id}", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})