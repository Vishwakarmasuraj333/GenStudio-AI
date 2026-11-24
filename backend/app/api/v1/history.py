from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.generation import GenerationJob
from app.schemas.generation import GenerationJobOut

router = APIRouter()

@router.get("/", response_model=List[GenerationJobOut])
def list_generation_history(
    task_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(GenerationJob).filter(GenerationJob.user_id == current_user.id)
    if task_type:
        query = query.filter(GenerationJob.task_type == task_type)
    if status:
        query = query.filter(GenerationJob.status == status)

    jobs = query.order_by(GenerationJob.created_at.desc()).offset(offset).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=GenerationJobOut)
def get_history_detail(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id,
        GenerationJob.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Generation job record not found.")
    return job
