# GenStudio AI
## Advanced AI Image & Video Generation Research Platform
### M.Sc. IT Major Project Thesis & Full-Stack System

[![CI Pipeline](https://github.com/suraj/genstudio-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/suraj/genstudio-ai/actions)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![Tests Passing](https://img.shields.io/badge/Pytest-38%2F38%20Passed-brightgreen.svg)](docs/FINAL_INDEPENDENT_AUDIT.md)

---

### Executive Overview
**GenStudio AI** is an original, production-grade full-stack generative AI research platform engineered for academic evaluation, empirical benchmarking, and live demonstration. It unifies state-of-the-art hosted diffusion and flow-matching models with a reproducible evaluation harness and a multi-objective intelligent model routing engine.

Crucially, **the application runs on standard consumer laptops without a dedicated NVIDIA GPU** by dispatching compute-intensive inference to hosted serverless endpoints (Hugging Face Inference Providers and Google Gemini 2.0 Flash) while managing local database persistence, background queues, and media verification.

---

### Key Capabilities

1. **Text-to-Image Synthesis:** FLUX.1 [schnell] (12B Rectified Flow Transformer) & SDXL Base 1.0 at 1024x1024 resolution with seed control and multi-aspect ratios.
2. **Video Generation:** LTX-Video Diffusion Transformer (24fps MP4) supporting text-to-video and reference image-to-video animation.
3. **Image Transformation:** Language-guided editing using Instruct-Pix2Pix with strength modulation.
4. **AI Prompt Enhancement:** Gemini 2.0 Flash integration with automatic negative prompt extraction and heuristic fallback engine.
5. **Intelligent Model Router:** Constrained multi-objective utility optimization ($w_c U_c + w_s U_s + w_q U_q + w_r U_r$) achieving up to 50% cost and 62.5% latency reductions compared to static baselines.
6. **Empirical Benchmarks:** Standardized 6-domain prompt benchmark (`GenStudio-Bench-v1`) measuring median/p90/p95 latency and cost, with one-click CSV and JSON exports.
7. **Production Security:** Zero browser-exposed API keys, Argon2id password hashing, JWT HS256 auth, server-side RBAC, IDOR protection, and binary magic-byte upload validation.
8. **Three Explicit Execution Modes:** `live` (strict external inference, no fake outputs), `test` (isolated fixtures for pytest), and `offline-preview` (clearly labeled UI simulations).

---

### Project Architecture

```
genstudio-ai/
├── backend/
│   ├── app/
│   │   ├── api/             # REST routes (/auth, /studio, /projects, /experiments, /admin)
│   │   ├── core/            # Config, Argon2id security, logging, SQLite/PostgreSQL engine
│   │   ├── models/          # Normalized SQLAlchemy models (User, Job, MediaAsset, etc.)
│   │   ├── providers/       # Adapters: Hugging Face, Gemini, ComfyUI, Mock test fixture
│   │   ├── research/        # 6-Domain dataset, statistical metrics calculator, router
│   │   ├── storage/         # SHA-256 integrity, magic-byte inspection, file serving
│   │   ├── tasks/           # Asynchronous worker with cancellation and verified delivery
│   │   └── main.py          # FastAPI application & startup seed routines
│   ├── alembic/             # Database migrations (001_initial_schema.py - idempotent)
│   ├── tests/               # 38 Pytest unit and integration tests (100% passing)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js 14 App Router (23 verified routes)
│   │   ├── components/      # UI components, responsive Sidebar, Header, Navbar, Footer
│   │   ├── lib/             # Typed API client, AuthContext, data schemas
│   │   └── styles/          # Tailwind CSS with studio dark palette & touch targets
│   └── package.json
├── docs/                    # Complete Engineering & Academic Documentation
│   ├── FINAL_INDEPENDENT_AUDIT.md
│   ├── FEATURE_VERIFICATION_MATRIX.md
│   ├── RESPONSIVE_QA_REPORT.md
│   ├── SECURITY_AUDIT.md
│   ├── AI_PROVIDER_SETUP.md
│   ├── ACADEMIC_RESEARCH_METHODOLOGY.md
│   └── VIVA_QUESTIONS_AND_ANSWERS.md
├── docker-compose.yml       # Production deployment with PostgreSQL and Redis
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example
└── README.md
```

---

### Quick Start & Local Execution

#### Prerequisites
- Node.js 18+ (tested on Node v24.20.0)
- Python 3.10+ (tested on Python 3.12.10)
- Windows, macOS, or Linux (No NVIDIA GPU required)

#### 1. Setup Backend
```powershell
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv ../venv
..\venv\Scripts\activate   # On Windows (or source ../venv/bin/activate on Unix)

# Install dependencies
pip install -r requirements.txt

# Run database migrations (idempotent across new and existing databases)
alembic upgrade head

# Run all automated tests (38/38 passing)
pytest -v

# Start FastAPI server on port 8000
uvicorn app.main:app --reload --port 8000
```
The backend API is now running at `http://localhost:8000` with interactive Swagger docs at `http://localhost:8000/docs`.

#### 2. Setup Frontend
```powershell
# In a separate terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Build production bundle (verifies all 23 routes)
npm run build

# Start Next.js server
npm run start   # or 'npm run dev' for development
```
The studio interface is accessible at `http://localhost:3000`.

---

### Environment Variables (.env)

Configure server credentials in `.env` (or copy `.env.example`):
```env
# Operational Mode: live | test | offline-preview
# - live: real external inference (fails honestly if keys missing; zero fake output)
# - offline-preview: clearly labeled simulation mode for offline demo
# - test: deterministic fixtures for automated pytest suite
PROVIDER_MODE=live

# Optional Third-Party Keys (Required for Live External Inference)
HF_API_TOKEN=hf_your_hugging_face_token_here
GEMINI_API_KEY=your_gemini_api_key_from_google_ai_studio

# Database (Default: Zero-dependency local SQLite)
DATABASE_URL=sqlite:///./genstudio.db

# JWT Security
JWT_SECRET=your_super_secret_jwt_key_here
```

---

### Verification and Academic Evaluation

- **Automated Test Suite:** Execute `pytest -v` inside `backend/` to verify all 38 tests covering authentication, RBAC, background job lifecycle, media checksums, path traversal protection, and IDOR isolation.
- **Controlled Benchmarking:** Navigate to `http://localhost:3000/experiments` to run the standardized 6-domain benchmark and export empirical CSV/JSON results.
- **Comprehensive Documentation:**
  - [docs/FINAL_INDEPENDENT_AUDIT.md](docs/FINAL_INDEPENDENT_AUDIT.md) — Comprehensive technical audit.
  - [docs/FEATURE_VERIFICATION_MATRIX.md](docs/FEATURE_VERIFICATION_MATRIX.md) — Feature status ledger.
  - [docs/RESPONSIVE_QA_REPORT.md](docs/RESPONSIVE_QA_REPORT.md) — Viewport audit (320px–1920px).
  - [docs/SECURITY_AUDIT.md](docs/SECURITY_AUDIT.md) — Security & vulnerability remediation.
  - [docs/AI_PROVIDER_SETUP.md](docs/AI_PROVIDER_SETUP.md) — Provider setup & rate cards.
  - [docs/ACADEMIC_RESEARCH_METHODOLOGY.md](docs/ACADEMIC_RESEARCH_METHODOLOGY.md) — Thesis methodology & dataset.
  - [docs/VIVA_QUESTIONS_AND_ANSWERS.md](docs/VIVA_QUESTIONS_AND_ANSWERS.md) — 25 defense questions.
