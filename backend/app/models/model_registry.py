import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class ModelRegistryEntry(Base):
    __tablename__ = "model_registry"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    provider = Column(String(50), nullable=False, index=True) # huggingface, google, comfyui, local
    model_id = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    version = Column(String(30), nullable=True)
    task_types = Column(JSON, nullable=False) # list of tasks e.g. ["text-to-image"]
    max_resolution = Column(String(20), default="1024x1024")
    supported_aspect_ratios = Column(JSON, default=list) # ["1:1", "16:9", "9:16"]
    capabilities_json = Column(JSON, default=dict) # supports_seed, supports_negative_prompt, etc.
    pricing_json = Column(JSON, default=dict) # cost_per_gen_usd, tier, checked_at
    license_info = Column(String(100), default="Open / Permissive")
    is_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
