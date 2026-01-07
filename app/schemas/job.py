from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict

class JobCreate(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    status: Optional[str] = "aberta"

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O título não pode estar vazio")
        return v.strip()

class JobResponse(JobCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobSummary(BaseModel):
    id: int
    title: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class JobUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    requirements: Optional[str]
    status: Optional[str]