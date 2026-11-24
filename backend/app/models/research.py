import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Float, Integer, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    dataset_name = Column(String(100), default="GenStudio-Bench-v1", nullable=False)
    prompt_count = Column(Integer, default=0)
    target_models = Column(JSON, default=list) # ["black-forest-labs/FLUX.1-schnell", "stabilityai/stable-diffusion-xl-base-1.0"]
    status = Column(String(20), default="pending", nullable=False) # pending, running, completed, failed
    summary_metrics = Column(JSON, default=dict) # aggregate stats per model
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    results = relationship("EvaluationResult", back_populates="run", cascade="all, delete-orphan")

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    run_id = Column(String(36), ForeignKey("evaluation_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    prompt_id = Column(String(50), nullable=False)
    prompt_text = Column(Text, nullable=False)
    prompt_category = Column(String(50), nullable=False, index=True) # photorealism, artistic, cinematic, typography, etc.
    model_id = Column(String(100), nullable=False, index=True)
    latency_ms = Column(Float, nullable=False)
    cost_usd = Column(Float, default=0.0)
    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)
    output_asset_id = Column(String(36), nullable=True)
    
    # Research Metrics
    human_score_quality = Column(Float, nullable=True) # 1.0 - 5.0
    human_score_alignment = Column(Float, nullable=True) # 1.0 - 5.0
    sim_score = Column(Float, nullable=True) # CLIP similarity score (0.0 - 1.0)
    temporal_score = Column(Float, nullable=True) # Video temporal consistency metric (0.0 - 1.0)
    raw_metrics_json = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    run = relationship("EvaluationRun", back_populates="results")

class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(String(36), ForeignKey("generation_jobs.id", ondelete="SET NULL"), nullable=True, index=True)
    asset_id = Column(String(36), ForeignKey("media_assets.id", ondelete="SET NULL"), nullable=True, index=True)
    rating = Column(Integer, nullable=False) # 1 to 5
    feedback_text = Column(Text, nullable=True)
    tags = Column(JSON, default=list) # ["high_detail", "anatomy_flaw", "prompt_adherent"]
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
