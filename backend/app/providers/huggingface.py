import time
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
from app.providers.base import ImageProviderInterface, VideoProviderInterface, ProviderGenerationResult
from app.providers.registry import get_model_by_id

class ProviderException(Exception):
    def __init__(self, message: str, status_code: int = 500, provider_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.provider_code = provider_code

class ProviderConfigurationError(ProviderException):
    def __init__(self, message: str = "Hugging Face API token is not configured."):
        super().__init__(message=message, status_code=503, provider_code="HF_KEY_MISSING")

class HuggingFaceProvider(ImageProviderInterface, VideoProviderInterface):
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or settings.HF_API_TOKEN
        # Standard Hugging Face serverless router endpoint
        self.base_url = "https://router.huggingface.co/hf-inference/models"
        self.legacy_base_url = "https://api-inference.huggingface.co/models"

    @property
    def provider_name(self) -> str:
        return "huggingface"

    def is_configured(self) -> bool:
        return bool(self.api_token and self.api_token.strip())

    def validate_model(self, model_id: str) -> bool:
        model = get_model_by_id(model_id)
        return model is not None and model.get("provider") == "huggingface"

    def get_capabilities(self, model_id: str) -> Dict[str, Any]:
        model = get_model_by_id(model_id)
        if not model:
            return {}
        return model.get("capabilities_json", {})

    def _get_headers(self) -> Dict[str, str]:
        if not self.is_configured():
            raise ProviderConfigurationError(
                "Hugging Face API token is not configured. Please add HF_API_TOKEN to your server environment or .env file."
            )
        return {
            "Authorization": f"Bearer {self.api_token.strip()}",
            "Accept": "image/png, image/jpeg, video/mp4, application/json",
            "User-Agent": f"GenStudio-AI/{settings.VERSION}"
        }

    async def _post_with_retry(self, url: str, payload: Dict[str, Any], timeout: float = 90.0) -> httpx.Response:
        headers = self._get_headers()
        max_retries = 3
        backoff = 2.0

        async with httpx.AsyncClient(timeout=timeout) as client:
            for attempt in range(max_retries):
                try:
                    response = await client.post(url, json=payload, headers=headers)
                    
                    # 503 Model Loading: Hugging Face cold start
                    if response.status_code == 503 and attempt < max_retries - 1:
                        data = response.json() if "application/json" in response.headers.get("content-type", "") else {}
                        estimated_time = data.get("estimated_time", backoff)
                        time.sleep(min(estimated_time, 5.0))
                        continue

                    # 429 Rate limited
                    if response.status_code == 429 and attempt < max_retries - 1:
                        time.sleep(backoff * (attempt + 1))
                        continue

                    return response
                except httpx.TimeoutException:
                    if attempt == max_retries - 1:
                        raise ProviderException("Inference request timed out after 90 seconds.", status_code=504, provider_code="TIMEOUT")
                    time.sleep(backoff)
                except httpx.RequestError as e:
                    if attempt == max_retries - 1:
                        raise ProviderException(f"Network error communicating with Hugging Face: {str(e)}", status_code=502, provider_code="NETWORK_ERROR")
                    time.sleep(backoff)

        raise ProviderException("Max retries exceeded for Hugging Face inference.", status_code=502)

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
        if not self.validate_model(model_id):
            raise ProviderException(f"Model {model_id} is not supported by Hugging Face provider.", status_code=400)

        model_info = get_model_by_id(model_id) or {}
        capabilities = model_info.get("capabilities_json", {})
        pricing = model_info.get("pricing_json", {})
        cost_usd = pricing.get("cost_per_gen_usd", 0.003)

        payload: Dict[str, Any] = {
            "inputs": prompt,
            "parameters": {}
        }
        
        # Add supported model parameters cleanly
        if capabilities.get("supports_negative_prompt") and negative_prompt:
            payload["parameters"]["negative_prompt"] = negative_prompt
        if seed is not None and capabilities.get("supports_seed"):
            payload["parameters"]["seed"] = seed
        if width and height:
            payload["parameters"]["width"] = width
            payload["parameters"]["height"] = height
        if parameters:
            for k, v in parameters.items():
                if k not in payload["parameters"]:
                    payload["parameters"][k] = v

        url = f"{self.base_url}/{model_id}"
        start_time = time.perf_counter()
        
        response = await self._post_with_retry(url, payload, timeout=120.0)
        latency_ms = (time.perf_counter() - start_time) * 1000.0

        if response.status_code != 200:
            error_msg = response.text
            try:
                err_json = response.json()
                if "error" in err_json:
                    error_msg = err_json["error"]
            except Exception:
                pass
            raise ProviderException(
                f"Hugging Face API returned error ({response.status_code}): {error_msg}",
                status_code=response.status_code,
                provider_code=f"HF_{response.status_code}"
            )

        content_type = response.headers.get("content-type", "image/png").split(";")[0]
        media_bytes = response.content

        return ProviderGenerationResult(
            media_bytes=media_bytes,
            mime_type=content_type,
            latency_ms=round(latency_ms, 2),
            cost_usd=cost_usd,
            width=width,
            height=height,
            metadata={
                "provider": "huggingface",
                "model_id": model_id,
                "prompt": prompt,
                "seed": seed,
                "aspect_ratio": f"{width}:{height}"
            }
        )

    async def transform_image(
        self,
        image_bytes: bytes,
        prompt: str,
        model_id: str,
        strength: float = 0.75,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        import base64
        headers = self._get_headers()
        model_info = get_model_by_id(model_id) or {}
        cost_usd = model_info.get("pricing_json", {}).get("cost_per_gen_usd", 0.005)

        # Instruct-Pix2Pix expects multipart or raw binary + prompt headers
        url = f"{self.base_url}/{model_id}"
        start_time = time.perf_counter()

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                url,
                data=image_bytes,
                headers={
                    **headers,
                    "x-prompt": prompt,
                    "x-strength": str(strength)
                }
            )

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        if response.status_code != 200:
            raise ProviderException(f"Image transformation failed ({response.status_code}): {response.text}", status_code=response.status_code)

        return ProviderGenerationResult(
            media_bytes=response.content,
            mime_type="image/png",
            latency_ms=round(latency_ms, 2),
            cost_usd=cost_usd,
            metadata={"model_id": model_id, "strength": strength, "prompt": prompt}
        )

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
        model_info = get_model_by_id(model_id) or {}
        cost_usd = model_info.get("pricing_json", {}).get("cost_per_gen_usd", 0.045)

        payload = {
            "inputs": prompt,
            "parameters": {
                "num_frames": int(duration_sec * fps),
                "fps": fps,
                "width": width,
                "height": height,
                "seed": seed or 42
            }
        }
        url = f"{self.base_url}/{model_id}"
        start_time = time.perf_counter()

        response = await self._post_with_retry(url, payload, timeout=180.0)
        latency_ms = (time.perf_counter() - start_time) * 1000.0

        if response.status_code != 200:
            raise ProviderException(f"Video generation failed ({response.status_code}): {response.text}", status_code=response.status_code)

        return ProviderGenerationResult(
            media_bytes=response.content,
            mime_type="video/mp4",
            latency_ms=round(latency_ms, 2),
            cost_usd=cost_usd,
            width=width,
            height=height,
            duration_sec=duration_sec,
            metadata={"model_id": model_id, "fps": fps, "duration_sec": duration_sec}
        )

    async def image_to_video(
        self,
        reference_image_bytes: bytes,
        prompt: str,
        model_id: str,
        duration_sec: float = 5.0,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        import base64
        model_info = get_model_by_id(model_id) or {}
        cost_usd = model_info.get("pricing_json", {}).get("cost_per_gen_usd", 0.050)

        b64_image = base64.b64encode(reference_image_bytes).decode("utf-8")
        payload = {
            "inputs": prompt,
            "image": b64_image,
            "parameters": {
                "duration_sec": duration_sec
            }
        }
        url = f"{self.base_url}/{model_id}"
        start_time = time.perf_counter()

        response = await self._post_with_retry(url, payload, timeout=180.0)
        latency_ms = (time.perf_counter() - start_time) * 1000.0

        if response.status_code != 200:
            raise ProviderException(f"Image to video failed ({response.status_code}): {response.text}", status_code=response.status_code)

        return ProviderGenerationResult(
            media_bytes=response.content,
            mime_type="video/mp4",
            latency_ms=round(latency_ms, 2),
            cost_usd=cost_usd,
            duration_sec=duration_sec,
            metadata={"model_id": model_id, "prompt": prompt}
        )
