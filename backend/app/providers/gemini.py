import json
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
from app.providers.base import PromptEnhancerInterface

class GeminiPromptEnhancer(PromptEnhancerInterface):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.endpoint_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    @property
    def provider_name(self) -> str:
        return "gemini"

    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    def validate_model(self, model_id: str) -> bool:
        return model_id in ["gemini-2.0-flash", "gemini-1.5-flash"]

    def get_capabilities(self, model_id: str) -> Dict[str, Any]:
        return {
            "supports_negative_prompt_extraction": True,
            "style_adaptation": True,
            "token_budget": 1000
        }

    async def enhance_prompt(
        self,
        prompt: str,
        style: Optional[str] = "cinematic photorealism",
        target_task: str = "text-to-image"
    ) -> Dict[str, Any]:
        # If API key is not configured, apply high-quality deterministic prompt engineering heuristics
        if not self.is_configured():
            return self._heuristic_fallback_enhancement(prompt, style, target_task)

        system_instruction = (
            "You are an expert generative AI prompt engineer for high-end text-to-image and text-to-video diffusion models. "
            "Given a raw user prompt and a desired style, expand and refine it with precise visual descriptors, lighting, textures, "
            "camera angles, and compositional details suitable for models like FLUX.1 and LTX-Video. "
            "Return strictly a valid JSON object with keys: "
            "'enhanced_prompt' (string), 'suggested_negative_prompt' (string or null), 'refinements' (list of strings explaining additions)."
        )

        user_content = f"Raw Prompt: {prompt}\nTarget Style: {style}\nTask Type: {target_task}"

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"{system_instruction}\n\n{user_content}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "responseMimeType": "application/json"
            }
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    f"{self.endpoint_url}?key={self.api_key.strip()}",
                    json=payload
                )
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text_part = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")
                        parsed = json.loads(text_part)
                        return {
                            "original_prompt": prompt,
                            "enhanced_prompt": parsed.get("enhanced_prompt", prompt),
                            "suggested_negative_prompt": parsed.get("suggested_negative_prompt", "blurry, low quality, artifacts, watermark"),
                            "provider": "gemini-2.0-flash",
                            "refinements": parsed.get("refinements", ["Refined visual descriptors", "Enhanced lighting"])
                        }
        except Exception:
            pass

        # Fallback if network or API error occurs
        return self._heuristic_fallback_enhancement(prompt, style, target_task)

    def _heuristic_fallback_enhancement(self, prompt: str, style: Optional[str], target_task: str) -> Dict[str, Any]:
        style = (style or "photorealistic").lower()
        style_additions = {
            "photorealistic": "hyper-detailed textures, 85mm prime lens f/1.4, natural volumetric lighting, cinematic color grading, authentic fine grain",
            "cinematic": "panavision 70mm, anamorphic lens flare, moody atmospheric haze, dramatic chiaroscuro lighting, cinematic masterpiece",
            "artistic": "intricate digital illustration, masterwork concept art, rich dynamic color palette, expressive brushstrokes",
            "anime": "clean line art, Makoto Shinkai aesthetic, vibrant cloudscapes, luminous rim lighting, high-detail anime keyframe",
            "3d_render": "octane render 3D, raytraced reflections, subsurface scattering, ambient occlusion, studio lighting"
        }
        
        addition = style_additions.get(style, style_additions["photorealistic"])
        refined_prompt = f"{prompt.rstrip('. ')}, {addition}"
        
        return {
            "original_prompt": prompt,
            "enhanced_prompt": refined_prompt,
            "suggested_negative_prompt": "blurry, oversaturated, low-res, distorted anatomy, duplicate limbs, watermark, text, out of frame",
            "provider": "gemini-heuristic-adapter",
            "refinements": [
                f"Added {style} camera and lighting descriptors",
                "Applied texture fidelity expansion",
                "Appended tailored negative prompt guardrails"
            ]
        }
