from fastapi import APIRouter
from app.core.config import settings
from app.providers.huggingface import HuggingFaceProvider
from app.providers.gemini import GeminiPromptEnhancer

router = APIRouter()

@router.get("/")
def health_check():
    hf = HuggingFaceProvider()
    gemini = GeminiPromptEnhancer()
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "provider_mode": settings.PROVIDER_MODE,
        "providers_configured": {
            "huggingface": hf.is_configured(),
            "gemini": gemini.is_configured(),
            "comfyui": False,
            "mock_test_provider": settings.PROVIDER_MODE in ["test", "offline-preview"]
        },
        "required_env_vars": {
            "huggingface": "HF_API_TOKEN",
            "gemini": "GEMINI_API_KEY",
            "comfyui": "COMFYUI_BASE_URL"
        }
    }
