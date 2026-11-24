# Literature Review
## Comparative Analysis of Diffusion, Flow-Matching, and Multi-Modal Generative Architectures

### 1. Evolution of Image Synthesis Architectures
The landscape of deep generative visual synthesis has progressed across three paradigm shifts:
1. **Generative Adversarial Networks (Goodfellow et al., 2014; Karras et al., StyleGAN3, 2021):** Early benchmarks established high visual fidelity but suffered from severe mode collapse, non-convergence during minimax training, and limited diversity when conditioned on complex semantic prompts.
2. **Denoising Diffusion Probabilistic Models (DDPM) & Latent Diffusion (Ho et al., 2020; Rombach et al., Stable Diffusion, 2022):** Formulated image generation as a parameterized reverse Markovian process. Moving diffusion forward and reverse processes to the lower-dimensional latent space of a pre-trained Variational Autoencoder (VAE) dramatically reduced computational complexity, paving the way for SD 1.5, SD 2.1, and SDXL 1.0.
3. **Rectified Flow Matching & Diffusion Transformers (Lipman et al., 2023; Esser et al., FLUX.1, 2024):** Modern architectures substitute standard U-Nets with DiT (Diffusion Transformer) backbones, utilizing straight vector field trajectories (rectified flow). FLUX.1 [schnell] achieves parity or superiority over multi-step diffusion in as few as 4 sampling steps, demonstrating state-of-the-art typographical fidelity and anatomical accuracy.

### 2. Video Synthesis & Temporal Coherence Challenges
Video generation introduces the requirement of temporal consistency across consecutive frames:
- **Spatial-Temporal Latent Decoupling:** Models such as LTX-Video (Lightricks, 2024) and Wan2.1 (Wan-AI, 2025) leverage 3D causal convolutions and space-time cross-attention mechanisms.
- **Artifacts and Motion Drift:** Traditional frame interpolation approaches suffer from temporal flickering and subject morphing. Diffusion transformers trained directly on temporal video tokens mitigate unnatural deformation by conditioning latents on learned optical flow manifolds.

### 3. Survey of Intelligent Routing & Multi-Model Ensembles
Existing commercial wrappers typically bind clients to a single proprietary foundation model. Recent work in LLM routing (e.g., FrugalGPT, Chen et al., 2023) demonstrated that dynamic cascade routing reduces inference cost by up to 73%. GenStudio AI translates this paradigm to multi-modal generative vision, pioneering constrained multi-objective utility scoring for diffusion models.
