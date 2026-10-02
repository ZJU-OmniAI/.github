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

| Date | Work | What's new |
| :--- | :--- | :--- |
| **2026.09** | [**EmbodiedMemory-Bench**](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_memory) | A benchmark for memory in long-horizon embodied tasks, with **2,554 executable episodes**. [Paper](https://arxiv.org/abs/2609.28236) · [Dataset](https://huggingface.co/datasets/lzLiang/EmbodiedMemoryBench) |
| **2026.09** | [**Spatial-Interactor**](https://github.com/ZJU-OmniAI/Spatial-Interactor) | Learning spatial reasoning from interaction trajectories; includes **LSI-108K** and model checkpoints. [Paper](https://arxiv.org/abs/2609.23038) · [Models & Data](https://huggingface.co/collections/kagakouko/spatial-interactor) |
| **2026.09** | [**VLA-Corrector**](https://github.com/ZJU-OmniAI/vla-corrector) | Accepted to **NeurIPS 2026** — lightweight monitoring and correction for adaptive VLA action horizons. [Paper](https://arxiv.org/abs/2607.01804) · [Project](https://zju-omniai.github.io/vla-corrector/) |
| **2026.08** | [**Embodied-Navigator**](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_navigator) | Pixel-based navigation with selective reasoning, trajectory memory, and zero-shot deployment on Unitree Go2. [Paper](https://arxiv.org/abs/2608.17512) · [Project](https://zju-omniai.github.io/Embodied-Navigator/) |
| **2026.07** | [**ProVisE**](https://github.com/ZJU-OmniAI/ProVisE) | A shared spatial-cognition evaluation interface for image-generation models and VLMs. [Paper](https://arxiv.org/abs/2607.21072) · [Project](https://zju-omniai.github.io/ProVisE/) |

## Research Directions

<a name="embodied-cerebellum"></a>
### 01 · 具身小脑 | Embodied Cerebellum

**Closed-loop action execution, monitoring, and correction.**<br>
让机器人在执行中感知偏差、及时纠错，兼顾动作效率与控制可靠性。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[VLA-Corrector](https://github.com/ZJU-OmniAI/vla-corrector)**<br><sub>NeurIPS 2026</sub> | Monitor visual drift during action chunks, interrupt stale actions, and guide corrective replanning with a lightweight external corrector. | [Paper](https://arxiv.org/abs/2607.01804) · [Code](https://github.com/ZJU-OmniAI/vla-corrector) · [Project](https://zju-omniai.github.io/vla-corrector/) |

📚 **[Awesome Closed-Loop VLA](https://github.com/ZJU-OmniAI/Awesome-Closed-Loop-VLA)** — A reading guide connecting execution, prediction, and learning loops.

<a name="embodied-brain"></a>
### 02 · 具身大脑 | Embodied Brain

**Reasoning, planning, navigation, and memory for long-horizon interaction.**<br>
让智能体理解环境、记住经验、规划任务，并在交互中反思与调整。

Our **[Embodied-Omni](https://github.com/ZJU-OmniAI/Embodied-Omni)** series brings three complementary capabilities together:

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[Embodied-Reasoner](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_reasoner)**<br><sub>ACL 2026 Main</sub> | Combine visual search, long-horizon planning, environment-state reasoning, and reflection in an observation–thought–action loop. | [Paper](https://aclanthology.org/2026.acl-long.1910/) · [Project](https://embodied-reasoner.github.io/) · [Dataset](https://huggingface.co/datasets/zwq2018/embodied_reasoner) |
| **[Embodied-Navigator](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_navigator)**<br><sub>arXiv 2026</sub> | Connect pixel pointing to 3D navigation with selective reasoning, Anchor-Trajectory Memory, and Two-Level GRPO. | [Paper](https://arxiv.org/abs/2608.17512) · [Project](https://zju-omniai.github.io/Embodied-Navigator/) · [Model](https://huggingface.co/UnderTides/Embodied-Navigator-7B-GRPO) |
| **[EmbodiedMemory-Bench](https://github.com/ZJU-OmniAI/Embodied-Omni/tree/main/embodied_memory)**<br><sub>arXiv 2026</sub> | Evaluate retained observations, changing world states, interaction-derived knowledge, and experience generalization. | [Paper](https://arxiv.org/abs/2609.28236) · [Project](https://zju-omniai.github.io/Embodied-Omni/EmbodiedMemoryBench/) · [Dataset](https://huggingface.co/datasets/lzLiang/EmbodiedMemoryBench) |

<a name="spatial-intelligence"></a>
### 03 · 空间智能与世界模型 | Spatial Intelligence & World Models

**Learning and evaluating how AI understands the physical world.**<br>
从交互轨迹学习空间关系、状态变化与物理过程，建立可检验的空间认知能力。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[Spatial-Interactor](https://github.com/ZJU-OmniAI/Spatial-Interactor)**<br><sub>arXiv 2026</sub> | Learn local state transitions and long-horizon spatial reasoning from real and simulated interaction trajectories. | [Paper](https://arxiv.org/abs/2609.23038) · [Project](https://zju-omniai.github.io/Spatial-Interactor/) · [Models & Data](https://huggingface.co/collections/kagakouko/spatial-interactor) |
| **[ProVisE](https://github.com/ZJU-OmniAI/ProVisE)**<br><sub>arXiv 2026</sub> | Evaluate spatial cognition through protocol-constrained visual answers, sharing task semantics and metrics across model families. | [Paper](https://arxiv.org/abs/2607.21072) · [Project](https://zju-omniai.github.io/ProVisE/) · [Dataset](https://huggingface.co/datasets/wx91726/SpatialGen-Bench) |

📚 **[Awesome World Model](https://github.com/ZJU-OmniAI/Awesome-World-Model)** — Papers, frameworks, datasets, and benchmarks for world-model research.

<a name="trustworthy-multimodal"></a>
### 04 · 可信多模态 | Trustworthy Multimodal Intelligence

**Better visual grounding and more reliable multimodal understanding.**<br>
减少多模态幻觉，让模型的判断更忠实于视觉证据。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[MGAP](https://github.com/ZJU-OmniAI/MGAP)**<br><sub>ICML 2026</sub> | Reduce object hallucinations with geometry-aware, training-free adaptive projection while preserving semantic structure. | [Paper](https://arxiv.org/abs/2606.09859) · [Code](https://github.com/ZJU-OmniAI/MGAP) · [OpenReview](https://openreview.net/forum?id=LInDSHWGMK) |
| **[OMNEX-VL](https://github.com/ZJU-OmniAI/OMNEX-VL)**<br><sub>AAAI 2026</sub> | Improve visual grounding through caption feedback, diversity-aware sampling, and conflict regularization. | [Paper](https://ojs.aaai.org/index.php/AAAI/article/view/37772) · [Code](https://github.com/ZJU-OmniAI/OMNEX-VL) · [Model](https://huggingface.co/OmniAI-ZJU/OMNEX-VL) |

<a name="reasoning-and-rl"></a>
### 05 · 推理与强化学习 | Reasoning & Reinforcement Learning

**Post-training methods for reasoning and verifiable generation.**<br>
研究从模仿学习到奖励优化的衔接，提升推理、代码生成与学习效率。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[GFT](https://github.com/ZJU-OmniAI/GFT)**<br><sub>ACL 2026 Findings</sub> | Bridge imitation and reward fine-tuning with unbiased group advantages and dynamic coefficient rectification. | [Paper](https://aclanthology.org/2026.findings-acl.1444/) · [Code](https://github.com/ZJU-OmniAI/GFT) · [Dataset](https://huggingface.co/datasets/OmniAI-ZJU/NuminaMath-Cot-Distillation-100K) |
| **[VeriRL](https://github.com/ZJU-OmniAI/VeriRL)**<br><sub>arXiv 2025 · AI for Code & Hardware</sub> | Improve Verilog generation through reinforcement learning with trace-back reward rescoring and sample-balanced optimization. | [Paper](https://arxiv.org/abs/2508.18462) · [Model](https://huggingface.co/tttboy/Verirl-CodeQwen2.5) · [Dataset](https://huggingface.co/datasets/tttboy/Veribench-53K) |

<a name="autonomous-agents"></a>
### 06 · 自主智能体 | Autonomous Agents & Tool Use

**Agents that improve their policies and turn instructions into workflows.**<br>
从策略反思与优化，到数据分析、工具调用和自主工作流。

| Project | Focus | Resources |
| :--- | :--- | :--- |
| **[Agent-Pro](https://github.com/ZJU-OmniAI/Agent-Pro)**<br><sub>ACL 2024</sub> | Enable LLM agents to evolve their decision policies through policy-level reflection and optimization. | [Paper](https://aclanthology.org/2024.acl-long.292/) · [Code](https://github.com/ZJU-OmniAI/Agent-Pro) |
| **[Data-Copilot](https://github.com/ZJU-OmniAI/Data-Copilot)**<br><sub>ICLR 2024 Workshop · Oral</sub> | Connect natural-language requests with heterogeneous data through autonomous tool design, analysis, and visualization workflows. | [Paper](https://arxiv.org/abs/2306.07209) · [Code](https://github.com/ZJU-OmniAI/Data-Copilot) · [OpenReview](https://openreview.net/forum?id=iUEBnQyfWE) |

## Tools for Research & Work

- **[LLM_in_Work](https://github.com/ZJU-OmniAI/LLM_in_Work)** — AI assistants for Word, PowerPoint, Excel, and Overleaf, with in-place edits and diff review.
- **[Paper_Mind](https://github.com/ZJU-OmniAI/Paper_Mind)** — A paper library organized around tags, remembered concepts, and optional LLM assistance.

---

**Explore:** [All repositories](https://github.com/orgs/ZJU-OmniAI/repositories) · **Discuss:** open an issue in the relevant repository · **Contact:** [zhangwenqi@zju.edu.cn](mailto:zhangwenqi@zju.edu.cn)
