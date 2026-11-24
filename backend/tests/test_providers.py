import pytest
from app.providers.huggingface import HuggingFaceProvider, ProviderConfigurationError
from app.providers.gemini import GeminiPromptEnhancer
from app.providers.mock_provider import MockTestProvider
from app.providers.registry import CURATED_MODELS, get_model_by_id

def test_model_registry_loaded():
    assert len(CURATED_MODELS) >= 5
    flux = get_model_by_id("black-forest-labs/FLUX.1-schnell")
    assert flux is not None
    assert flux["provider"] == "huggingface"
    assert "text-to-image" in flux["task_types"]

def test_huggingface_unconfigured_raises_explicit_error():
    # When api_token is None or empty, must raise ProviderConfigurationError
    hf = HuggingFaceProvider(api_token=None)
    with pytest.raises(ProviderConfigurationError) as exc_info:
        hf._get_headers()
    assert "Hugging Face API token is not configured" in str(exc_info.value)

@pytest.mark.asyncio
async def test_mock_provider_deterministic_output():
    mock = MockTestProvider()
    res = await mock.generate_image(
        prompt="Test prompt",
        model_id="black-forest-labs/FLUX.1-schnell",
        width=512,
        height=512
    )
    assert res.mime_type == "image/png"
    assert res.media_bytes.startswith(b"\x89PNG")
    assert res.latency_ms > 0
    assert res.cost_usd > 0

@pytest.mark.asyncio
async def test_gemini_prompt_enhancer_heuristic_fallback():
    enhancer = GeminiPromptEnhancer(api_key=None)
    res = await enhancer.enhance_prompt(
        prompt="cyberpunk detective",
        style="cinematic"
    )
    assert "cyberpunk detective" in res["enhanced_prompt"]
    assert "suggested_negative_prompt" in res
    assert res["provider"] == "gemini-heuristic-adapter"
