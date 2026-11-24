# GenStudio AI — Academic Research Methodology & Empirical Benchmarking Protocol

**Candidate**: Suraj (M.Sc. Information Technology)  
**Thesis Title**: Comparative Evaluation and Intelligent Routing of Hosted Generative AI Models for Text-to-Image and Image-to-Video Synthesis  
**Evaluation Standard**: Verifiable Empirical Records, Strict Execution Isolation, Reproducible Scientific Dataset.

---

## 1. Research Objectives & Motivation

### 1.1 The Hardware Bottleneck in Generative AI Research
State-of-the-art vision generative models—specifically 12B rectified flow transformers (FLUX.1) and temporal diffusion transformers (LTX-Video)—require upwards of 24GB–48GB of high-bandwidth VRAM (e.g. NVIDIA A100/H100) to execute unquantized inference. Standard non-GPU workstations and university laptops cannot run these models locally without severe out-of-memory crashes or unviable latency.

### 1.2 Core Research Contributions
This project designs, implements, and empirically validates **GenStudio AI**, addressing three foundational research questions:
1. **Can multi-modal creative generation pipelines be effectively decoupled from local GPU hardware?**  
   *Yes*: By engineering a thin, secure client architecture dispatching to hosted serverless inference routers while preserving local database persistence and media integrity verification.
2. **How do rectified flow matching models (FLUX.1) compare against latent diffusion models (SDXL 1.0) across distinct visual challenge domains?**  
   *Methodology*: Through a fixed, standardized 6-domain prompt benchmark (`GenStudio-Bench-v1`) measuring empirical latency, cost per success, and typographical adherence.
3. **Can an automated multi-objective decision policy (Intelligent Router) reduce aggregate inference costs and latency while adhering to budget constraints?**  
   *Methodology*: By formulating a constrained utility function $U(m) = w_c U_c(m) + w_s U_s(m) + w_q U_q(m) + w_r U_r(m)$ and proving Pareto optimality against static single-model dispatch policies.

---

## 2. Standardized Benchmark Dataset (`GenStudio-Bench-v1`)

To guarantee rigorous scientific reproducibility, all evaluation experiments utilize `GenStudio-Bench-v1`, a fixed, curated suite of evaluation prompts spanning 6 critical domains:

| Domain Category | Specific Visual Challenge Evaluated | Benchmark Prompts Count | Key Evaluation Target |
|---|---|---|---|
| **Photorealism** | Human micro-texture, skin porosity, subsurface scattering, ambient natural illumination | 5 prompts | Elimination of waxy "AI plastic" skin textures |
| **Spatial Composition** | Left/right relational layout, foreground/background occlusion, multi-object counts | 5 prompts | Spatial attention binding adherence |
| **Typography & Text** | Accurate spelling of embedded words, neon signs, t-shirt slogans, letter kerning | 5 prompts | Flow-matching rectified token adherence |
| **Cinematic Aesthetics** | Anamorphic lens distortion, 35mm film grain, volumetric fog, dramatic chiaroscuro | 5 prompts | Contrast dynamics & optical lens simulation |
| **Artistic Rendering** | Impasto oil painting, linocut printing, watercolor wash, architectural ink sketch | 5 prompts | Stylistic medium fidelity |
| **Motion Dynamics (Video)** | Fluid wave motion, temporal object permanence, natural camera tracking pan | 5 prompts | Optical flow coherence across 24 FPS frames |

All benchmark prompts are defined in [dataset.py](file:///c:/Users/imdee/.gemini/antigravity/scratch/genstudio-ai/backend/app/research/dataset.py) and cannot be altered during automated runs.

---

## 3. Evaluation Metrics Formulation

1. **Percentile Latency ($P_{50}, P_{90}, P_{95}$)**:
   Measures end-to-end turnaround latency from request dispatch to binary image validation and disk persistence.
   $$\text{P-th Percentile} = v_{\lfloor \frac{P}{100} \cdot (N - 1) \rfloor}$$
2. **Cost per Success (CPS)**:
   Accounts for provider failure waste by allocating billed costs strictly across successful generations:
   $$\text{CPS} = \frac{\sum_{i=1}^N \text{Cost}(i)}{N_{\text{success}}}$$
3. **Empirical Success Rate ($R_s$)**:
   Ratio of completed, byte-validated generations to total attempted requests:
   $$R_s = \frac{N_{\text{success}}}{N_{\text{total}}}$$
4. **Intelligent Router Multi-Objective Utility Function**:
   $$U(m) = w_c \left(1 - \frac{C_m}{C_{\max}}\right) + w_s \left(1 - \frac{L_m}{L_{\max}}\right) + w_q Q_m + w_r R_m$$
   - $w_c, w_s, w_q, w_r$: Weights for cost, speed, quality, and reliability (sum = 1.0).
   - $C_m, L_m$: Estimated cost and historical P50 latency of model $m$.
   - $Q_m, R_m$: Domain quality weight and empirical success rate.

---

## 4. Academic Honesty Standard & Data Contamination Safeguards

### Mandatory Rules for Research Integrity:
1. **Zero Fabricated Metrics**: No evaluation metric (latency, cost, success rate) is ever fabricated or simulated in live mode.
2. **No Fake CLIP / Alignment Scores**: Automated ML image-text alignment metrics (such as CLIP score or aesthetic predictor) are only computed if a genuine local or remote model is loaded and executed. In standard mode, similarity metrics are omitted or derived from user human-eval feedback rather than invented numbers.
3. **Execution Isolation**: Runs conducted in `offline-preview` mode are explicitly stamped in database metadata with `is_offline_preview=True` and flagged with `[Offline Preview Simulation - Synthetic Test Fixtures]` in all exported tables. Preview simulations can never contaminate live research datasets.
4. **Export Integrity**: Exported CSV and JSON files are generated directly from persistent database records in the `evaluation_runs` and `evaluation_results` tables.

---

## 5. Limitations & Future Scope

1. **Third-Party Inference Queue Latency**: In live mode, latency is subject to upstream serverless cold starts on Hugging Face infrastructure. While P50 warm latency is ~1.4s for FLUX.1 [schnell], cold starts can take up to 25s.
2. **Human Evaluation Sample Size**: Subjective visual quality evaluation currently relies on registered researcher feedback. Future iterations will integrate crowdsourced pairwise Arena comparisons (Elo rating system).
3. **Video Duration Constraints**: Current serverless video models generate up to 5 seconds of continuous 24fps motion. Multi-shot cinematic continuity requires hierarchical keyframe chaining.
