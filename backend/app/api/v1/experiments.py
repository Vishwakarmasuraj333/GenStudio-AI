from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.research import EvaluationRun, EvaluationResult, UserFeedback
from app.schemas.research import (
    ExperimentCreate, ExperimentOut, HumanEvalSubmission,
    RoutingRequest, RoutingDecision
)
from app.research.dataset import BENCHMARK_PROMPTS, get_benchmark_prompts
from app.research.runner import BenchmarkRunner
from app.research.router import IntelligentModelRouter
from app.core.config import settings

router = APIRouter()

@router.get("/prompts")
def list_benchmark_prompts(
    category: Optional[str] = "all",
    limit: int = Query(20, ge=1, le=50)
):
    """Returns curated standardized benchmark prompts across domain categories."""
    return get_benchmark_prompts(category=category, limit=limit)

@router.post("/run", response_model=ExperimentOut, status_code=status.HTTP_201_CREATED)
async def run_experiment(
    payload: ExperimentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Executes a reproducible controlled evaluation across specified models.
    Records latency, cost, success rate, and calculates statistical summaries.
    Clearly distinguishes live external inference from offline preview test fixtures.
    """
    from app.providers.huggingface import HuggingFaceProvider
    hf = HuggingFaceProvider()

    # Determine execution mode honesty
    requested_live = (
        payload.execution_mode == "live" or
        (payload.execution_mode == "auto" and settings.PROVIDER_MODE == "live")
    )
    if requested_live:
        if not hf.is_configured():
            if payload.execution_mode == "live":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot execute live benchmark: Hugging Face API token (HF_API_TOKEN) is not configured in server environment. Configure HF_API_TOKEN or select 'offline-preview' execution mode."
                )
            use_live = False
        else:
            use_live = True
    else:
        use_live = False

    runner = BenchmarkRunner(db=db, use_live_provider=use_live)
    desc = payload.description or ""
    if not use_live:
        desc = (desc + " [Offline Preview Simulation - Synthetic Test Fixtures]").strip()

    run = await runner.execute_run(
        name=payload.name,
        target_models=payload.target_models,
        category=payload.prompt_category or "all",
        sample_size=payload.sample_size,
        description=desc
    )
    return run

@router.get("/runs", response_model=List[ExperimentOut])
def list_experiment_runs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    runs = db.query(EvaluationRun).order_by(EvaluationRun.created_at.desc()).offset(offset).limit(limit).all()
    return runs

@router.get("/runs/{run_id}", response_model=ExperimentOut)
def get_experiment_run(
    run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Evaluation run not found.")
    return run

@router.get("/runs/{run_id}/results")
def get_run_results(
    run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    results = db.query(EvaluationResult).filter(EvaluationResult.run_id == run_id).all()
    return [
        {
            "id": r.id,
            "prompt_id": r.prompt_id,
            "prompt_text": r.prompt_text,
            "prompt_category": r.prompt_category,
            "model_id": r.model_id,
            "latency_ms": r.latency_ms,
            "cost_usd": r.cost_usd,
            "success": r.success,
            "error_message": r.error_message,
            "sim_score": r.sim_score,
            "temporal_score": r.temporal_score,
            "human_score_quality": r.human_score_quality,
            "human_score_alignment": r.human_score_alignment
        }
        for r in results
    ]

@router.get("/runs/{run_id}/export/csv")
def export_run_csv(
    run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Evaluation run not found.")

    export_path = Path(settings.MEDIA_STORAGE_DIR).parent / "reports" / f"eval_run_{run_id}.csv"
    BenchmarkRunner.export_run_to_csv(run, export_path)
    return FileResponse(
        export_path,
        media_type="text/csv",
        filename=f"GenStudio_Benchmark_{run.name.replace(' ', '_')}_{run_id[:6]}.csv"
    )

@router.get("/runs/{run_id}/export/json")
def export_run_json(
    run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Evaluation run not found.")

    export_path = Path(settings.MEDIA_STORAGE_DIR).parent / "reports" / f"eval_run_{run_id}.json"
    BenchmarkRunner.export_run_to_json(run, export_path)
    return FileResponse(
        export_path,
        media_type="application/json",
        filename=f"GenStudio_Benchmark_{run.name.replace(' ', '_')}_{run_id[:6]}.json"
    )

@router.post("/route", response_model=RoutingDecision)
def evaluate_intelligent_routing(
    payload: RoutingRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Evaluates the multi-objective intelligent model routing policy
    against a static baseline.
    """
    router_engine = IntelligentModelRouter()
    decision = router_engine.route(
        task_type=payload.task_type,
        prompt=payload.prompt,
        priority=payload.priority,
        max_budget_usd=payload.max_budget_usd,
        max_latency_ms=payload.max_latency_ms
    )
    return decision

@router.post("/feedback")
def submit_human_evaluation(
    payload: HumanEvalSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = db.query(EvaluationResult).filter(EvaluationResult.id == payload.result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Evaluation observation record not found.")

    result.human_score_quality = payload.human_score_quality
    result.human_score_alignment = payload.human_score_alignment
    db.commit()
    return {"message": "Human evaluation scores recorded successfully."}
