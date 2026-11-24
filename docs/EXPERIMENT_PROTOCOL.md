# Experiment Protocol
## GenStudio AI: Step-by-Step Benchmarking & Verification Protocol

### 1. Dataset Specification: GenStudio-Bench-v1
The benchmark dataset consists of standardized prompts spanning 6 challenging domains:
1. **Photorealism (PHOTO):** Extreme texture detail, macro lenses, skin rendering, volumetric sunlight.
2. **Spatial Composition (SPAT):** Relative object placement (left/right, foreground/background), complex occlusions.
3. **Cinematic Aesthetics (CINE):** Anamorphic lenses, 70mm grain, dramatic chiaroscuro lighting.
4. **Typography & Text Rendering (TYPO):** Legible signage, neon text, correct character spelling.
5. **Stylized Art (ART):** Complex brushstrokes, surreal geometry, oil-on-canvas rendering.
6. **Motion Dynamics (VID):** High-velocity camera motion, fluid dynamics for video diffusion.

### 2. Execution Procedure
1. Initialize test database and ensure all 6 curated models are registered in `model_registry`.
2. Configure credentials in `.env` (or run in deterministic fixture mode if credentials are unconfigured).
3. Execute benchmark harness via API (`POST /api/v1/experiments/run`) or Python runner script.
4. The harness dispatches sequential prompt requests across all target models under identical seeds.
5. Record start time, completion time, raw media bytes, SHA256 checksum, and status.
6. Compute summary metrics: median latency, p90 latency, p95 latency, success rate, cost per success.
7. Export dataset to CSV and JSON formats for external statistical verification.
