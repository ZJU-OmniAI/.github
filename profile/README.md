<p align="center">
  <img src="https://raw.githubusercontent.com/ZJU-OmniAI/.github/main/assets/banner.svg" width="100%" alt="ZJU-OmniAI — Embodied Intelligence and General-Purpose AI">
</p>

<p align="center">
  <strong>Learning to perceive, reason, remember, and act.</strong><br>
  Zhejiang University · 浙江大学
</p>

We build AI systems that connect multimodal understanding with reasoning and action. Our research spans **embodied intelligence**, **spatial cognition**, **trustworthy multimodal models**, **reinforcement learning**, and **autonomous agents**.

我们关注从感知、推理、记忆到行动的智能闭环，以<strong>具身小脑与具身大脑</strong>为主线，探索通用智能的学习与实践。

<p align="center">
  <a href="#embodied-cerebellum">具身小脑</a> ·
  <a href="#embodied-brain">具身大脑</a> ·
  <a href="#spatial-intelligence">空间智能</a> ·
  <a href="#trustworthy-multimodal">可信多模态</a> ·
  <a href="#reasoning-and-rl">推理与强化学习</a> ·
  <a href="#autonomous-agents">自主智能体</a>
</p>

## Recent Highlights

Automatically updated all-time counts from Hugging Face. Cross-repository totals are refreshed every 5 minutes. Badges are cached and may lag behind the source. [Refresh details](https://github.com/ZJU-OmniAI/.github/tree/main/metrics).

[![models downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FZJU-OmniAI%2F.github%2Fhf-download-stats%2Fdownloads.json&query=%24.team.models&label=models+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://raw.githubusercontent.com/ZJU-OmniAI/.github/hf-download-stats/downloads.json) [![datasets downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FZJU-OmniAI%2F.github%2Fhf-download-stats%2Fdownloads.json&query=%24.team.datasets&label=datasets+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://raw.githubusercontent.com/ZJU-OmniAI/.github/hf-download-stats/downloads.json) [![total downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FZJU-OmniAI%2F.github%2Fhf-download-stats%2Fdownloads.json&query=%24.team.total&label=total+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://raw.githubusercontent.com/ZJU-OmniAI/.github/hf-download-stats/downloads.json)

| Date | Work | What's new |
| :--- | :--- | :--- |
| **2026.10** | [**DTCA**](https://github.com/ZJU-OmniAI/DTCA) | Token-level credit assignment for reinforcement learning in diffusion language models; up to **+9.0 points** on MATH500 over LLaDA-8B-Instruct. [Paper](https://zju-omniai.github.io/DTCA/assets/resources/dtca-paper.pdf) · [Project](https://zju-omniai.github.io/DTCA/) |
| **2026.10** | [**VLA-Rolling**](https://github.com/ZJU-OmniAI/VLA-Rolling) | Reuse the unexecuted action tail instead of starting each chunk from noise: lower inference cost in **all 16** model–benchmark pairs, up to **1.48×** faster. [Paper](https://arxiv.org/abs/2610.25043) · [Project](https://chenbao123ww.github.io/VLA-Rolling/) · [![model downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2FChenbao77%2FVLA-Rolling%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=model+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/Chenbao77/VLA-Rolling) |
| **2026.10** | [**Scene-Designer**](https://github.com/ZJU-OmniAI/Scene-Designer) | Agentic 3D scene generation that learns to both design and critique scenes, from **Scene-OTA-35K** and **Scene-OTC-15K** with Critic-guided Scene-GRPO. [Paper](https://arxiv.org/abs/2610.23121) · [Project](https://zju-omniai.github.io/Scene-Designer/) · [![model downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2FXuanyuLiu%2FScene-Builder-Qwen3-VL-8B-Instruct%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=model+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/XuanyuLiu/Scene-Builder-Qwen3-VL-8B-Instruct) [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2FXuanyuLiu%2FScene-OTC-Bench%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/XuanyuLiu/Scene-OTC-Bench) |
| **2026.10** | [**VLA-Δ**](https://github.com/ZJU-OmniAI/VLA-Delta) | A VLA that learns how the physical state changes, not only which action to take; **98.4%** average success on LIBERO and **90.06%** on RoboTwin 2.0 (Clean). [Paper](https://arxiv.org/abs/2610.21306) · [Project](https://zju-omniai.github.io/VLA-Delta/) · [![models downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FZJU-OmniAI%2F.github%2Fhf-download-stats%2Fdownloads.json&query=%24.projects%5B%22vla-delta%22%5D.models&label=models+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://raw.githubusercontent.com/ZJU-OmniAI/.github/hf-download-stats/downloads.json) |
| **2026.09** | [**EmbodiedMemory-Bench**](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_memory) | A benchmark for memory in long-horizon embodied tasks, with **2,554 executable episodes**. [Paper](https://arxiv.org/abs/2609.28236) · [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2FlzLiang%2FEmbodiedMemoryBench%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/lzLiang/EmbodiedMemoryBench) |

## Research Directions

<a name="embodied-cerebellum"></a>
### 01 · 具身小脑 | Embodied Cerebellum

**Action learning, efficient execution, and closed-loop correction.**<br>
让机器人理解动作带来的物理变化，在执行中感知偏差、及时纠错，兼顾动作效率与控制可靠性。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[VLA-Corrector](https://github.com/ZJU-OmniAI/vla-corrector)**<br><sub>NeurIPS 2026</sub> | Monitor visual drift during action chunks, interrupt stale actions, and guide corrective replanning with a lightweight external corrector. | [Paper](https://arxiv.org/abs/2607.01804) · [Code](https://github.com/ZJU-OmniAI/vla-corrector) · [Project](https://zju-omniai.github.io/vla-corrector/) |
| **[VLA-Δ](https://github.com/ZJU-OmniAI/VLA-Delta)**<br><sub>arXiv 2026</sub> | Learn action-relevant representations from physical state differences, supervised by future-state difference text, structured transition slots, and optical flow, and generate continuous actions with a flow-matching action expert. | [Paper](https://arxiv.org/abs/2610.21306) · [Project](https://zju-omniai.github.io/VLA-Delta/) · [![models downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FZJU-OmniAI%2F.github%2Fhf-download-stats%2Fdownloads.json&query=%24.projects%5B%22vla-delta%22%5D.models&label=models+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://raw.githubusercontent.com/ZJU-OmniAI/.github/hf-download-stats/downloads.json) |
| **[VLA-Rolling](https://github.com/ZJU-OmniAI/VLA-Rolling)**<br><sub>arXiv 2026</sub> | Carry the unexecuted action tail into the next planning window; a lightweight confidence estimator sets renoising and the denoising budget while the base VLA stays frozen. | [Paper](https://arxiv.org/abs/2610.25043) · [Project](https://chenbao123ww.github.io/VLA-Rolling/) · [![model downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2FChenbao77%2FVLA-Rolling%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=model+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/Chenbao77/VLA-Rolling) |

📚 **[Awesome Closed-Loop VLA](https://github.com/ZJU-OmniAI/Awesome-Closed-Loop-VLA)** — A reading guide connecting execution, prediction, and learning loops.

<a name="embodied-brain"></a>
### 02 · 具身大脑 | Embodied Brain

**Reasoning, planning, navigation, and memory for long-horizon interaction.**<br>
让智能体理解环境、记住经验、规划任务，并在交互中反思与调整。

Our **[Embodied-Omni](https://github.com/ZJU-OmniAI/Embodied-Omni)** series brings three complementary capabilities together:

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[Embodied-Reasoner](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_reasoner)**<br><sub>ACL 2026 Main</sub> | Combine visual search, long-horizon planning, environment-state reasoning, and reflection in an observation–thought–action loop. | [Paper](https://aclanthology.org/2026.acl-long.1910/) · [Project](https://embodied-reasoner.github.io/) · [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2Fzwq2018%2Fembodied_reasoner%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/zwq2018/embodied_reasoner) |
| **[Embodied-Navigator](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_navigator)**<br><sub>arXiv 2026</sub> | Connect pixel pointing to 3D navigation with selective reasoning, Anchor-Trajectory Memory, and Two-Level GRPO. | [Paper](https://arxiv.org/abs/2608.17512) · [Project](https://zju-omniai.github.io/Embodied-Navigator/) · [![model downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2FUnderTides%2FEmbodied-Navigator-7B-GRPO%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=model+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/UnderTides/Embodied-Navigator-7B-GRPO) |
| **[EmbodiedMemory-Bench](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_memory)**<br><sub>arXiv 2026</sub> | Evaluate retained observations, changing world states, interaction-derived knowledge, and experience generalization. | [Paper](https://arxiv.org/abs/2609.28236) · [Project](https://zju-omniai.github.io/Embodied-Omni/EmbodiedMemoryBench/) · [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2FlzLiang%2FEmbodiedMemoryBench%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/lzLiang/EmbodiedMemoryBench) |

<a name="spatial-intelligence"></a>
### 03 · 空间智能与世界模型 | Spatial Intelligence & World Models

**Learning and evaluating how AI understands and constructs the physical world.**<br>
从交互轨迹学习空间关系、状态变化与物理过程，建立可检验的空间认知能力，并让智能体设计物理合理、功能正确的 3D 场景。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[Spatial-Interactor](https://github.com/ZJU-OmniAI/Spatial-Interactor)**<br><sub>arXiv 2026</sub> | Learn local state transitions and long-horizon spatial reasoning from real and simulated interaction trajectories. | [Paper](https://arxiv.org/abs/2609.23038) · [Project](https://zju-omniai.github.io/Spatial-Interactor/) · [![models downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FZJU-OmniAI%2F.github%2Fhf-download-stats%2Fdownloads.json&query=%24.projects%5B%22spatial-interactor%22%5D.models&label=models+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://raw.githubusercontent.com/ZJU-OmniAI/.github/hf-download-stats/downloads.json) [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2Fkagakouko%2FLSI-108K%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/kagakouko/LSI-108K) |
| **[ProVisE](https://github.com/ZJU-OmniAI/ProVisE)**<br><sub>arXiv 2026</sub> | Evaluate spatial cognition through protocol-constrained visual answers, sharing task semantics and metrics across model families. | [Paper](https://arxiv.org/abs/2607.21072) · [Project](https://zju-omniai.github.io/ProVisE/) · [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2Fwx91726%2FSpatialGen-Bench%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/wx91726/SpatialGen-Bench) |
| **[Scene-Designer](https://github.com/ZJU-OmniAI/Scene-Designer)**<br><sub>arXiv 2026</sub> | Learn design intelligence for agentic 3D scene generation: build physically valid, functionally correct, layout-coherent scenes, critique their quality, and refine design decisions with Critic-guided Scene-GRPO. | [Paper](https://arxiv.org/abs/2610.23121) · [Project](https://zju-omniai.github.io/Scene-Designer/) · [![model downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2FXuanyuLiu%2FScene-Builder-Qwen3-VL-8B-Instruct%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=model+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/XuanyuLiu/Scene-Builder-Qwen3-VL-8B-Instruct) [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2FXuanyuLiu%2FScene-OTC-Bench%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/XuanyuLiu/Scene-OTC-Bench) |

📚 **[Awesome World Model](https://github.com/ZJU-OmniAI/Awesome-World-Model)** — Papers, frameworks, datasets, and benchmarks for world-model research.

<a name="trustworthy-multimodal"></a>
### 04 · 可信多模态 | Trustworthy Multimodal Intelligence

**Better visual grounding and more reliable multimodal understanding.**<br>
减少多模态幻觉，让模型的判断更忠实于视觉证据。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[MGAP](https://github.com/ZJU-OmniAI/MGAP)**<br><sub>ICML 2026</sub> | Reduce object hallucinations with geometry-aware, training-free adaptive projection while preserving semantic structure. | [Paper](https://arxiv.org/abs/2606.09859) · [Code](https://github.com/ZJU-OmniAI/MGAP) · [OpenReview](https://openreview.net/forum?id=LInDSHWGMK) |
| **[OMNEX-VL](https://github.com/ZJU-OmniAI/OMNEX-VL)**<br><sub>AAAI 2026</sub> | Improve visual grounding through caption feedback, diversity-aware sampling, and conflict regularization. | [Paper](https://ojs.aaai.org/index.php/AAAI/article/view/37772) · [Code](https://github.com/ZJU-OmniAI/OMNEX-VL) · [![model downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2FOmniAI-ZJU%2FOMNEX-VL%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=model+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/OmniAI-ZJU/OMNEX-VL) · [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2FOmniAI-ZJU%2FOMNEX-VL-DATA%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/OmniAI-ZJU/OMNEX-VL-DATA) |

<a name="reasoning-and-rl"></a>
### 05 · 推理与强化学习 | Reasoning & Reinforcement Learning

**Post-training methods for reasoning and verifiable generation.**<br>
研究从模仿学习到奖励优化的衔接，覆盖自回归与扩散语言模型，提升推理、代码生成与学习效率。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[GFT](https://github.com/ZJU-OmniAI/GFT)**<br><sub>ACL 2026 Findings</sub> | Bridge imitation and reward fine-tuning with unbiased group advantages and dynamic coefficient rectification. | [Paper](https://aclanthology.org/2026.findings-acl.1444/) · [Code](https://github.com/ZJU-OmniAI/GFT) · [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2FOmniAI-ZJU%2FNuminaMath-Cot-Distillation-100K%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/OmniAI-ZJU/NuminaMath-Cot-Distillation-100K) |
| **[DTCA](https://github.com/ZJU-OmniAI/DTCA)**<br><sub>Preprint 2026</sub> | Assign token-level credit in reinforcement learning for diffusion language models through contribution-weighted denoising-step selection, part-of-speech credit, and entropy-flow calibration. | [Paper](https://zju-omniai.github.io/DTCA/assets/resources/dtca-paper.pdf) · [Code](https://github.com/ZJU-OmniAI/DTCA) · [Project](https://zju-omniai.github.io/DTCA/) |
| **[VeriRL](https://github.com/ZJU-OmniAI/VeriRL)**<br><sub>arXiv 2025 · AI for Code & Hardware</sub> | Improve Verilog generation through reinforcement learning with trace-back reward rescoring and sample-balanced optimization. | [Paper](https://arxiv.org/abs/2508.18462) · [![model downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2Ftttboy%2FVerirl-CodeQwen2.5%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=model+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/tttboy/Verirl-CodeQwen2.5) · [![dataset downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fdatasets%2Ftttboy%2FVeribench-53K%3Fexpand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=dataset+downloads&color=FFD21E&logo=huggingface&cacheSeconds=300)](https://huggingface.co/datasets/tttboy/Veribench-53K) |

<a name="autonomous-agents"></a>
### 06 · 自主智能体 | Autonomous Agents & Tool Use

**Agents that improve their policies and turn instructions into workflows.**<br>
从策略反思与优化，到数据分析、工具调用和自主工作流。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[Agent-Pro](https://github.com/ZJU-OmniAI/Agent-Pro)**<br><sub>ACL 2024</sub> | Enable LLM agents to evolve their decision policies through policy-level reflection and optimization. | [Paper](https://aclanthology.org/2024.acl-long.292/) · [Code](https://github.com/ZJU-OmniAI/Agent-Pro) |
| **[Data-Copilot](https://github.com/ZJU-OmniAI/Data-Copilot)**<br><sub>ICLR 2024 Workshop · Oral</sub> | Connect natural-language requests with heterogeneous data through autonomous tool design, analysis, and visualization workflows. | [Paper](https://arxiv.org/abs/2306.07209) · [Code](https://github.com/ZJU-OmniAI/Data-Copilot) · [OpenReview](https://openreview.net/forum?id=iUEBnQyfWE) |

## Tools for Research & Work

- **[LLM_in_Work](https://github.com/ZJU-OmniAI/LLM_in_Work)** — Your local Claude Code or Codex agent in Word, PowerPoint, Excel, Overleaf, and the PDFs you read in Chrome: select exactly what you mean, review the diff, and edit only that part, or just ask.
- **[Paper_Mind](https://github.com/ZJU-OmniAI/Paper_Mind)** — A tag-based library for the papers you collect: one-click capture, tags and topic packs, local and LLM search, and recommendations from your own collection.

---

**Explore:** [All repositories](https://github.com/orgs/ZJU-OmniAI/repositories) · **Discuss:** open an issue in the relevant repository · **Contact:** [zhangwenqi@zju.edu.cn](mailto:zhangwenqi@zju.edu.cn)
