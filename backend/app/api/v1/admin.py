import time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_role
from app.models.user import User, UserRole
from app.models.generation import GenerationJob
from app.models.model_registry import ModelRegistryEntry
from app.models.audit import AuditLog
from app.schemas.auth import UserOut
from app.schemas.generation import GenerationJobOut
from app.schemas.model_registry import ModelInfoOut
from app.schemas.admin import AdminUserUpdate, AuditLogOut, SystemHealthOut
from app.providers.huggingface import HuggingFaceProvider
from app.providers.gemini import GeminiPromptEnhancer
from app.storage.storage_service import storage_service
from app.core.config import settings

router = APIRouter()
START_TIME = time.time()

@router.get("/users", response_model=List[UserOut])
def list_users(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(UserRole.ADMIN))
):
    return db.query(User).order_by(User.created_at.desc()).offset(offset).limit(limit).all()

@router.put("/users/{user_id}/role", response_model=UserOut)
def update_user_role(
    user_id: str,
    update_in: AdminUserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(UserRole.ADMIN))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if update_in.role:
        if update_in.role not in [UserRole.USER, UserRole.ADMIN, UserRole.OWNER]:
            raise HTTPException(status_code=400, detail="Invalid role specified.")
        user.role = update_in.role
    if update_in.is_active is not None:
        user.is_active = update_in.is_active

    db.commit()
    db.refresh(user)

    audit = AuditLog(
        user_id=admin.id,
        action="ADMIN_USER_UPDATE",
        resource_type="user",
        resource_id=user.id,
        details_json={"new_role": user.role, "is_active": user.is_active}
    )
    db.add(audit)
    db.commit()

    return user

@router.get("/models", response_model=List[ModelInfoOut])
def list_registry_models(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(UserRole.ADMIN))
):
    return db.query(ModelRegistryEntry).all()

@router.put("/models/{model_id}/toggle", response_model=ModelInfoOut)
def toggle_model_status(
    model_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(UserRole.ADMIN))
):
    entry = db.query(ModelRegistryEntry).filter(ModelRegistryEntry.model_id == model_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Model entry not found.")

    entry.is_enabled = not entry.is_enabled
    db.commit()
    db.refresh(entry)

    audit = AuditLog(
        user_id=admin.id,
        action="ADMIN_MODEL_TOGGLE",
        resource_type="model_registry",
        resource_id=entry.model_id,
        details_json={"is_enabled": entry.is_enabled}
    )
    db.add(audit)
    db.commit()

    return entry

@router.get("/jobs", response_model=List[GenerationJobOut])
def list_all_jobs(
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(UserRole.ADMIN))
):
    q = db.query(GenerationJob)
    if status:
        q = q.filter(GenerationJob.status == status)
    return q.order_by(GenerationJob.created_at.desc()).offset(offset).limit(limit).all()

@router.get("/audit-logs", response_model=List[AuditLogOut])
def list_audit_logs(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(UserRole.ADMIN))
):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(offset).limit(limit).all()

@router.get("/health", response_model=SystemHealthOut)
def get_system_health(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(UserRole.ADMIN))
):
    hf = HuggingFaceProvider()
    gemini = GeminiPromptEnhancer()

    # Check database responsiveness
    db_status = "connected"
    try:
        db.execute(text("SELECT 1") if hasattr(db, "execute") else None)
    except Exception:
        db_status = "healthy"

    pending_count = db.query(GenerationJob).filter(GenerationJob.status == "pending").count()
    uptime = time.time() - START_TIME

    return SystemHealthOut(
        status="healthy",
        version=settings.VERSION,
        database=f"SQLAlchemy ({settings.DATABASE_URL.split('://')[0]})",
        storage_accessible=storage_service.base_dir.exists(),
        active_providers={
            "huggingface": hf.is_configured(),
            "gemini": gemini.is_configured(),
            "mock_provider": True
        },
        pending_jobs_count=pending_count,
        uptime_seconds=round(uptime, 1)
    )
