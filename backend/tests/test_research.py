import pytest
from app.research.dataset import get_benchmark_prompts, BENCHMARK_PROMPTS
from app.research.metrics import ResearchMetricsCalculator
from app.research.router import IntelligentModelRouter

def test_benchmark_dataset_retrieval():
    prompts = get_benchmark_prompts("all", limit=10)
    assert len(prompts) == 10
    categories = {p["category"] for p in BENCHMARK_PROMPTS}
    assert "photorealism" in categories
    assert "cinematic" in categories
    assert "typography" in categories

def test_metrics_percentile_calculation():
    values = [100.0, 200.0, 300.0, 400.0, 500.0]
    p50 = ResearchMetricsCalculator.calculate_percentile(values, 50.0)
    assert p50 == 300.0
    p90 = ResearchMetricsCalculator.calculate_percentile(values, 90.0)
    assert p90 == 460.0

def test_summary_metrics_aggregation():
    sample_records = [
        {"model_id": "model_a", "latency_ms": 1200.0, "cost_usd": 0.003, "success": True, "sim_score": 0.85},
        {"model_id": "model_a", "latency_ms": 1400.0, "cost_usd": 0.003, "success": True, "sim_score": 0.83},
        {"model_id": "model_a", "latency_ms": 2000.0, "cost_usd": 0.003, "success": False, "sim_score": 0.50}
    ]
    summary = ResearchMetricsCalculator.compute_summary_metrics(sample_records)
    assert "model_a" in summary
    stats = summary["model_a"]
    assert stats["total_samples"] == 3
    assert stats["successful_samples"] == 2
    assert stats["failed_samples"] == 1
    assert stats["success_rate"] == round(2/3, 4)

def test_intelligent_model_router_priorities():
    router = IntelligentModelRouter()

    # Cost priority should favor FLUX.1 (0.003 vs 0.006)
    decision_cost = router.route(
        task_type="text-to-image",
        prompt="A photo of a cat",
        priority="cost"
    )
    assert decision_cost["selected_model_id"] == "black-forest-labs/FLUX.1-schnell"
    assert "cost_savings_vs_baseline_pct" in decision_cost["policy_comparison"]

    # Strict budget constraint rejection
    decision_budget = router.route(
        task_type="text-to-image",
        prompt="A photo of a cat",
        priority="balanced",
        max_budget_usd=0.004
    )
    assert decision_budget["selected_model_id"] == "black-forest-labs/FLUX.1-schnell"

@pytest.mark.asyncio
async def test_experiment_api_run(client, user_auth_headers):
    response = client.post(
        "/api/v1/experiments/run",
        headers=user_auth_headers,
        json={
            "name": "Controlled Fast Benchmark",
            "target_models": ["black-forest-labs/FLUX.1-schnell", "stabilityai/stable-diffusion-xl-base-1.0"],
            "prompt_category": "photorealism",
            "sample_size": 2
        }
    )
    assert response.status_code == 201
    run_data = response.json()
    assert run_data["status"] == "completed"
    assert run_data["prompt_count"] == 4
    assert "black-forest-labs/FLUX.1-schnell" in run_data["summary_metrics"]

    # Test CSV Export
    run_id = run_data["id"]
    csv_res = client.get(f"/api/v1/experiments/runs/{run_id}/export/csv", headers=user_auth_headers)
    assert csv_res.status_code == 200
    assert "text/csv" in csv_res.headers.get("content-type", "")
    assert "run_id" in csv_res.text

    # Test JSON Export
    json_res = client.get(f"/api/v1/experiments/runs/{run_id}/export/json", headers=user_auth_headers)
    assert json_res.status_code == 200
    assert "application/json" in json_res.headers.get("content-type", "")
    assert json_res.json()["run_id"] == run_id
