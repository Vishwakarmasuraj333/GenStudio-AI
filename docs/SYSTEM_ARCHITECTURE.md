# System Architecture
## GenStudio AI: Architectural Blueprint & Distributed Design

### 1. High-Level Architecture Overview
GenStudio AI employs a decoupled, asynchronous micro-tier architecture comprising:
1. **Presentation Layer:** Next.js 14 App Router, React 18, TypeScript, Tailwind CSS, Lucide icons.
2. **API & Orchestration Layer:** FastAPI application running on Uvicorn with Pydantic validation, Argon2id security, and async background workers.
3. **Provider Integration Abstraction:** Unified adapter interfaces for Hugging Face Inference Providers, Google Gemini 2.0 Flash, ComfyUI, and offline test fixtures.
4. **Research Engine:** Multi-objective utility router, standardized benchmark dataset, and metrics calculator.
5. **Data & Storage Persistence:** Relational database (SQLite local zero-dependency / PostgreSQL production) managed via SQLAlchemy 2.0 and Alembic migrations, coupled with SHA256-verified local object storage.

### 2. Architecture Diagram (Mermaid)

```mermaid
graph TD
    subgraph ClientLayer ["Client Presentation (Next.js 14 + Tailwind)"]
        UI_Home["Landing & Showcase Page"]
        UI_Studio["Image & Video Studio Workspaces"]
        UI_Bench["Research Benchmark & Router Sandbox"]
        UI_Admin["Governance & Audit Dashboard"]
    end

    subgraph ApiGateway ["FastAPI Core Gateway (:8000)"]
        Router["FastAPI APIRouter (/api/v1)"]
        AuthMid["JWT Auth & Argon2id RBAC"]
        RateLimiter["Request Validation & Magic-Byte Guard"]
    end

    subgraph ServiceLayer ["Service & Research Engine"]
        TaskWorker["Async Background Job Queue"]
        RouterEngine["Intelligent Model Router"]
        BenchRunner["Benchmark Execution Harness"]
        StorageSvc["StorageService (SHA-256 + MIME)"]
    end

    subgraph ProviderAdapters ["Decoupled Provider Adapters"]
        HF_Adapter["HuggingFaceProvider (FLUX.1 / SDXL / LTX-Video)"]
        Gemini_Adapter["GeminiPromptEnhancer (2.0 Flash)"]
        Mock_Adapter["MockTestProvider (Offline Fixture)"]
        Comfy_Adapter["ComfyUIProvider (Node Graph REST)"]
    end

    subgraph DataStorage ["Persistent Data Layer"]
        DB[(SQLAlchemy Relational DB - SQLite / PostgreSQL)]
        MediaDisk["Secure Object Storage Directory (/storage/media)"]
    end

    UI_Home --> Router
    UI_Studio --> Router
    UI_Bench --> Router
    UI_Admin --> Router

    Router --> AuthMid
    AuthMid --> RateLimiter
    RateLimiter --> TaskWorker
    RateLimiter --> RouterEngine
    RateLimiter --> BenchRunner

    TaskWorker --> HF_Adapter
    TaskWorker --> Mock_Adapter
    TaskWorker --> Gemini_Adapter
    TaskWorker --> Comfy_Adapter

    TaskWorker --> StorageSvc
    StorageSvc --> MediaDisk

    TaskWorker --> DB
    BenchRunner --> DB
    Router --> DB
```

### 3. Asynchronous Job Lifecycle Sequence (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor User as Researcher Client
    participant API as FastAPI Gateway
    participant Worker as Background Task Worker
    participant Provider as Hugging Face Hosted Inference
    participant Storage as Storage & Disk
    participant DB as Relational Database

    User->>API: POST /api/v1/studio/image (Prompt, Model, Seed)
    API->>DB: INSERT INTO generation_jobs (status="pending")
    API-->>User: HTTP 202 Accepted (job_id)
    API->>Worker: Dispatch execute_generation_job(job_id)

    Worker->>DB: UPDATE generation_jobs SET status="processing"
    Worker->>Provider: Authenticated Inference Request (POST /models/flux)
    Provider-->>Worker: HTTP 200 OK (Raw Image Bytes)
    
    Worker->>Storage: verify_magic_bytes() & calculate_checksum()
    Storage->>Storage: Save bytes to /media/{hash_prefix}/{hash}.png
    
    Worker->>DB: INSERT INTO media_assets (checksum, file_path, public_url)
    Worker->>DB: UPDATE generation_jobs SET status="completed", latency_ms=1240
    Worker->>DB: INSERT INTO usage_records (cost_usd=0.003)

    User->>API: GET /api/v1/studio/jobs/{job_id} (or SSE Stream)
    API-->>User: HTTP 200 OK (status="completed", assets=[...])
```
