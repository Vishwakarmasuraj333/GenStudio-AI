# Problem Statement
## GenStudio AI: Research Problem Formulation

### 1. Context and Motivation
While generative models for image and video synthesis have reached unprecedented visual capabilities, their practical utilization in academic, research, and non-enterprise environments is constrained by three core problems:

1. **Hardware Infeasibility:** State-of-the-art diffusion transformers require 16GB to 80GB of specialized VRAM (NVIDIA A100/H100), rendering local execution impossible on standard student or developer laptops without dedicated GPUs.
2. **Ad-Hoc, Non-Reproducible API Usage:** Practitioners using hosted inference often rely on fragmented, ad-hoc scripts that lack systematic latency tracking, cost ledger accounting, parameter persistence, and error recovery mechanisms.
3. **Suboptimal Static Model Selection:** Traditional systems hard-code a single generative model for all requests. Because models exhibit disparate price-performance characteristics (e.g., FLUX.1 schnell at \$0.003 vs SDXL at \$0.006 vs video models at \$0.045+), static selection routinely incurs unnecessary financial expenditure or intolerable latency delays.

### 2. Specific Research Questions
This project investigates the following research questions (RQs):
- **RQ1:** How can a full-stack architecture enable ordinary client hardware to perform production-grade image and video synthesis reliably using hosted inference APIs without compromising security?
- **RQ2:** What are the empirical latency, cost, prompt adherence, and temporal consistency distributions of modern hosted models (FLUX.1, SDXL, LTX-Video, Wan2.1) when evaluated across standardized prompt domains?
- **RQ3:** Can a multi-objective intelligent routing algorithm dynamically select generative models to achieve Pareto-optimal trade-offs between cost, latency, and quality compared to static baseline policies?
