from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class ProviderGenerationResult(BaseModel):
    media_bytes: bytes
    mime_type: str
    latency_ms: float
    cost_usd: float
    provider_job_id: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration_sec: Optional[float] = None
    metadata: Dict[str, Any] = {}

class BaseProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of provider e.g. huggingface, gemini, comfyui."""
        pass

    @abstractmethod
    def validate_model(self, model_id: str) -> bool:
        """Check if model_id is supported and valid."""
        pass

    @abstractmethod
    def get_capabilities(self, model_id: str) -> Dict[str, Any]:
        """Return parameter support and capability flags."""
        pass

class ImageProviderInterface(BaseProvider):
    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        model_id: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        seed: Optional[int] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        pass

    @abstractmethod
    async def transform_image(
        self,
        image_bytes: bytes,
        prompt: str,
        model_id: str,
        strength: float = 0.75,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        pass

class VideoProviderInterface(BaseProvider):
    @abstractmethod
    async def generate_video(
        self,
        prompt: str,
        model_id: str,
        duration_sec: float = 5.0,
        width: int = 1280,
        height: int = 720,
        fps: int = 24,
        seed: Optional[int] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        pass

    @abstractmethod
    async def image_to_video(
        self,
        reference_image_bytes: bytes,
        prompt: str,
        model_id: str,
        duration_sec: float = 5.0,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        pass

class PromptEnhancerInterface(BaseProvider):
    @abstractmethod
    async def enhance_prompt(
        self,
        prompt: str,
        style: Optional[str] = "photorealistic",
        target_task: str = "text-to-image"
    ) -> Dict[str, Any]:
        pass
