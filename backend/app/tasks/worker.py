import asyncio
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.generation import GenerationJob, MediaAsset, JobStatus, TaskType
from app.models.audit import UsageRecord, AuditLog
from app.providers.huggingface import HuggingFaceProvider, ProviderConfigurationError, ProviderException
from app.providers.mock_provider import MockTestProvider
from app.storage.storage_service import storage_service
from app.core.config import settings

# Global active jobs registry for cancellation coordination
_ACTIVE_JOB_CANCELLATIONS = set()

def cancel_active_job(job_id: str):
    _ACTIVE_JOB_CANCELLATIONS.add(job_id)

async def execute_generation_job(job_id: str, db: Optional[Session] = None):
    """
    Asynchronously processes a generation job in background.
    Safely captures errors, records latency and costs, verifies media outputs,
    and maintains database integrity.
    """
    should_close_db = False
    if db is None:
        db = SessionLocal()
        should_close_db = True
    try:
        job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
        if not job:
            return

        # Check if already cancelled
        if job.id in _ACTIVE_JOB_CANCELLATIONS or job.status == JobStatus.CANCELLED:
            job.status = JobStatus.CANCELLED
            job.error_message = "Job cancelled by user before execution."
            db.commit()
            return

        job.status = JobStatus.PROCESSING
        job.started_at = datetime.now(timezone.utc)
        job.progress = 10
        db.commit()

        start_time = time.perf_counter()
        provider_name = job.provider
        task_type = job.task_type
        model_id = job.model_id
        prompt = job.prompt
        negative_prompt = job.negative_prompt
        params = job.parameters or {}

        # Select provider adapter
        hf_provider = HuggingFaceProvider()
        mock_provider = MockTestProvider()
        mode = settings.PROVIDER_MODE.lower()

        job.progress = 30
        db.commit()

        # Dispatch generation
        try:
            # Enforce honesty rule: In live mode, verify credentials before dispatching. Never silently fallback.
            if mode == "live":
                if provider_name == "huggingface":
                    if not hf_provider.is_configured():
                        raise ProviderConfigurationError(
                            "Hugging Face API token is not configured. Please add HF_API_TOKEN to your server environment or .env file to enable live inference. Substitute mock generation is disabled in live mode."
                        )
                else:
                    raise ProviderConfigurationError(f"Provider '{provider_name}' is not configured for live inference.")
            elif mode not in ["test", "offline-preview"]:
                raise ValueError(f"Invalid PROVIDER_MODE '{settings.PROVIDER_MODE}'. Must be 'live', 'test', or 'offline-preview'.")
            if task_type == TaskType.TEXT_TO_IMAGE:
                aspect_ratio = params.get("aspect_ratio", "1:1")
                width = params.get("width", 1024)
                height = params.get("height", 1024)
                seed = params.get("seed")

                if mode == "live":
                    result = await hf_provider.generate_image(
                        prompt=prompt,
                        model_id=model_id,
                        negative_prompt=negative_prompt,
                        width=width,
                        height=height,
                        seed=seed,
                        parameters=params
                    )
                else:
                    # Explicit deterministic test or offline-preview fixture provider
                    result = await mock_provider.generate_image(
                        prompt=prompt,
                        model_id=model_id,
                        negative_prompt=negative_prompt,
                        width=width,
                        height=height,
                        seed=seed
                    )
                    if mode == "offline-preview":
                        result.metadata["offline_preview"] = True
                        result.metadata["synthetic_fixture"] = True
                    elif mode == "test":
                        result.metadata["test_mode"] = True

            elif task_type == TaskType.TEXT_TO_VIDEO:
                duration_sec = float(params.get("duration_sec", 5.0))
                width = params.get("width", 1280)
                height = params.get("height", 720)
                fps = params.get("fps", 24)
                seed = params.get("seed")

                if mode == "live":
                    result = await hf_provider.generate_video(
                        prompt=prompt,
                        model_id=model_id,
                        duration_sec=duration_sec,
                        width=width,
                        height=height,
                        fps=fps,
                        seed=seed
                    )
                else:
                    result = await mock_provider.generate_video(
                        prompt=prompt,
                        model_id=model_id,
                        duration_sec=duration_sec,
                        width=width,
                        height=height,
                        fps=fps,
                        seed=seed
                    )
                    if mode == "offline-preview":
                        result.metadata["offline_preview"] = True
                        result.metadata["synthetic_fixture"] = True
                    elif mode == "test":
                        result.metadata["test_mode"] = True

            elif task_type == TaskType.IMAGE_TO_VIDEO:
                duration_sec = float(params.get("duration_sec", 5.0))
                ref_bytes = b""
                ref_id = params.get("reference_image_id")
                if ref_id:
                    ref_asset = db.query(MediaAsset).filter(MediaAsset.id == ref_id).first()
                    if ref_asset and ref_asset.file_path:
                        with open(ref_asset.file_path, "rb") as f:
                            ref_bytes = f.read()

                if mode == "live":
                    if not ref_bytes:
                        raise ValueError("Reference image asset not found or empty.")
                    result = await hf_provider.image_to_video(
                        reference_image_bytes=ref_bytes,
                        prompt=prompt,
                        model_id=model_id,
                        duration_sec=duration_sec
                    )
                else:
                    result = await mock_provider.image_to_video(
                        reference_image_bytes=ref_bytes or b"dummy",
                        prompt=prompt,
                        model_id=model_id,
                        duration_sec=duration_sec
                    )
                    if mode == "offline-preview":
                        result.metadata["offline_preview"] = True
                        result.metadata["synthetic_fixture"] = True
                    elif mode == "test":
                        result.metadata["test_mode"] = True

            elif task_type == TaskType.IMAGE_TO_IMAGE:
                ref_bytes = b""
                ref_id = params.get("base_image_id")
                strength = float(params.get("strength", 0.75))
                if ref_id:
                    ref_asset = db.query(MediaAsset).filter(MediaAsset.id == ref_id).first()
                    if ref_asset and ref_asset.file_path:
                        with open(ref_asset.file_path, "rb") as f:
                            ref_bytes = f.read()

                if mode == "live":
                    if not ref_bytes:
                        raise ValueError("Base image asset not found or empty.")
                    result = await hf_provider.transform_image(
                        image_bytes=ref_bytes,
                        prompt=prompt,
                        model_id=model_id,
                        strength=strength
                    )
                else:
                    result = await mock_provider.transform_image(
                        image_bytes=ref_bytes or b"dummy",
                        prompt=prompt,
                        model_id=model_id,
                        strength=strength
                    )
                    if mode == "offline-preview":
                        result.metadata["offline_preview"] = True
                        result.metadata["synthetic_fixture"] = True
                    elif mode == "test":
                        result.metadata["test_mode"] = True
            else:
                raise ValueError(f"Unsupported task type: {task_type}")

        except ProviderConfigurationError as pce:
            job.status = JobStatus.FAILED
            job.error_message = f"Provider Configuration Error: {str(pce)}"
            job.completed_at = datetime.now(timezone.utc)
            db.commit()
            return
        except Exception as gen_err:
            job.status = JobStatus.FAILED
            job.error_message = f"Generation Error: {str(gen_err)}"
            job.completed_at = datetime.now(timezone.utc)
            db.commit()
            return

        # Verification of generated output bytes (Section 6: Never report as completed until verified)
        media_type = "video" if "video" in task_type else "image"
        if not storage_service.verify_magic_bytes(result.media_bytes, result.mime_type):
            job.status = JobStatus.FAILED
            job.error_message = "Output verification failed: corrupted or invalid media byte signature."
            job.completed_at = datetime.now(timezone.utc)
            db.commit()
            return

        # Save media asset securely
        ext = "mp4" if media_type == "video" else "png"
        filename = f"genstudio_{job.id[:8]}.{ext}"
        storage_key, file_path, public_url, file_size, checksum = await storage_service.save_bytes(
            data=result.media_bytes,
            filename=filename,
            media_type=media_type,
            mime_type=result.mime_type
        )

        # Create MediaAsset record
        asset = MediaAsset(
            user_id=job.user_id,
            project_id=job.project_id,
            job_id=job.id,
            media_type=media_type,
            storage_key=storage_key,
            file_path=file_path,
            public_url=public_url,
            mime_type=result.mime_type,
            file_size_bytes=file_size,
            width=result.width,
            height=result.height,
            duration_sec=result.duration_sec,
            checksum_sha256=checksum,
            metadata_json={
                **result.metadata,
                "verified": True,
                "provider_mode": mode,
                "provider_actual": "huggingface" if mode == "live" else ("offline_preview" if mode == "offline-preview" else "mock_test_provider"),
                "is_live_inference": mode == "live",
                "is_offline_preview": mode == "offline-preview"
            }
        )
        db.add(asset)

        # Update Job Record
        total_latency = (time.perf_counter() - start_time) * 1000.0
        job.status = JobStatus.COMPLETED
        job.progress = 100
        job.latency_ms = round(total_latency, 2)
        job.cost_usd = result.cost_usd
        job.completed_at = datetime.now(timezone.utc)

        # Record Usage Telemetry
        usage = UsageRecord(
            user_id=job.user_id,
            job_id=job.id,
            provider=job.provider,
            model_id=job.model_id,
            compute_duration_sec=round(total_latency / 1000.0, 2),
            estimated_cost_usd=result.cost_usd
        )
        db.add(usage)

        # Record Audit Log
        audit = AuditLog(
            user_id=job.user_id,
            action="GENERATION_COMPLETED",
            resource_type="generation_job",
            resource_id=job.id,
            details_json={
                "task_type": job.task_type,
                "model_id": job.model_id,
                "latency_ms": job.latency_ms,
                "cost_usd": job.cost_usd
            }
        )
        db.add(audit)

        db.commit()

    finally:
        if job_id in _ACTIVE_JOB_CANCELLATIONS:
            _ACTIVE_JOB_CANCELLATIONS.discard(job_id)
        if should_close_db:
            db.close()
