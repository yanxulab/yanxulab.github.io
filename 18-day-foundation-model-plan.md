# 18 天 Foundation Models + Post-Training 冲刺计划

目标岗位：OpenAI / Anthropic / Google DeepMind 风格的 **Post-Training / RL Research Engineer**。

边界说明：18 天可以建立完整技术地图、完成可演示的底层实现并形成面试叙事；它不能替代长期论文复现、规模化训练经验或真实研究成果。

## 每天固定框架（5 小时）

| 模块 | 时间 | 当日产出 |
|---|---:|---|
| 进化史 + 理论学习 | 60 min | 一页概念图、关键论文脉络 |
| 数学 | 45 min | 手推关键公式、写清假设与维度 |
| Colab 实现 | 120 min | 可运行 notebook、测试、训练曲线 |
| Ablation + Visualization | 45 min | 至少一个变量、对照实验与图表 |
| 写作 | 30 min | 写入本周长文的一个章节 |

## 18 天表格

| 周 | Topic | 具体内容 |
|---|---|---|
| 第 1 周 · D1 | Transformer 起点：token、embedding 与语言模型 I/O | **进化史/理论：**RNN→Seq2Seq→Attention→Transformer；tokenizer、BPE、词表、context、causal LM；输入 token IDs→embedding→logits→sampling。**数学：**embedding lookup、softmax、cross-entropy、weight tying、参数量估算。**Colab：**从零实现 byte/BPE tokenizer、embedding 与 LM head，并检查 tensor shape。**Ablation/可视化：**词表大小对序列长度、OOV、参数量的影响；embedding 相似度图。**写作：**Blog 1 第 1 章。 |
| 第 1 周 · D2 | Self-Attention 从零：Q/K/V、mask、多头注意力 | **进化史/理论：**Bahdanau attention 到 scaled dot-product attention；MHA 的意义。**数学：**手推 $Q=XW_Q,K=XW_K,V=XW_V$、$\mathrm{softmax}(QK^T/\sqrt{d_k})V$、causal mask、复杂度 $O(n^2d)$。**Colab：**仅用 PyTorch tensor 实现 single-head/MHA，和 `nn.MultiheadAttention` 对齐。**Ablation/可视化：**有无 scaling、不同 head 数、mask 错误；attention heatmap。**写作：**Blog 1 第 2 章。 |
| 第 1 周 · D3 | Transformer block 与现代 LLM layer | **进化史/理论：**Post-LN→Pre-LN；LayerNorm→RMSNorm；绝对位置→RoPE/ALiBi；ReLU/GELU→SwiGLU；MHA→MQA/GQA。**数学：**残差梯度路径、RMSNorm、RoPE 旋转、SwiGLU、各模块参数量。**Colab：**实现 decoder block（RMSNorm+RoPE+GQA+SwiGLU）。**Ablation/可视化：**Pre/Post-Norm 梯度、RoPE 位置外推、MHA/GQA 参数和显存。**写作：**Blog 1 第 3 章。 |
| 第 1 周 · D4 | 从零训练 Tiny GPT：weights、loss 与优化 | **进化史/理论：**GPT-1/2/3、Chinchilla scaling；初始化、AdamW、warmup、cosine decay、mixed precision、gradient clipping/accumulation。**数学：**next-token NLL、perplexity、AdamW、compute/parameter/token scaling。**Colab：**组装并训练 Tiny GPT，保存 checkpoint，生成文本。**Ablation/可视化：**深度/宽度、学习率、weight decay；train/val loss 与梯度范数。**写作：**Blog 1 第 4 章。 |
| 第 1 周 · D5 | 推理系统：decoding、KV cache 与量化 | **进化史/理论：**greedy、temperature、top-k/top-p、beam；prefill/decode；KV cache、continuous batching、FlashAttention、speculative decoding、INT8/INT4。**数学：**无/有 cache 的时间与显存复杂度；KV bytes/token 计算。**Colab：**给 Tiny GPT 加 KV cache，并实现多种 sampling。**Ablation/可视化：**延迟、吞吐、显存、质量随 context/temperature/top-p/量化变化。**写作：**Blog 1 第 5 章。 |
| 第 1 周 · D6 | 拆解真实开源 LLM + 主流模型谱系 | **进化史/理论：**GPT、Claude、Gemini、Llama、Qwen、Mistral、DeepSeek 的公开演进；dense/MoE、长上下文、reasoning。区分官方公开、第三方估算与未知参数。**数学：**从 config 计算 embedding、attention、MLP、LM head、总参数与 KV cache。**Colab：**加载 Hugging Face 小模型，遍历 module/weights/config，hook I/O shape，画结构图。**Ablation/可视化：**两种架构的参数分布、延迟与显存。**写作：**合并润色并发布 Blog 1《Inside a Modern LLM》。 |
| 第 2 周 · D7 | 数据工程与 pre-training pipeline | **进化史/理论：**Common Crawl、去重、过滤、数据混合、污染、版权/PII；document packing、curriculum、数据配比。**数学：**tokens/epoch、FLOPs 粗估、采样权重、重复率与有效样本量。**Colab：**构造小型多域语料 pipeline：清洗、MinHash/近似去重、tokenize、pack。**Ablation/可视化：**数据质量/重复率/混合比例对 validation loss 的影响。**写作：**Blog 2 第 1 章。 |
| 第 2 周 · D8 | 规模化训练：并行、显存与稳定性 | **进化史/理论：**DP/DDP、FSDP/ZeRO、tensor/pipeline/context/expert parallel；BF16、activation checkpointing、通信瓶颈。**数学：**参数/梯度/optimizer/activation 显存账本；all-reduce 通信量；MFU。**Colab：**写显存与 compute estimator；模拟 gradient accumulation/checkpointing，条件允许做双 GPU demo。**Ablation/可视化：**batch、sequence、checkpointing 对峰值显存和 step time。**写作：**Blog 2 第 2 章。 |
| 第 2 周 · D9 | MoE 与高效适配：LoRA/QLoRA/Model Souping | **进化史/理论：**Switch→Mixtral→DeepSeek MoE；router、top-k experts、load balance、capacity；PEFT、LoRA/QLoRA、adapter merging、model soups。**数学：**总参数 vs 激活参数；router softmax、aux loss；LoRA $\Delta W=BA$；权重平均成立条件。**Colab：**实现 toy MoE router；对小模型训练两个 LoRA adapter，再 merge/soup。**Ablation/可视化：**expert collapse、top-k/capacity、LoRA rank、不同 soup 权重。**写作：**Blog 2 第 3 章。 |
| 第 2 周 · D10 | VLM/LVM：视觉编码器到多模态对齐 | **进化史/理论：**ViT、CLIP、Flamingo、LLaVA、Qwen-VL/Gemini 类架构；encoder、projector/resampler、cross-attention、视觉 tokens、训练阶段。**数学：**patch embedding、contrastive loss、cross-attention、token budget。**Colab：**实现 ViT patchify + projector，接入小语言模型或复现 mini-CLIP。**Ablation/可视化：**patch size、冻结/解冻 vision encoder、projector 深度；相似度/attention 图。**写作：**Blog 2 第 4 章。 |
| 第 2 周 · D11 | Diffusion 与生成媒体模型 | **进化史/理论：**VAE/GAN→DDPM→Latent Diffusion→DiT→flow matching；text/image/video/audio generation；U-Net/DiT、VAE、text encoder、scheduler、CFG。**数学：**forward noise、$\epsilon$/$v$ prediction、ELBO 直觉、classifier-free guidance、flow matching ODE。**Colab：**从零训练 2D/toy DDPM，再运行 diffusers 小 pipeline。**Ablation/可视化：**steps、scheduler、CFG、seed；去噪轨迹与质量/速度。**写作：**Blog 2 第 5 章。 |
| 第 2 周 · D12 | Prompt optimization + 评测与模型榜单 | **进化史/理论：**in-context learning、CoT、self-consistency、ReAct、prompt search/optimization；LLM/VLM/GenMedia prompt 差异；benchmark saturation/contamination。**数学：**accuracy、pass@k、pairwise Elo/Bradley–Terry、judge bias、置信区间、FID/CLIPScore 基础。**Colab：**统一 eval harness，对多种 prompt 模板与小模型做成对评测。**Ablation/可视化：**zero/few-shot、CoT、system prompt、顺序敏感性；bootstrap CI。**写作：**合并 Blog 2，并制作“模型—谱系—强项—短板—榜单”动态附录。 |
| 第 3 周 · D13 | Post-training 全景与 SFT | **进化史/理论：**base→instruction-tuned→chat/reasoning；instruction 数据、chat template、loss masking、packing、LoRA/QLoRA、灾难性遗忘。**数学：**token-level CE、prompt mask、mixture weighting。**Colab：**为小模型做 QLoRA SFT，建立 base/SFT checkpoint 与可复现实验。**Ablation/可视化：**数据量、epoch、学习率、LoRA rank、是否训练 prompt tokens。**写作：**Blog 3 第 1 章。 |
| 第 3 周 · D14 | Preference data 与 Reward Model | **进化史/理论：**人类反馈、chosen/rejected、标注协议、position/style bias、reward hacking；pointwise/pairwise/process reward。**数学：**Bradley–Terry、pairwise logistic loss、reward margin、calibration。**Colab：**合成并清洗 preference pairs，训练小 reward model/reranker。**Ablation/可视化：**标签噪声、长度偏差、数据不平衡；reward 分布和校准曲线。**写作：**Blog 3 第 2 章。 |
| 第 3 周 · D15 | RLHF/PPO 从第一性原理实现 | **进化史/理论：**SFT→RM→PPO；policy/reference/reward/value 四模型角色；on-policy rollout、KL control、GAE。**数学：**policy gradient、importance ratio、clipped objective、GAE、KL penalty。**Colab：**在 toy LM/bandit 上实现 PPO 核心循环，再用 TRL 跑小规模实验。**Ablation/可视化：**clip range、KL coefficient、reward scale；reward/KL/entropy/clip fraction。**写作：**Blog 3 第 3 章。 |
| 第 3 周 · D16 | DPO 及直接偏好优化家族 | **进化史/理论：**RLHF 到 DPO；IPO、ORPO、KTO、SimPO 的目标与适用场景；reference-based/reference-free。**数学：**从 KL-regularized RL 推到 DPO loss，理解 $\beta$、隐式 reward 与 log-ratio。**Colab：**从零实现 DPO loss，与 TRL 对齐并训练 SFT checkpoint。**Ablation/可视化：**$\beta$、reference model、preference noise、chosen/rejected 长度。**写作：**Blog 3 第 4 章。 |
| 第 3 周 · D17 | Reasoning RL 与 GRPO | **进化史/理论：**verifiable rewards、group sampling、outcome/process rewards、rejection sampling、curriculum；GRPO 与 PPO/DPO 的差异及失效模式。**数学：**group-relative advantage、normalized reward、KL regularization、方差与 group size。**Colab：**在可验证数学/格式任务上实现 mini-GRPO loop，记录 rollout。**Ablation/可视化：**group size、reward shaping、KL、采样温度；正确率/reward/KL/输出长度。**写作：**Blog 3 第 5 章。 |
| 第 3 周 · D18 | Post-training 系统、红队、模型卡与模拟面试 | **进化史/理论：**offline/online eval、LLM-as-judge、safety tuning、拒答/过拒、data flywheel、持续 post-training；端到端工程故障点。**数学：**多目标 Pareto、win rate CI、inter-rater agreement、power/sample-size 直觉。**Colab：**统一运行 base/SFT/DPO/GRPO，生成 eval report 与 model card。**Ablation/可视化：**能力—安全—风格—成本 trade-off；失败案例 taxonomy。**写作：**发布 Blog 3；准备 10 分钟 system walkthrough、20 道深挖题和 3 个研究 proposal。 |

## 三篇旗舰长文

| 周 | 长文 | 必须展示的证据 |
|---|---|---|
| 第 1 周 | **Inside a Modern LLM: From Tokens to KV Cache** | 从零 attention/decoder、Tiny GPT、KV cache benchmark、真实模型 anatomy |
| 第 2 周 | **How Foundation Models Are Built and Extended Beyond Text** | 数据 pipeline、显存 estimator、MoE/LoRA soup、mini-VLM、diffusion、eval harness |
| 第 3 周 | **Post-Training from First Principles: SFT, RLHF, DPO and GRPO** | SFT→RM→PPO/DPO/GRPO 对照、ablation、model card、失败分析 |

## 18 天结束时的验收标准

- 能在白板上从 tensor shape、参数量、训练 loss 到 decoding/KV cache 讲透一个 decoder-only LLM。
- 能区分“公司已公开的架构事实、可信第三方推测、完全未知信息”，不编造 GPT/Claude/Gemini 的层数或参数。
- 至少有 12 个可运行 notebook、3 篇旗舰文章、1 个统一评测 harness、1 份模型卡。
- 能从目标函数推导并比较 SFT、PPO、DPO、GRPO，且展示至少一次受控 ablation。
- 能回答研究面试中的 trade-off：数据、算力、质量、安全、延迟、显存、稳定性、评测偏差。

