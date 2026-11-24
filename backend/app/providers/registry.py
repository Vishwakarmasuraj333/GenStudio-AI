from typing import List, Dict, Any, Optional

CURATED_MODELS: List[Dict[str, Any]] = [
    {
        "provider": "huggingface",
        "model_id": "black-forest-labs/FLUX.1-schnell",
        "display_name": "FLUX.1 [schnell]",
        "version": "1.0",
        "task_types": ["text-to-image"],
        "max_resolution": "1024x1024",
        "supported_aspect_ratios": ["1:1", "16:9", "9:16", "4:3", "3:4"],
        "capabilities_json": {
            "supports_seed": True,
            "supports_negative_prompt": False,
            "supports_guidance_scale": False,
            "steps": 4,
            "fast_inference": True
        },
        "pricing_json": {
            "cost_per_gen_usd": 0.003,
            "tier": "community_inference",
            "source": "Hugging Face Inference Provider Rate Card",
            "last_checked": "2026-11-20"
        },
        "license_info": "Apache-2.0",
        "is_enabled": True
    },
    {
        "provider": "huggingface",
        "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
        "display_name": "SDXL 1.0 Base",
        "version": "1.0",
        "task_types": ["text-to-image"],
        "max_resolution": "1024x1024",
        "supported_aspect_ratios": ["1:1", "16:9", "9:16", "4:3"],
        "capabilities_json": {
            "supports_seed": True,
            "supports_negative_prompt": True,
            "supports_guidance_scale": True,
            "steps": 30,
            "fast_inference": False
        },
        "pricing_json": {
            "cost_per_gen_usd": 0.006,
            "tier": "standard_inference",
            "source": "Hugging Face Serverless Inference Documentation",
            "last_checked": "2026-11-20"
        },
        "license_info": "OpenRAIL++",
        "is_enabled": True
    },
    {
        "provider": "huggingface",
        "model_id": "timbrooks/instruct-pix2pix",
        "display_name": "InstructPix2Pix",
        "version": "1.0",
        "task_types": ["image-to-image"],
        "max_resolution": "512x512",
        "supported_aspect_ratios": ["1:1"],
        "capabilities_json": {
            "supports_seed": True,
            "supports_negative_prompt": False,
            "supports_strength": True
        },
        "pricing_json": {
            "cost_per_gen_usd": 0.005,
            "tier": "standard_inference",
            "source": "Hugging Face Inference Endpoints",
            "last_checked": "2026-11-20"
        },
        "license_info": "CreativeML OpenRAIL-M",
        "is_enabled": True
    },
    {
        "provider": "huggingface",
        "model_id": "Lightricks/LTX-Video",
        "display_name": "LTX-Video (DiT)",
        "version": "0.9.1",
        "task_types": ["text-to-video", "image-to-video"],
        "max_resolution": "1280x720",
        "supported_aspect_ratios": ["16:9", "9:16", "1:1"],
        "capabilities_json": {
            "supports_seed": True,
            "supports_duration": True,
            "max_duration_sec": 10.0,
            "fps": 24,
            "requires_queue": True
        },
        "pricing_json": {
            "cost_per_gen_usd": 0.045,
            "tier": "video_inference",
            "source": "Hugging Face Dedicated / Partner Endpoint Estimation",
            "last_checked": "2026-11-20"
        },
        "license_info": "Apache-2.0",
        "is_enabled": True
    },
    {
        "provider": "huggingface",
        "model_id": "Wan-AI/Wan2.1-T2V-14B",
        "display_name": "Wan2.1 Video 14B",
        "version": "2.1",
        "task_types": ["text-to-video"],
        "max_resolution": "1280x720",
        "supported_aspect_ratios": ["16:9", "9:16"],
        "capabilities_json": {
            "supports_seed": True,
            "supports_duration": True,
            "max_duration_sec": 5.0,
            "fps": 16,
            "requires_queue": True
        },
        "pricing_json": {
            "cost_per_gen_usd": 0.080,
            "tier": "high_compute_video",
            "source": "Inference Endpoint Pricing Matrix",
            "last_checked": "2026-11-20"
        },
        "license_info": "Apache-2.0",
        "is_enabled": True
    },
    {
        "provider": "google",
        "model_id": "gemini-2.0-flash",
        "display_name": "Gemini 2.0 Flash (Prompt Refinement)",
        "version": "2.0",
        "task_types": ["prompt-enhancement"],
        "max_resolution": "N/A",
        "supported_aspect_ratios": [],
        "capabilities_json": {
            "supports_negative_prompt_extraction": True,
            "style_adaptation": True,
            "token_budget": 1000
        },
        "pricing_json": {
            "cost_per_gen_usd": 0.0001,
            "tier": "llm_text",
            "source": "Google AI Studio Pricing",
            "last_checked": "2026-11-20"
        },
        "license_info": "Commercial / Proprietary API",
        "is_enabled": True
    }
]

def get_model_by_id(model_id: str) -> Optional[Dict[str, Any]]:
    for m in CURATED_MODELS:
        if m["model_id"] == model_id:
            return m
    return None

def list_models_for_task(task_type: str) -> List[Dict[str, Any]]:
    return [m for m in CURATED_MODELS if task_type in m["task_types"] and m["is_enabled"]]
