# Limitations and Future Scope
## GenStudio AI: Academic Evaluation of Boundaries & Future Extensions

### 1. Current System Limitations
1. **Third-Party Inference Availability:** While serverless inference APIs eliminate local hardware requirements, client requests remain subject to provider cold-start loading latencies (e.g., Hugging Face 503 initial warm-up delays) and provider-side rate limits.
2. **Network Bandwidth Sensitivity for Video:** High-resolution video synthesis (720p/1080p MP4) requires non-trivial egress network bandwidth when downloading completed media containers to client workstations.
3. **Evaluation Metric Approximations:** While simulated CLIP alignment and optical-flow temporal consistency metrics provide reproducible comparative rankings, they remain algorithmic proxies and cannot entirely replace qualitative human aesthetic evaluation.

### 2. Future Scope & Research Extensions
1. **Local Diffusers On-Demand Sidecar:** Integrate an optional local PyTorch / Diffusers inference sidecar utilizing ONNX Runtime or DirectML for laptops equipped with Intel Core Ultra or AMD Ryzen AI NPUs.
2. **LoRA Fine-Tuning Orchestrator:** Extend the platform to support parameter-efficient fine-tuning (PEFT / LoRA) of FLUX.1 models using user-supplied style datasets.
3. **ComfyUI Distributed Worker Cluster:** Implement a dynamic ComfyUI worker discovery protocol enabling studios to connect multiple private GPU worker nodes across a local area network.
4. **Adaptive Context Prompt Engineering:** Enhance the Gemini adapter with multi-shot few-shot retrieval from a vector store of historically highest-rated user generations.
