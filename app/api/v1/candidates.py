from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.candidate_service import create_candidate, get_candidates, get_candidate
from app.schemas.candidate import CandidateCreate, CandidateResponse, CandidateSummary
from app.config import settings
import os
import shutil
from datetime import datetime



## CRUD dos candidatos ##

router = APIRouter(prefix="/candidates", tags=["candidates"])

@router.post("/", response_model=CandidateResponse)
async def create_candidate_api(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    education: str = Form(...),
    career_objective: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Garante que o diretório existe
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # 2. Gera nome único para o arquivo
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{resume.filename}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    
    try:
        # 3. Salva o arquivo de forma
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        
        # 4. Cria o objeto para o service
        candidate_data = CandidateCreate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            education=education,
            career_objective=career_objective,
            resume_path=filepath
        )
        
        # 5. Chama o serviço para salvar no banco
        return create_candidate(db, candidate_data)
        
    except Exception as e:
        # Limpeza em caso de erro
        if os.path.exists(filepath):
            os.remove(filepath)
        print(f"Erro detalhado: {e}") # Log para você ver no terminal
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
# Ver todos os candidatos
@router.get("/", response_model=list[CandidateSummary])
def read_candidates(db: Session = Depends(get_db)):
    return get_candidates(db)

# Ver um candidato específico
@router.get("/{candidate_id}", response_model=CandidateResponse)
def read_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return candidate

# Deletar um candidato
@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    
    # Remove o arquivo de currículo
    if os.path.exists(candidate.resume_path):
        os.remove(candidate.resume_path)
    
    db.delete(candidate)
    db.commit()
    return {"detail": "Candidato deletado com sucesso"}