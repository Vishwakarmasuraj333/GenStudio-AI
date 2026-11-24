from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ExperimentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    target_models: List[str] = Field(..., min_items=1)
    prompt_category: Optional[str] = "all" # "photorealism", "artistic", "cinematic", "spatial_composition", "typography", "all"
    sample_size: int = Field(default=5, ge=1, le=50)
    execution_mode: Optional[str] = "auto" # "auto", "live", "offline-preview"

class HumanEvalSubmission(BaseModel):
    result_id: str
    human_score_quality: float = Field(..., ge=1.0, le=5.0)
    human_score_alignment: float = Field(..., ge=1.0, le=5.0)
    notes: Optional[str] = None

class ModelBenchmarkSummary(BaseModel):
    model_id: str
    total_samples: int
    success_rate: float
    median_latency_ms: float
    p95_latency_ms: float
    avg_cost_usd: float
    avg_sim_score: float # CLIP-like image-text similarity
    avg_quality_score: Optional[float] = None
    avg_alignment_score: Optional[float] = None
    pareto_efficient: bool = False

class ExperimentOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    dataset_name: str
    prompt_count: int
    target_models: List[str]
    status: str
    summary_metrics: Dict[str, Any] = {}
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RoutingRequest(BaseModel):
    task_type: str = "text-to-image"
    prompt: str
    priority: str = "balanced" # "cost", "speed", "quality", "balanced"
    max_budget_usd: Optional[float] = 0.05
    max_latency_ms: Optional[float] = 10000.0

class RoutingDecision(BaseModel):
    selected_model_id: str
    provider: str
    reason: str
    estimated_cost_usd: float
    estimated_latency_ms: float
    confidence_score: float
    alternative_models: List[Dict[str, Any]] = []
    policy_comparison: Dict[str, Any] = {}
