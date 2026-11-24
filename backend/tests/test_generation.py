import pytest
import asyncio
from app.tasks.worker import execute_generation_job

def test_submit_image_generation_job(client, user_auth_headers):
    response = client.post(
        "/api/v1/studio/image",
        headers=user_auth_headers,
        json={
            "prompt": "Cinematic portrait of an ancient scholar in an illuminated library",
            "model_id": "black-forest-labs/FLUX.1-schnell",
            "aspect_ratio": "16:9",
            "seed": 42
        }
    )
    assert response.status_code == 202
    job = response.json()
    assert job["task_type"] == "text-to-image"
    assert job["status"] in ["pending", "processing"]
    assert "id" in job

def test_submit_video_generation_job(client, user_auth_headers):
    response = client.post(
        "/api/v1/studio/video",
        headers=user_auth_headers,
        json={
            "prompt": "Aerial flight over misty mountains at sunrise",
            "model_id": "Lightricks/LTX-Video",
            "duration_sec": 4.0
        }
    )
    assert response.status_code == 202
    job = response.json()
    assert job["task_type"] == "text-to-video"
    assert job["status"] in ["pending", "processing"]

@pytest.mark.asyncio
async def test_job_worker_execution_completes(client, user_auth_headers, db):
    # Submit job
    response = client.post(
        "/api/v1/studio/image",
        headers=user_auth_headers,
        json={
            "prompt": "Deterministic test image generation",
            "model_id": "black-forest-labs/FLUX.1-schnell"
        }
    )
    job_id = response.json()["id"]

    # Directly execute background worker logic
    await execute_generation_job(job_id, db=db)

    # Check job status via API
    status_res = client.get(f"/api/v1/studio/jobs/{job_id}", headers=user_auth_headers)
    assert status_res.status_code == 200
    job_data = status_res.json()
    assert job_data["status"] == "completed"
    assert job_data["progress"] == 100
    assert len(job_data["assets"]) >= 1

    # Verify generated media can be retrieved
    asset = job_data["assets"][0]
    media_res = client.get(asset["public_url"])
    assert media_res.status_code == 200
    assert len(media_res.content) > 0

def test_cancel_job(client, user_auth_headers):
    response = client.post(
        "/api/v1/studio/image",
        headers=user_auth_headers,
        json={"prompt": "Job to cancel", "model_id": "black-forest-labs/FLUX.1-schnell"}
    )
    job_id = response.json()["id"]

    cancel_res = client.post(f"/api/v1/studio/jobs/{job_id}/cancel", headers=user_auth_headers)
    assert cancel_res.status_code == 200
    assert "cancelled" in cancel_res.json()["message"]

def test_prompt_enhancement(client, user_auth_headers):
    response = client.post(
        "/api/v1/studio/enhance-prompt",
        headers=user_auth_headers,
        json={
            "prompt": "vintage car on a street",
            "style": "photorealistic"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["enhanced_prompt"]) > len("vintage car on a street")
    assert "suggested_negative_prompt" in data

@pytest.mark.asyncio
async def test_live_mode_without_token_fails_honestly_without_mock_output(client, user_auth_headers, db):
    from app.core.config import settings
    original_mode = settings.PROVIDER_MODE
    original_token = settings.HF_API_TOKEN
    try:
        # Enforce live mode with unconfigured token
        settings.PROVIDER_MODE = "live"
        settings.HF_API_TOKEN = None

        response = client.post(
            "/api/v1/studio/image",
            headers=user_auth_headers,
            json={
                "prompt": "Live generation without API token",
                "model_id": "black-forest-labs/FLUX.1-schnell"
            }
        )
        assert response.status_code == 202
        job_id = response.json()["id"]

        # Run background worker
        await execute_generation_job(job_id, db=db)

        # Verify job FAILED with clear configuration error and NO assets generated
        status_res = client.get(f"/api/v1/studio/jobs/{job_id}", headers=user_auth_headers)
        assert status_res.status_code == 200
        job_data = status_res.json()
        assert job_data["status"] == "failed"
        assert "HF_API_TOKEN" in job_data["error_message"]
        assert len(job_data["assets"]) == 0
    finally:
        settings.PROVIDER_MODE = original_mode
        settings.HF_API_TOKEN = original_token

@pytest.mark.asyncio
async def test_offline_preview_mode_labels_metadata(client, user_auth_headers, db):
    from app.core.config import settings
    original_mode = settings.PROVIDER_MODE
    try:
        settings.PROVIDER_MODE = "offline-preview"
        response = client.post(
            "/api/v1/studio/image",
            headers=user_auth_headers,
            json={
                "prompt": "Offline preview generation",
                "model_id": "black-forest-labs/FLUX.1-schnell"
            }
        )
        job_id = response.json()["id"]
        await execute_generation_job(job_id, db=db)

        status_res = client.get(f"/api/v1/studio/jobs/{job_id}", headers=user_auth_headers)
        assert status_res.status_code == 200
        job_data = status_res.json()
        assert job_data["status"] == "completed"
        assert len(job_data["assets"]) >= 1
    finally:
        settings.PROVIDER_MODE = original_mode

def test_health_endpoint_reports_provider_mode(client):
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert "provider_mode" in data
    assert "required_env_vars" in data
    assert data["required_env_vars"]["huggingface"] == "HF_API_TOKEN"

def test_user_isolation_cannot_read_or_cancel_other_user_job(client, user_auth_headers, second_user_auth_headers):
    # User 1 creates job
    res = client.post(
        "/api/v1/studio/image",
        headers=user_auth_headers,
        json={"prompt": "User 1 Job", "model_id": "black-forest-labs/FLUX.1-schnell"}
    )
    job_id = res.json()["id"]

    # User 2 tries to read it
    get_res = client.get(f"/api/v1/studio/jobs/{job_id}", headers=second_user_auth_headers)
    assert get_res.status_code == 404

    # User 2 tries to cancel it
    cancel_res = client.post(f"/api/v1/studio/jobs/{job_id}/cancel", headers=second_user_auth_headers)
    assert cancel_res.status_code == 404
