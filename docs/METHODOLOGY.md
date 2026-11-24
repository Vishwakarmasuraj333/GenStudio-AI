# Research Methodology
## GenStudio AI: Scientific Methodology & Mathematical Formulations

### 1. Controlled Experimental Design
To rigorously evaluate hosted generative AI models, GenStudio AI adheres to three experimental control tenets:
1. **Identical Semantic Conditioning:** Models are tested on the exact same benchmark prompts under fixed aspect ratios and seeds.
2. **Environment Standardization:** Latency measurements separate client-to-gateway round-trips from gateway-to-provider execution times using microsecond-precision `time.perf_counter()`.
3. **No Hidden Failures:** HTTP 503 cold starts, 429 rate limit events, and timeouts are recorded explicitly in results rather than omitted from averages.

### 2. Multi-Objective Optimization Formulation
The intelligent routing engine selects a model $m^*$ from the eligible set $\mathcal{M}_{\text{task}}$:

$$m^* = \arg\max_{m \in \mathcal{M}_{\text{eligible}}} \left[ w_c U_c(m) + w_s U_s(m) + w_q U_q(m) + w_r U_r(m) \right]$$

Subject to hard constraints:
$$\text{Cost}(m) \le B_{\max}, \quad \text{Latency}(m) \le L_{\max}$$

Where:
- $U_c(m) = \max\left(0, 1 - \frac{\text{Cost}(m)}{C_{\max}}\right)$ (Normalized cost utility)
- $U_s(m) = \max\left(0, 1 - \frac{\text{Latency}(m)}{L_{\max}}\right)$ (Normalized speed utility)
- $U_q(m) \in [0, 1]$ (Empirical prompt adherence & fidelity score)
- $U_r(m) \in [0, 1]$ (Historical availability & success reliability)
- $\sum w_i = 1.0$ (Policy weights configured by user: cost, speed, quality, or balanced)

### 3. Pareto Frontier Analysis
A model $m_1$ dominates model $m_2$ if it is strictly superior in at least one metric without being inferior in any other metric. GenStudio AI computes the non-dominated Pareto front across the Cost $\times$ Latency $\times$ Quality manifold.
