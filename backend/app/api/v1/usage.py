from datetime import datetime, timezone, timedelta
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.generation import GenerationJob
from app.models.audit import UsageRecord
from app.schemas.usage import UsageRecordOut, UsageSummaryOut

router = APIRouter()

@router.get("/summary", response_model=UsageSummaryOut)
def get_usage_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    now = datetime.now(timezone.utc)
    start_period = now - timedelta(days=30)

    jobs = db.query(GenerationJob).filter(
        GenerationJob.user_id == current_user.id,
        GenerationJob.created_at >= start_period
    ).all()

    total = len(jobs)
    successful = len([j for j in jobs if j.status == "completed"])
    failed = len([j for j in jobs if j.status == "failed"])
    total_cost = sum([j.cost_usd or 0.0 for j in jobs])

    cost_by_provider = {}
    cost_by_model = {}
    gens_by_task = {}

    for j in jobs:
        cost_by_provider[j.provider] = round(cost_by_provider.get(j.provider, 0.0) + (j.cost_usd or 0.0), 5)
        cost_by_model[j.model_id] = round(cost_by_model.get(j.model_id, 0.0) + (j.cost_usd or 0.0), 5)
        gens_by_task[j.task_type] = gens_by_task.get(j.task_type, 0) + 1

    return UsageSummaryOut(
        total_generations=total,
        successful_generations=successful,
        failed_generations=failed,
        total_cost_usd=round(total_cost, 4),
        cost_by_provider=cost_by_provider,
        cost_by_model=cost_by_model,
        generations_by_task=gens_by_task,
        period_start=start_period,
        period_end=now
    )

@router.get("/records", response_model=List[UsageRecordOut])
def get_usage_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    records = db.query(UsageRecord).filter(
        UsageRecord.user_id == current_user.id
    ).order_by(UsageRecord.created_at.desc()).limit(50).all()
    return records
