from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class ModelInfoOut(BaseModel):
    id: str
    provider: str
    model_id: str
    display_name: str
    version: Optional[str] = None
    task_types: List[str]
    max_resolution: str
    supported_aspect_ratios: List[str]
    capabilities_json: Dict[str, Any]
    pricing_json: Dict[str, Any]
    license_info: str
    is_enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ModelFilter(BaseModel):
    task_type: Optional[str] = None
    provider: Optional[str] = None
    is_enabled: Optional[bool] = True
