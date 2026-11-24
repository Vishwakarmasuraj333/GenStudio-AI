import asyncio
import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.generation import GenerationJob, MediaAsset, JobStatus, TaskType
from app.schemas.generation import (
    ImageGenRequest, VideoGenRequest, ImageToVideoRequest, ImageEditRequest,
    PromptEnhanceRequest, PromptEnhanceResponse, GenerationJobOut, MediaAssetOut
)
from app.providers.gemini import GeminiPromptEnhancer
from app.providers.registry import get_model_by_id
from app.tasks.worker import execute_generation_job, cancel_active_job
from app.storage.storage_service import storage_service
from app.core.config import settings

router = APIRouter()

@router.post("/enhance-prompt", response_model=PromptEnhanceResponse)
async def enhance_prompt(
    payload: PromptEnhanceRequest,
    current_user: User = Depends(get_current_active_user)
):
    enhancer = GeminiPromptEnhancer()
    res = await enhancer.enhance_prompt(
        prompt=payload.prompt,
        style=payload.style,
        target_task=payload.target_task
    )
    return PromptEnhanceResponse(**res)

@router.post("/image", response_model=GenerationJobOut, status_code=status.HTTP_202_ACCEPTED)
async def create_image_generation(
    payload: ImageGenRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Optional prompt enhancement on-the-fly
    prompt = payload.prompt
    negative_prompt = payload.negative_prompt
    if payload.enable_prompt_enhancement:
        enhancer = GeminiPromptEnhancer()
        enhanced_res = await enhancer.enhance_prompt(prompt, style=payload.style_preset)
        prompt = enhanced_res["enhanced_prompt"]
        if not negative_prompt and enhanced_res.get("suggested_negative_prompt"):
            negative_prompt = enhanced_res["suggested_negative_prompt"]

    # Model resolution derivation
    ar_map = {
        "1:1": (1024, 1024),
        "16:9": (1344, 768),
        "9:16": (768, 1344),
        "4:3": (1152, 864),
        "3:4": (864, 1152)
    }
    width, height = ar_map.get(payload.aspect_ratio, (1024, 1024))

    # Determine provider from model registry
    model_info = get_model_by_id(payload.model_id) or {}
    provider = model_info.get("provider", "huggingface")

    job = GenerationJob(
        user_id=current_user.id,
        project_id=payload.project_id,
        task_type=TaskType.TEXT_TO_IMAGE,
        provider=provider,
        model_id=payload.model_id,
        prompt=prompt,
        negative_prompt=negative_prompt,
        parameters={
            "aspect_ratio": payload.aspect_ratio,
            "width": width,
            "height": height,
            "seed": payload.seed,
            "style_preset": payload.style_preset,
            "original_prompt": payload.prompt if payload.enable_prompt_enhancement else None
        },
        status=JobStatus.PENDING,
        progress=0
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Dispatch to background task worker
    background_tasks.add_task(execute_generation_job, job.id)

    return job

@router.post("/video", response_model=GenerationJobOut, status_code=status.HTTP_202_ACCEPTED)
async def create_text_to_video(
    payload: VideoGenRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    model_info = get_model_by_id(payload.model_id) or {}
    provider = model_info.get("provider", "huggingface")

    job = GenerationJob(
        user_id=current_user.id,
        project_id=payload.project_id,
        task_type=TaskType.TEXT_TO_VIDEO,
        provider=provider,
        model_id=payload.model_id,
        prompt=payload.prompt,
        parameters={
            "duration_sec": payload.duration_sec,
            "aspect_ratio": payload.aspect_ratio,
            "width": payload.width,
            "height": payload.height,
            "fps": payload.fps,
            "seed": payload.seed
        },
        status=JobStatus.PENDING,
        progress=0
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(execute_generation_job, job.id)
    return job

@router.post("/image-to-video", response_model=GenerationJobOut, status_code=status.HTTP_202_ACCEPTED)
async def create_image_to_video(
    payload: ImageToVideoRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Verify reference asset exists and belongs to user
    ref_asset = db.query(MediaAsset).filter(
        MediaAsset.id == payload.reference_image_id,
        MediaAsset.user_id == current_user.id
    ).first()
    if not ref_asset:
        raise HTTPException(status_code=404, detail="Reference image asset not found.")

    model_info = get_model_by_id(payload.model_id) or {}
    provider = model_info.get("provider", "huggingface")

    job = GenerationJob(
        user_id=current_user.id,
        project_id=payload.project_id or ref_asset.project_id,
        task_type=TaskType.IMAGE_TO_VIDEO,
        provider=provider,
        model_id=payload.model_id,
        prompt=payload.prompt or "smooth camera motion",
        parameters={
            "reference_image_id": ref_asset.id,
            "duration_sec": payload.duration_sec
        },
        status=JobStatus.PENDING,
        progress=0
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(execute_generation_job, job.id)
    return job

@router.post("/edit", response_model=GenerationJobOut, status_code=status.HTTP_202_ACCEPTED)
async def create_image_transformation(
    payload: ImageEditRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    base_asset = db.query(MediaAsset).filter(
        MediaAsset.id == payload.base_image_id,
        MediaAsset.user_id == current_user.id
    ).first()
    if not base_asset:
        raise HTTPException(status_code=404, detail="Base image asset not found.")

    job = GenerationJob(
        user_id=current_user.id,
        project_id=payload.project_id or base_asset.project_id,
        task_type=TaskType.IMAGE_TO_IMAGE,
        provider="huggingface",
        model_id=payload.model_id,
        prompt=payload.prompt,
        parameters={
            "base_image_id": base_asset.id,
            "strength": payload.strength
        },
        status=JobStatus.PENDING,
        progress=0
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(execute_generation_job, job.id)
    return job

@router.post("/upload", response_model=MediaAssetOut)
async def upload_reference_image(
    file: UploadFile = File(...),
    project_id: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validation: File size
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"Uploaded file exceeds maximum permitted size of {settings.MAX_UPLOAD_SIZE_BYTES // (1024*1024)}MB."
        )

    # Validation: MIME type
    mime_type = file.content_type or "image/png"
    if mime_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file MIME type: {mime_type}. Allowed: {settings.ALLOWED_IMAGE_TYPES}"
        )

    # Validation: Magic bytes file signature verification (Section 11)
    if not storage_service.verify_magic_bytes(content, mime_type):
        raise HTTPException(
            status_code=400,
            detail="File signature mismatch. The file content does not match its claimed image extension."
        )

    storage_key, file_path, public_url, file_size, checksum = await storage_service.save_bytes(
        data=content,
        filename=file.filename or "upload.png",
        media_type="image",
        mime_type=mime_type
    )

    asset = MediaAsset(
        user_id=current_user.id,
        project_id=project_id,
        media_type="image",
        storage_key=storage_key,
        file_path=file_path,
        public_url=public_url,
        mime_type=mime_type,
        file_size_bytes=file_size,
        checksum_sha256=checksum,
        metadata_json={"source": "user_upload", "original_filename": file.filename}
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@router.get("/jobs/{job_id}", response_model=GenerationJobOut)
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id,
        GenerationJob.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job

@router.post("/jobs/{job_id}/cancel")
def cancel_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id,
        GenerationJob.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    if job.status in [JobStatus.COMPLETED, JobStatus.CANCELLED]:
        return {"message": f"Job is already {job.status}."}

    cancel_active_job(job.id)
    job.status = JobStatus.CANCELLED
    job.error_message = "Cancelled by user."
    db.commit()
    return {"message": "Job cancelled successfully."}

@router.post("/jobs/{job_id}/retry", response_model=GenerationJobOut)
def retry_job(
    job_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id,
        GenerationJob.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    new_job = GenerationJob(
        user_id=current_user.id,
        project_id=job.project_id,
        task_type=job.task_type,
        provider=job.provider,
        model_id=job.model_id,
        prompt=job.prompt,
        negative_prompt=job.negative_prompt,
        parameters=job.parameters,
        status=JobStatus.PENDING,
        progress=0
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    background_tasks.add_task(execute_generation_job, new_job.id)
    return new_job

@router.get("/jobs/{job_id}/events")
async def stream_job_events(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Server-Sent Events (SSE) stream for real-time generation progress."""
    async def event_generator():
        while True:
            # Query fresh state
            curr_job = db.query(GenerationJob).filter(
                GenerationJob.id == job_id,
                GenerationJob.user_id == current_user.id
            ).first()
            if not curr_job:
                yield f"event: error\ndata: {json.dumps({'error': 'Job not found'})}\n\n"
                break

            data = {
                "id": curr_job.id,
                "status": curr_job.status,
                "progress": curr_job.progress,
                "error_message": curr_job.error_message,
                "latency_ms": curr_job.latency_ms,
                "assets": [
                    {"id": a.id, "public_url": a.public_url, "mime_type": a.mime_type}
                    for a in curr_job.assets
                ]
            }
            yield f"event: update\ndata: {json.dumps(data)}\n\n"

            if curr_job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                break

            await asyncio.sleep(1.0)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/media/{storage_key:path}")
def serve_media(storage_key: str):
    """Safely serves stored media assets preventing path traversal."""
    file_path = storage_service.get_file_path(storage_key)
    if not file_path or not file_path.exists():
        raise HTTPException(status_code=404, detail="Media asset file not found.")

    ext = file_path.suffix.lower()
    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".mp4": "video/mp4",
        ".webm": "video/webm"
    }
    content_type = media_types.get(ext, "application/octet-stream")
    return FileResponse(file_path, media_type=content_type)
