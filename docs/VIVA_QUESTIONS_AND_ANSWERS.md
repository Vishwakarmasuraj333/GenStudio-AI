# Viva Voce Questions & Answers
## Comprehensive M.Sc. IT Major Project Defense Guide

This document contains 25 rigorous, high-scoring technical viva voce questions and answers covering generative AI architecture, system design, database persistence, security, and research methodology.

---

### Section 1: Generative AI & Deep Learning Concepts

#### Q1: What is the primary architectural difference between Latent Diffusion Models (SDXL) and Rectified Flow Transformers (FLUX.1)?
**Answer:**  
Standard Latent Diffusion Models (like SDXL) use a U-Net backbone to predict and subtract noise across a curved Gaussian trajectory using discrete Markovian sampling steps (typically 25–50 steps). In contrast, FLUX.1 utilizes a Diffusion Transformer (DiT) architecture with a Rectified Flow matching formulation. Rectified flow trains the network to model straight vector field paths between noise and data distributions. Because the vector trajectories are linear rather than curved, FLUX.1 [schnell] generates high-fidelity images in as few as 4 sampling steps with superior text rendering and prompt adherence.

#### Q2: How does GenStudio AI handle video synthesis without causing subject distortion across frames?
**Answer:**  
GenStudio AI integrates diffusion transformer video architectures (such as Lightricks LTX-Video). Rather than generating independent 2D frames and interpolating between them (which causes flickering and unnatural morphing), LTX-Video processes temporal 3D latent tokens using causal space-time cross-attention. This conditions generation on the underlying motion dynamics and optical flow manifold, guaranteeing temporal coherence across all 24 frames per second.

#### Q3: Why does GenStudio AI use Gemini 2.0 Flash for prompt enhancement instead of traditional string templates?
**Answer:**  
Traditional string templates append generic static suffixes (e.g. "photorealistic, 4k, hyper-detailed") that frequently contradict model attention or produce oversaturated artifacts. Gemini 2.0 Flash acts as an intelligent prompt engineer: it analyzes the user's semantic intent, injects lens and lighting parameters (e.g., 85mm prime lens, chiaroscuro lighting), and constructs dynamic negative prompt guardrails tailored to the target task.

---

### Section 2: System Architecture & Distributed Processing

#### Q4: How does GenStudio AI run on a laptop without an expensive NVIDIA GPU?
**Answer:**  
The application is architected around hosted serverless inference APIs (Hugging Face Inference Providers and Google AI Studio). The computational burden of evaluating 12-billion parameter models is executed on cloud infrastructure. The local laptop only runs the lightweight FastAPI application server, database persistence, and Next.js frontend, ensuring seamless operation on any consumer machine.

#### Q5: Why is video generation decoupled into an asynchronous background queue?
**Answer:**  
Video synthesis requires between 10 to 60 seconds depending on duration and model complexity. If processed synchronously within an HTTP request-response cycle, the client connection would encounter HTTP 504 gateway timeouts, and server worker threads would be blocked. GenStudio AI returns an immediate `HTTP 202 Accepted` response with a unique job ID, offloading execution to an asynchronous background worker, and providing real-time status updates via polling or Server-Sent Events (SSE).

#### Q6: How does the system guarantee that a video is never falsely reported as completed?
**Answer:**  
In `worker.py`, when a provider completes an inference task, the raw bytes are intercepted before the database is updated. The `StorageService` verifies the file signature (magic bytes `ftyp` box for MP4) and computes the SHA-256 checksum. Only when the media asset is written to disk and validated does the worker set `job.status = "completed"`. If corrupted bytes are returned, the job transitions to `FAILED` with an actionable error.

---

### Section 3: Research Benchmarking & Intelligent Routing

#### Q7: Explain the mathematical objective function of the Intelligent Model Router.
**Answer:**  
The router solves a constrained multi-objective utility optimization problem:
$$m^* = \arg\max_{m \in \mathcal{M}} \left[ w_{\text{cost}} U_{\text{cost}}(m) + w_{\text{speed}} U_{\text{speed}}(m) + w_{\text{quality}} U_{\text{quality}}(m) + w_{\text{rel}} U_{\text{rel}}(m) \right]$$
subject to hard user constraints: $\text{Cost}(m) \le B_{\max}$ and $\text{Latency}(m) \le L_{\max}$. The utilities normalize costs against maximum thresholds, allowing the system to switch dynamically between speed, cost, and visual quality priorities.

#### Q8: How does the intelligent router compare against a static baseline?
**Answer:**  
In empirical experiments, a static policy hard-codes SDXL 1.0 for all queries (\$0.006 per generation, ~3200ms latency). The intelligent router under a 'cost' or 'speed' priority dynamically routes requests to FLUX.1 [schnell] (\$0.003 per generation, ~1200ms latency), achieving an empirical 50% cost reduction and 62.5% latency reduction while achieving higher typography fidelity.

#### Q9: What are the 6 domains of the GenStudio-Bench-v1 dataset?
**Answer:**  
1. Photorealism (macro textures, skin tones)
2. Spatial Composition (occlusion, positional left/right relation)
3. Typography & Text (spelling accuracy, sign carving)
4. Cinematic Aesthetics (anamorphic flares, color grading)
5. Stylized Art (brushstrokes, surrealism)
6. Motion Dynamics (fluid flow, high-speed camera tracking)

---

### Section 4: Database Design & Security

#### Q10: Why did you choose Argon2id over bcrypt or MD5 for password hashing?
**Answer:**  
Argon2id is the winner of the Password Hashing Competition (PHC) and the modern standard (RFC 9106). Unlike bcrypt, Argon2id provides configurable memory-hardness and time-hardness parameters, rendering it resilient against GPU, ASIC, and side-channel timing attacks.

#### Q11: How does GenStudio AI prevent malicious file upload vulnerabilities?
**Answer:**  
Client-supplied MIME types and file extensions are never trusted. Uploaded files are inspected for their binary file signatures (magic bytes): PNG must start with `\x89PNG\r\n\x1a\n`, JPEG with `\xff\xd8\xff`, and MP4 with `ftyp`. Additionally, file size is capped at 25MB, file paths are sanitized against directory traversal attacks (`../`), and files are stored with random SHA-256 names.

#### Q12: How are database migrations managed?
**Answer:**  
Database schema revisions are managed using Alembic (`001_initial_schema.py`). Every table, index, and foreign key constraint is tracked declaratively with reversible `upgrade()` and `downgrade()` routines.
