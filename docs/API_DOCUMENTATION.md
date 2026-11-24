# API Documentation
## GenStudio AI: Comprehensive REST & Server-Sent Events Specification

### Base URL
- Development: `http://localhost:8000/api/v1`
- OpenAPI Specification (Swagger UI): `http://localhost:8000/docs`

---

### Authentication Endpoints

#### `POST /auth/register`
Creates a new researcher account.
- **Request Body:**
  ```json
  {
    "email": "user@university.edu",
    "password": "SecurePassword123!",
    "full_name": "Dr. Researcher"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1Ni...",
    "token_type": "bearer",
    "user": {
      "id": "e4a2b91c-...",
      "email": "user@university.edu",
      "full_name": "Dr. Researcher",
      "role": "USER",
      "is_active": true,
      "created_at": "2026-11-24T11:00:00Z"
    }
  }
  ```

#### `POST /auth/login`
Authenticates user and issues JWT.
- **Request Body:**
  ```json
  {
    "email": "user@university.edu",
    "password": "SecurePassword123!"
  }
  ```
- **Response (200 OK):** Token object with access token and user metadata.

#### `GET /auth/me`
Returns current authenticated user profile. Requires Bearer Token.

---

### Generation Studio Endpoints

#### `POST /studio/image`
Queues a text-to-image synthesis task.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "prompt": "An ethereal glass observatory on an emerald cliff at golden hour",
    "negative_prompt": "blurry, artifacts",
    "model_id": "black-forest-labs/FLUX.1-schnell",
    "aspect_ratio": "16:9",
    "seed": 42,
    "style_preset": "photorealistic",
    "project_id": null,
    "enable_prompt_enhancement": false
  }
  ```
- **Response (202 Accepted):** Generation job record with `status: "pending"`.

#### `POST /studio/video`
Queues a text-to-video generation job.
- **Request Body:**
  ```json
  {
    "prompt": "Cinematic aerial drone flight through misty mountains at sunrise",
    "model_id": "Lightricks/LTX-Video",
    "duration_sec": 5.0,
    "aspect_ratio": "16:9",
    "fps": 24,
    "seed": 100
  }
  ```

#### `POST /studio/image-to-video`
Animates a reference image.
- **Request Body:**
  ```json
  {
    "reference_image_id": "asset-uuid",
    "prompt": "smooth camera pan right",
    "duration_sec": 5.0
  }
  ```

#### `POST /studio/edit`
Executes InstructPix2Pix language-guided image modification.
- **Request Body:**
  ```json
  {
    "base_image_id": "asset-uuid",
    "prompt": "add snow on the trees",
    "strength": 0.75
  }
  ```

#### `POST /studio/enhance-prompt`
Expands a raw prompt with visual descriptors via Gemini 2.0 Flash adapter.
- **Request Body:**
  ```json
  {
    "prompt": "a sports car",
    "style": "cinematic"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "original_prompt": "a sports car",
    "enhanced_prompt": "a sleek silver sports car accelerating down a coastal highway at dusk, 35mm anamorphic lens, motion blur...",
    "suggested_negative_prompt": "blurry, low quality, artifacts",
    "provider": "gemini-2.0-flash",
    "refinements": ["Added camera dynamics", "Applied cinematic lighting"]
  }
  ```

#### `GET /studio/jobs/{job_id}`
Retrieves job status, progress (0-100), latency, and asset references.

#### `GET /studio/jobs/{job_id}/events`
Server-Sent Events (SSE) streaming endpoint for live real-time progress updates.

#### `GET /studio/media/{storage_key:path}`
Streams stored media bytes with appropriate MIME headers and path-traversal safeguards.

---

### Research & Benchmarking Endpoints

#### `POST /experiments/run`
Triggers a reproducible evaluation across target models using fixed prompt benchmark dataset.
- **Request Body:**
  ```json
  {
    "name": "Diffusion Latency Study",
    "target_models": [
      "black-forest-labs/FLUX.1-schnell",
      "stabilityai/stable-diffusion-xl-base-1.0"
    ],
    "prompt_category": "all",
    "sample_size": 5
  }
  ```

#### `POST /experiments/route`
Simulates multi-objective intelligent model routing vs static baseline.
- **Request Body:**
  ```json
  {
    "task_type": "text-to-image",
    "prompt": "Portrait of an elderly watchmaker",
    "priority": "cost",
    "max_budget_usd": 0.05
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "selected_model_id": "black-forest-labs/FLUX.1-schnell",
    "provider": "huggingface",
    "reason": "Model FLUX.1 achieved top utility score under cost policy...",
    "estimated_cost_usd": 0.003,
    "estimated_latency_ms": 1200.0,
    "policy_comparison": {
      "cost_savings_vs_baseline_pct": 50.0,
      "latency_reduction_vs_baseline_pct": 62.5,
      "is_pareto_optimal": true
    }
  }
  ```

#### `GET /experiments/runs/{id}/export/csv`
Downloads benchmark observations as formatted CSV.
