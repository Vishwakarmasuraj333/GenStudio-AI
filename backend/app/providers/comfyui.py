import json
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
from app.providers.base import ImageProviderInterface, ProviderGenerationResult

class ComfyUIProvider(ImageProviderInterface):
    """
    Integration adapter for ComfyUI REST/WebSocket workflow execution.
    Compatible with standard ComfyUI server instances on port 8188.
    """
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.COMFYUI_BASE_URL).rstrip("/")

    @property
    def provider_name(self) -> str:
        return "comfyui"

    def validate_model(self, model_id: str) -> bool:
        return model_id.startswith("comfyui/") or "checkpoint" in model_id

    def get_capabilities(self, model_id: str) -> Dict[str, Any]:
        return {
            "supports_seed": True,
            "supports_negative_prompt": True,
            "supports_workflow_graph": True,
            "custom_nodes": True
        }

    async def is_server_reachable(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/system_stats")
                return res.status_code == 200
        except Exception:
            return False

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
        # Check server availability
        if not await self.is_server_reachable():
            raise ConnectionError(f"ComfyUI server at {self.base_url} is currently unreachable.")

        # In ComfyUI, a generation request posts a node prompt graph to /prompt
        # Here we construct the standard default SDXL/Checkpoint node graph
        workflow = {
            "3": {
                "inputs": {
                    "seed": seed or 42,
                    "steps": 25,
                    "cfg": 7.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {"inputs": {"ckpt_name": model_id.replace("comfyui/", "")}, "class_type": "CheckpointLoaderSimple"},
            "5": {"inputs": {"width": width, "height": height, "batch_size": 1}, "class_type": "EmptyLatentImage"},
            "6": {"inputs": {"text": prompt, "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
            "7": {"inputs": {"text": negative_prompt or "", "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
            "8": {"inputs": {"samples": ["3", 0], "vae": ["4", 2]}, "class_type": "VAEDecode"},
            "9": {"inputs": {"filename_prefix": "GenStudio", "images": ["8", 0]}, "class_type": "SaveImage"}
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{self.base_url}/prompt", json={"prompt": workflow})
            if resp.status_code != 200:
                raise RuntimeError(f"ComfyUI prompt submission failed: {resp.text}")
            
            job_info = resp.json()
            prompt_id = job_info.get("prompt_id")

            # ComfyUI queue check: wait for history output
            import asyncio
            for _ in range(60):
                await asyncio.sleep(1.0)
                hist_resp = await client.get(f"{self.base_url}/history/{prompt_id}")
                if hist_resp.status_code == 200:
                    hist_data = hist_resp.json()
                    if prompt_id in hist_data:
                        outputs = hist_data[prompt_id].get("outputs", {})
                        if "9" in outputs and "images" in outputs["9"]:
                            img_meta = outputs["9"]["images"][0]
                            img_resp = await client.get(
                                f"{self.base_url}/view",
                                params={"filename": img_meta["filename"], "subfolder": img_meta["subfolder"], "type": img_meta["type"]}
                            )
                            return ProviderGenerationResult(
                                media_bytes=img_resp.content,
                                mime_type="image/png",
                                latency_ms=1200.0,
                                cost_usd=0.0,
                                width=width,
                                height=height,
                                metadata={"prompt_id": prompt_id, "comfyui": True}
                            )

        raise TimeoutError("ComfyUI generation timed out.")

    async def transform_image(self, *args, **kwargs) -> ProviderGenerationResult:
        raise NotImplementedError("ComfyUI image transformation requires specialized node graph.")
