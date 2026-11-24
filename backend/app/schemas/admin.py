from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr

class AdminUserUpdate(BaseModel):
    role: Optional[str] = None
    is_active: Optional[bool] = None

class AuditLogOut(BaseModel):
    id: str
    user_id: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details_json: Dict[str, Any] = {}
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SystemHealthOut(BaseModel):
    status: str
    version: str
    database: str
    storage_accessible: bool
    active_providers: Dict[str, bool]
    pending_jobs_count: int
    uptime_seconds: float
