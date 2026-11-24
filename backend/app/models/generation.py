import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Float, Integer, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class JobStatus(str):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskType(str):
    TEXT_TO_IMAGE = "text-to-image"
    IMAGE_TO_IMAGE = "image-to-image"
    TEXT_TO_VIDEO = "text-to-video"
    IMAGE_TO_VIDEO = "image-to-video"

class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True)
    task_type = Column(String(30), nullable=False, index=True) # text-to-image, etc.
    provider = Column(String(50), nullable=False, index=True) # huggingface, gemini, etc.
    model_id = Column(String(100), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    negative_prompt = Column(Text, nullable=True)
    parameters = Column(JSON, default=dict) # aspect_ratio, seed, steps, cfg, etc.
    status = Column(String(20), default=JobStatus.PENDING, nullable=False, index=True)
    progress = Column(Integer, default=0) # 0 to 100
    error_message = Column(Text, nullable=True)
    latency_ms = Column(Float, nullable=True)
    cost_usd = Column(Float, default=0.0)
    provider_job_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="generation_jobs")
    project = relationship("Project", back_populates="generation_jobs")
    assets = relationship("MediaAsset", back_populates="job", cascade="all, delete-orphan")
    usage_records = relationship("UsageRecord", back_populates="job", cascade="all, delete-orphan")

class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True)
    job_id = Column(String(36), ForeignKey("generation_jobs.id", ondelete="SET NULL"), nullable=True, index=True)
    media_type = Column(String(20), nullable=False, index=True) # image, video
    storage_key = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    public_url = Column(String(500), nullable=False)
    mime_type = Column(String(50), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    duration_sec = Column(Float, nullable=True)
    checksum_sha256 = Column(String(64), nullable=False)
    is_favorite = Column(Boolean, default=False, nullable=False)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="media_assets")
    project = relationship("Project", back_populates="media_assets")
    job = relationship("GenerationJob", back_populates="assets")
