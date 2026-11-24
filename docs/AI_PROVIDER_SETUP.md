# GenStudio AI — AI Provider Setup, Model Registry & Integration Guide

**Date**: November 24, 2026  
**Project**: GenStudio AI (M.Sc. Information Technology Major Project)  
**Target Audience**: Developers, Academic Evaluators, System Administrators.

---

## 1. Overview & Provider Architecture

GenStudio AI is engineered to eliminate local GPU requirements by routing compute-intensive multi-modal generative inference to hosted serverless API providers:
1. **Hugging Face Serverless Router Inference**: High-throughput hosted endpoints powering rectified flow and diffusion transformers for image generation, video synthesis, and language-guided image editing.
2. **Google AI Studio (Gemini 2.0 Flash)**: Ultra-low latency visual prompt refinement, lens dynamics parameter expansion, and automatic negative prompt extraction.
3. **Local ComfyUI (Optional)**: Optional self-hosted REST/WebSocket bridge for local diffusion clusters when available.

---

## 2. Execution Modes (`PROVIDER_MODE`)

The application supports three distinct operational modes defined in the backend configuration (`.env`):

| Mode | Environment Value | Behavior on Missing Credentials | Media Output Guarantee | Intended Use Case |
|---|---|---|---|---|
| **Live Inference** | `PROVIDER_MODE=live` (Default) | Fails immediately with HTTP 400 or Job `failed` status explaining exact missing token. | Real provider-synthesized media only. **Zero dummy media emitted.** | Production execution & live benchmark evaluation. |
| **Test Fixtures** | `PROVIDER_MODE=test` | Generates deterministic lightweight synthetic test fixtures. | Minimal valid binary media stamped with `test_mode=True`. | Automated unit and integration test suites (`pytest`). |
| **Offline Preview** | `PROVIDER_MODE=offline-preview` | Generates labeled simulation fixtures for UI inspection. | Outputs explicitly stamped in database metadata with `is_offline_preview=True`. UI renders prominent `[OFFLINE PREVIEW]` badges. | Offline academic defense presentations & UI testing without internet access. |

---

## 3. Supported Model Registry & Capability Specifications

### 3.1 Text-to-Image Synthesis

#### Model: FLUX.1 [schnell]
- **Exact Model ID**: `black-forest-labs/FLUX.1-schnell`
- **Provider**: Hugging Face Inference Providers
- **Architecture**: 12-Billion Parameter Rectified Flow Transformer (Flow Matching)
- **Default Resolution**: `1024x1024` (also supports `768x768`, `512x512`)
- **Inference Steps**: 4 steps (distilled ultra-fast synthesis)
- **P50 Latency**: ~1.4 seconds (warm serverless endpoint)
- **Pass-through Rate Card**: ~$0.003 USD / generation
- **License**: Apache 2.0 (Commercial & Academic permitted)
- **Strengths**: Leading typographical text rendering inside images, photorealistic lighting, prompt adherence.

#### Model: Stable Diffusion XL 1.0 Base
- **Exact Model ID**: `stabilityai/stable-diffusion-xl-base-1.0`
- **Provider**: Hugging Face Inference Providers
- **Architecture**: Latent Diffusion Model (Ensemble diffusion)
- **Default Resolution**: `1024x1024`
- **Inference Steps**: 30 steps
- **P50 Latency**: ~3.2 seconds
- **Pass-through Rate Card**: ~$0.006 USD / generation
- **License**: OpenRAIL++
- **Strengths**: Rich cinematic styling, wide artistic versatility, negative prompt guidance.

---

### 3.2 Video Generation (Text-to-Video & Image-to-Video)

#### Model: LTX-Video
- **Exact Model ID**: `Lightricks/LTX-Video`
- **Provider**: Hugging Face Inference Providers
- **Architecture**: Real-Time Diffusion Transformer (DiT) for Video
- **Supported Tasks**: `text-to-video`, `image-to-video` (animates reference image)
- **Frame Rate**: 24 FPS
- **Resolution**: `1280x720` or `768x512`
- **Duration**: Up to 5.0 seconds per request
- **Pass-through Rate Card**: ~$0.045 USD / generation
- **Output Container**: Validated H.264 / MP4 stream
- **License**: Apache 2.0

---

### 3.3 Image Editing (Image-to-Image)

#### Model: InstructPix2Pix
- **Exact Model ID**: `timbrooks/instruct-pix2pix`
- **Provider**: Hugging Face Inference Providers
- **Architecture**: Conditional Latent Diffusion with Language Guidance
- **Input Requirements**: Valid reference image (`.png` or `.jpeg`, max 25MB) + natural language editing instruction (e.g. "Add heavy snowfall to the scene", "Make it look like a pencil sketch").
- **Parameters**: `image_guidance_scale` (1.5 default), `strength` (0.75 default).
- **Resolution**: `512x512`
- **Pass-through Rate Card**: ~$0.005 USD / generation
- **License**: CreativeML OpenRAIL-M

---

### 3.4 Visual Prompt Refinement & Expansion

#### Model: Gemini 2.0 Flash
- **Exact Model ID**: `gemini-2.0-flash`
- **Provider**: Google AI Studio
- **Architecture**: Multimodal Generative LLM
- **Task**: Expands sparse user prompts (e.g. "a cat") into detailed photographic descriptions including lighting conditions, camera lens specifications (e.g. 85mm f/1.4), volumetric atmosphere, and negative prompt guardrails.
- **Latency**: < 350ms
- **Pass-through Rate Card**: ~$0.0001 USD / prompt expansion
- **Fallback Engine**: If `GEMINI_API_KEY` is not present, the platform automatically activates a local domain-rule heuristic expansion engine so users can continue refining prompts without interruption.

---

## 4. Setup & Configuration Instructions

### 4.1 Obtaining Provider API Keys

#### 1. Hugging Face Access Token (`HF_API_TOKEN`)
1. Create a free account at [huggingface.co](https://huggingface.co).
2. Navigate to **Settings** → **Access Tokens**.
3. Create a new token with **Read** permissions (sufficient for inference endpoints).
4. Copy the token starting with `hf_...`.

#### 2. Google AI Studio Key (`GEMINI_API_KEY`)
1. Navigate to [aistudio.google.com](https://aistudio.google.com).
2. Sign in with your Google account.
3. Click **Get API key** and generate a free API key.

---

### 4.2 Setting Environment Variables

In the project root, copy `.env.example` to `.env`:
```ini
# Operational Mode: live | test | offline-preview
PROVIDER_MODE=live

# Hugging Face User Access Token
HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google Gemini API Key
GEMINI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Local Database
DATABASE_URL=sqlite:///./genstudio.db
```

---

## 5. Verification & Testing

### How to Test in Live Mode:
1. Ensure `HF_API_TOKEN` is configured in `.env`.
2. Start the backend: `uvicorn app.main:app --reload`.
3. Check the health status:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
   Verify `"providers_configured": {"huggingface": true}`.
4. Open the studio at `http://localhost:3000/studio/image`. The header will show an emerald badge: `HF Live Active`.
5. Submit a prompt: "An astronaut exploring a neon crystalline cavern, 8k resolution". The server dispatches to FLUX.1 [schnell] and persists the genuine PNG.

### How to Test Missing Credentials Handling:
1. Clear `HF_API_TOKEN` from `.env` and restart the backend with `PROVIDER_MODE=live`.
2. Visit `http://localhost:3000/studio/image`.
3. The UI will display an amber banner:
   > **Provider Configuration Required**: Hugging Face API token (`HF_API_TOKEN`) is not configured in the server environment. Live inference requests cannot proceed.
4. The generation button is safely disabled, preventing doomed API submissions.
5. If an API request is submitted directly via curl, the job immediately enters `failed` status with an honest sanitized error message:
   ```
   Provider Configuration Required: Hugging Face API token (HF_API_TOKEN) is not configured. Live inference cannot proceed.
   ```
   **Zero fake images or videos are generated.**

### How to Test in Offline Preview Mode:
1. Set `PROVIDER_MODE=offline-preview` in `.env`.
2. Restart backend.
3. The studio interface and all generated media cards will clearly display the teal `[OFFLINE PREVIEW]` badge. All benchmark runs are explicitly labeled as synthetic fixtures.
