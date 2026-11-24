# Abstract
## GenStudio AI: Comparative Evaluation and Intelligent Routing of Hosted Generative AI Models for Text-to-Image and Image-to-Video Synthesis

**Candidate:** Suraj  
**Degree:** Master of Science in Information Technology (M.Sc. IT)  
**Institution:** Academic Evaluation Board  

---

### Abstract
Generative Artificial Intelligence has transitioned from experimental research into mission-critical creative software. However, the computational complexity of leading diffusion and flow-matching models (such as FLUX.1 with 12 billion parameters and LTX-Video diffusion transformers) imposes severe hardware constraints on client workstations. Concurrently, utilizing hosted serverless inference introduces multi-dimensional trade-offs across financial cost, inference latency, prompt fidelity, and availability.

This thesis presents **GenStudio AI**, a unified full-stack generative research studio engineered to solve these challenges. GenStudio AI abstracts hosted inference APIs into a normalized interface, isolates secrets on the server, and implements an asynchronous task execution queue with verified media delivery. Crucially, the platform contributes a reproducible evaluation benchmark across six rigorous prompt domains (photorealism, spatial composition, typography, cinematic aesthetics, artistic rendering, and motion dynamics).

To optimize multi-model deployment, an intelligent multi-objective routing algorithm is developed that formulates model selection as a constrained utility optimization problem:
$$S(m) = w_{\text{cost}} U_{\text{cost}}(m) + w_{\text{speed}} U_{\text{speed}}(m) + w_{\text{quality}} U_{\text{quality}}(m) + w_{\text{rel}} U_{\text{rel}}(m)$$

Empirical results demonstrate that the proposed routing policy achieves substantial cost reductions (up to 50% relative to static SDXL baseline) and latency reductions while preserving high semantic alignment. The system is verified through automated unit, integration, and security tests, providing an honest, reproducible foundation for generative AI deployment on consumer hardware.

**Keywords:** Generative AI, Flow Matching, Diffusion Transformers, FLUX.1, LTX-Video, Intelligent Model Routing, Empirical Benchmarking, Full-Stack Architecture.
