from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

class ImageGenRequest(BaseModel):
    prompt: str = Field(..., min_length=2, max_length=4000)
    negative_prompt: Optional[str] = None
    model_id: str = "black-forest-labs/FLUX.1-schnell"
    aspect_ratio: str = "1:1" # "1:1", "16:9", "9:16", "4:3", "3:4"
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    num_outputs: int = Field(default=1, ge=1, le=4)
    seed: Optional[int] = None
    style_preset: Optional[str] = "photorealistic"
    project_id: Optional[str] = None
    enable_prompt_enhancement: bool = False

class VideoGenRequest(BaseModel):
    prompt: str = Field(..., min_length=2, max_length=4000)
    model_id: str = "Lightricks/LTX-Video"
    duration_sec: float = Field(default=5.0, ge=2.0, le=10.0)
    aspect_ratio: str = "16:9" # "16:9", "9:16", "1:1"
    width: Optional[int] = 1280
    height: Optional[int] = 720
    fps: int = 24
    seed: Optional[int] = None
    project_id: Optional[str] = None

class ImageToVideoRequest(BaseModel):
    reference_image_id: str
    prompt: Optional[str] = "smooth cinematic camera motion"
    model_id: str = "Lightricks/LTX-Video"
    duration_sec: float = Field(default=5.0, ge=2.0, le=10.0)
    project_id: Optional[str] = None

class ImageEditRequest(BaseModel):
    base_image_id: str
    prompt: str = Field(..., min_length=2)
    model_id: str = "timbrooks/instruct-pix2pix"
    strength: float = Field(default=0.75, ge=0.1, le=1.0)
    project_id: Optional[str] = None

class PromptEnhanceRequest(BaseModel):
    prompt: str = Field(..., min_length=2)
    style: Optional[str] = "cinematic photorealism"
    target_task: Optional[str] = "text-to-image"

class PromptEnhanceResponse(BaseModel):
    original_prompt: str
    enhanced_prompt: str
    suggested_negative_prompt: Optional[str] = None
    provider: str
    refinements: List[str] = []

class MediaAssetOut(BaseModel):
    id: str
    user_id: str
    project_id: Optional[str] = None
    job_id: Optional[str] = None
    media_type: str
    public_url: str
    mime_type: str
    file_size_bytes: int
    width: Optional[int] = None
    height: Optional[int] = None
    duration_sec: Optional[float] = None
    checksum_sha256: str
    is_favorite: bool
    metadata_json: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True

class GenerationJobOut(BaseModel):
    id: str
    user_id: str
    project_id: Optional[str] = None
    task_type: str
    provider: str
    model_id: str
    prompt: str
    negative_prompt: Optional[str] = None
    parameters: Dict[str, Any] = {}
    status: str
    progress: int
    error_message: Optional[str] = None
    latency_ms: Optional[float] = None
    cost_usd: float = 0.0
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assets: List[MediaAssetOut] = []

    class Config:
        from_attributes = True
