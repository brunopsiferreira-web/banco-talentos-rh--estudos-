from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict

class CandidateCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    education: str
    career_objective: str
    resume_path: str

    @field_validator("first_name", "last_name")
    @classmethod
    def name_not_empty(cls, name: str) -> str:
        if not name.strip():
            raise ValueError("Não pode estar vazio")
        return name.strip().title()

class CandidateResponse(CandidateCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CandidateSummary(BaseModel):
    id: int
    first_name: str
    career_objective: str
    resume_path: str

    model_config = ConfigDict(from_attributes=True)