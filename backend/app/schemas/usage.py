from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class UsageRecordOut(BaseModel):
    id: str
    user_id: str
    job_id: Optional[str] = None
    provider: str
    model_id: str
    prompt_tokens: int
    completion_tokens: int
    compute_duration_sec: float
    estimated_cost_usd: float
    created_at: datetime

    class Config:
        from_attributes = True

class UsageSummaryOut(BaseModel):
    total_generations: int
    successful_generations: int
    failed_generations: int
    total_cost_usd: float
    cost_by_provider: dict
    cost_by_model: dict
    generations_by_task: dict
    period_start: datetime
    period_end: datetime
