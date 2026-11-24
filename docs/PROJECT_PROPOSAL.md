# M.Sc. Information Technology Major Project Proposal
## GenStudio AI: Advanced AI Image & Video Generation Research Platform

**Project Title:** Comparative Evaluation and Intelligent Routing of Hosted Generative AI Models for Text-to-Image and Image-to-Video Synthesis  
**Short Name:** GenStudio AI  
**Academic Degree:** Master of Science in Information Technology (M.Sc. IT)  
**Academic Year:** 2026  
**Candidate Name:** Suraj  
**Domain:** Generative Artificial Intelligence, Deep Learning, Cloud Systems, Distributed Systems  

---

### 1. Introduction & Background
Recent breakthroughs in deep generative modeling—specifically Rectified Flow Transformers (e.g., FLUX.1) and Latent Diffusion Transformers (e.g., LTX-Video)—have radically elevated synthetic visual fidelity, text rendering, and temporal coherence. However, for real-world researchers, students, and practitioners operating on consumer hardware lacking expensive multi-GPU clusters, running multi-billion parameter diffusion models locally is prohibitive. Furthermore, hosted inference APIs exhibit wide variances in latency, per-generation pricing, prompt alignment, and availability.

### 2. Proposed Work
GenStudio AI is a full-stack, production-grade generative AI research studio that unifies:
1. Hosted serverless inference for computationally intensive text-to-image and image-to-video generation.
2. A standardized 6-domain prompt benchmark harness for reproducible empirical evaluation.
3. An intelligent multi-objective model routing engine balancing user constraints (budget, latency, quality, reliability) against baseline static defaults.
4. Complete verifiable telemetry, asset management, and rigorous academic reporting.

### 3. Expected Outcomes
- Working web studio application built with Next.js 14 and FastAPI.
- Validated serverless inference adapters for FLUX.1, SDXL, LTX-Video, and Gemini 2.0 Flash.
- Fully normalized relational schema with Alembic migrations.
- Reproducible benchmarking suite producing CSV/JSON datasets.
- Comprehensive thesis and viva defense documentation.
