from fastapi import APIRouter
from . import candidates, jobs

api_router = APIRouter()
api_router.include_router(candidates.router)
api_router.include_router(jobs.router)