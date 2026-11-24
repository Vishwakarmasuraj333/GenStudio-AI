from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_archived: Optional[bool] = None

class ProjectOut(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    job_count: Optional[int] = 0
    asset_count: Optional[int] = 0

    class Config:
        from_attributes = True
