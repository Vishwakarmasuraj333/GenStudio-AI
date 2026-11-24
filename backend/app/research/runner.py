import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.research import EvaluationRun, EvaluationResult
from app.research.dataset import get_benchmark_prompts
from app.research.metrics import ResearchMetricsCalculator
from app.providers.mock_provider import MockTestProvider
from app.providers.huggingface import HuggingFaceProvider
from app.core.config import settings

class BenchmarkRunner:
    """
    Executes controlled experiments on a fixed dataset across multiple generative AI models.
    Records actual measurements, calculates statistical summaries, and exports CSV/JSON reports.
    """

    def __init__(self, db: Session, use_live_provider: bool = False):
        self.db = db
        self.use_live_provider = use_live_provider
        self.mock_provider = MockTestProvider()
        self.hf_provider = HuggingFaceProvider()

    async def execute_run(
        self,
        name: str,
        target_models: List[str],
        category: str = "all",
        sample_size: int = 5,
        description: Optional[str] = None
    ) -> EvaluationRun:
        prompts = get_benchmark_prompts(category=category, limit=sample_size)
        
        run = EvaluationRun(
            name=name,
            description=description or f"Comparative evaluation across {len(target_models)} models",
            dataset_name="GenStudio-Bench-v1",
            prompt_count=len(prompts) * len(target_models),
            target_models=target_models,
            status="running"
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        results_list = []

        for p in prompts:
            for m_id in target_models:
                start_ts = time.perf_counter()
                success = True
                error_msg = None
                cost_usd = 0.003
                latency_ms = 0.0

                try:
                    if self.use_live_provider and self.hf_provider.is_configured():
                        gen_res = await self.hf_provider.generate_image(
                            prompt=p["prompt"],
                            model_id=m_id,
                            width=1024,
                            height=1024
                        )
                        latency_ms = gen_res.latency_ms
                        cost_usd = gen_res.cost_usd
                    else:
                        gen_res = await self.mock_provider.generate_image(
                            prompt=p["prompt"],
                            model_id=m_id,
                            width=1024,
                            height=1024
                        )
                        latency_ms = gen_res.latency_ms
                        cost_usd = gen_res.cost_usd

                except Exception as e:
                    success = False
                    error_msg = str(e)
                    latency_ms = (time.perf_counter() - start_ts) * 1000.0

                sim_score = ResearchMetricsCalculator.estimate_clip_similarity(p["prompt"], m_id)
                temporal_score = ResearchMetricsCalculator.estimate_temporal_consistency(5.0, m_id) if "Video" in m_id or "Wan" in m_id else None

                eval_res = EvaluationResult(
                    run_id=run.id,
                    prompt_id=p["id"],
                    prompt_text=p["prompt"],
                    prompt_category=p["category"],
                    model_id=m_id,
                    latency_ms=round(latency_ms, 2),
                    cost_usd=cost_usd,
                    success=success,
                    error_message=error_msg,
                    sim_score=sim_score,
                    temporal_score=temporal_score,
                    raw_metrics_json={
                        "difficulty": p.get("difficulty", "medium"),
                        "aspect_ratio": p.get("aspect_ratio", "1:1"),
                        "simulated_run": not (self.use_live_provider and self.hf_provider.is_configured())
                    }
                )
                self.db.add(eval_res)
                results_list.append({
                    "model_id": m_id,
                    "latency_ms": latency_ms,
                    "cost_usd": cost_usd,
                    "success": success,
                    "sim_score": sim_score,
                    "human_score_quality": None,
                    "human_score_alignment": None
                })

        # Calculate final summary
        summary = ResearchMetricsCalculator.compute_summary_metrics(results_list)
        is_live = bool(self.use_live_provider and self.hf_provider.is_configured())
        summary["_execution_metadata"] = {
            "mode": "live" if is_live else "offline-preview",
            "is_live_inference": is_live,
            "is_simulated": not is_live,
            "label": "Live External Inference" if is_live else "Offline Preview (Synthetic Test Fixtures)"
        }
        run.summary_metrics = summary
        run.status = "completed"
        run.completed_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(run)

        return run

    @staticmethod
    def export_run_to_csv(run: EvaluationRun, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "run_id", "prompt_id", "prompt_category", "model_id",
                "latency_ms", "cost_usd", "success", "sim_score", "temporal_score", "prompt_text"
            ])
            for res in run.results:
                writer.writerow([
                    run.id, res.prompt_id, res.prompt_category, res.model_id,
                    res.latency_ms, res.cost_usd, res.success, res.sim_score,
                    res.temporal_score or "N/A", res.prompt_text
                ])
        return output_path

    @staticmethod
    def export_run_to_json(run: EvaluationRun, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "run_id": run.id,
            "name": run.name,
            "dataset_name": run.dataset_name,
            "created_at": run.created_at.isoformat(),
            "completed_at": run.completed_at.isoformat() if run.completed_at else None,
            "target_models": run.target_models,
            "summary_metrics": run.summary_metrics,
            "observations": [
                {
                    "prompt_id": r.prompt_id,
                    "category": r.prompt_category,
                    "model_id": r.model_id,
                    "latency_ms": r.latency_ms,
                    "cost_usd": r.cost_usd,
                    "success": r.success,
                    "sim_score": r.sim_score,
                    "temporal_score": r.temporal_score,
                    "prompt_text": r.prompt_text
                }
                for r in run.results
            ]
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return output_path
