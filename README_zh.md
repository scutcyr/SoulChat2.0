# [心理咨询师数字孪生（SoulChat2.0）](https://github.com/scutcyr/SoulChat2.0)
<p align="center">
    <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache%202-red.svg"></a>
    <a href="support os"><img src="https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/python-3.8+-aff.svg"></a>
    <a href="https://github.com/scutcyr/SoulChat2.0/graphs/contributors"><img src="https://img.shields.io/github/contributors/scutcyr/SoulChat2.0?color=9ea"></a>
    <a href="https://github.com/scutcyr/SoulChat2.0/commits"><img src="https://img.shields.io/github/commit-activity/m/scutcyr/SoulChat2.0?color=3af"></a>
    <a href="https://github.com/scutcyr/SoulChat2.0/issues"><img src="https://img.shields.io/github/issues/scutcyr/SoulChat2.0?color=9cc"></a>
    <a href="https://github.com/scutcyr/SoulChat2.0/stargazers"><img src="https://img.shields.io/github/stars/scutcyr/SoulChat2.0?color=ccf"></a>
</p>

\[ [English](README.md) | 中文 \]

## 简介
自2023年5月发布[SoulChat](https://github.com/scutcyr/SoulChat)以来，我们经过对真实世界心理咨询语言风格、心理咨询技术等方面的深入探索，在心理咨询师数字孪生建模能力上取得了显著提升。

ChatGPT诞生以来，国内外已有大量的工作将大模型（LLM）应用于情感陪护、心理健康支持对话、心理咨询对话领域，例如SoulChat、MeChat、QiaoBan、CPsyCoun、MindChat、EmoLLM等等。然而，过往的工作聚焦于借助精心设计的提示词来构建多轮心理健康对话数据集，微调出的“心理健康大模型”很容易造成回答的同质化、模板化，使得这些LLMs难以应对复杂多变的来访者，无法很好模拟现实世界真实心理咨询师的语言表达与疗法技术运用风格。

针对上述问题，华南理工大学未来技术学院-广东省数字孪生人实验室在灵心大模型（SoulChat1.0）基础上，推出了心理咨询师数字孪生大模型SoulChat2.0。SoulChat2.0首次定义了特定心理咨询师的数字孪生（PsyDT, Psychological consultant Digital Twin）任务：

$$
r = f_{LLM}(c|C_{N},D_{st},KB_{the.})
$$

其中 $c$ 表示咨询对话历史。 $C_{N}$ 表示 $N$ 个真实世界咨询师的咨询案例。 $D_{st}$ 表示用于构建大规模数字孪生数据的单轮咨询案例（来自互联网或者虚构的）。 $KB_{the.}$ 表示心理咨询技术知识库。

如下图所示，心理咨询师数字孪生大模型SoulChat2.0包含2个部分：（1）心理咨询师数字孪生数据生成；（2）心理咨询师数字孪生建模。

<p align="center">
    <img src="./figure/multi_turn_dialogue_generation_framework.png" width=900px/>
</p>

### （1）心理咨询师数字孪生数据生成

要实现特定的心理咨询师的数字孪生，前提是能获取该心理咨询师的大量咨询案例，但是这对于心理咨询师个体而言，难度极大。一方面，需要考虑心理咨询的伦理要求和隐私保护，另一方面，数据的采集也非常繁琐。为此，有必要建立一种仅需少量咨询案例的心理咨询师数字孪生数据生成框架。心理咨询师的每个咨询案例都体现了本人的语言风格与咨询技术应用方式，这可以借助于现有的先进的LLMs的语言总结能力去提取。同时，为了保证生成的数据的多样性，需要尽可能建模用户的个性特质，我们以常用的大五人格为参考，对单轮对话咨询数据库中的来访者进行了大五人格分析。通过综合真实世界咨询师的语言风格、咨询技术、来访者大五人格，结合真实世界咨询案例，对于单轮对话进行心理咨询师数字孪生数据生成。采取我们的框架生成的多轮对话数据，能有效表征特定心理咨询师的语言风格与咨询技术应用方式。为了综合考虑成本与效果，我们设定了用于心理咨询师数字孪生数据生成的单轮对话咨询数据库的规模为5000个，特定心理咨询师的咨询案例数目设定为12个（为保证低成本，一般不多于20个）。最终，只需要给定任意心理咨询师的少量咨询案例，我们的框架即可快速生成批量用于该心理咨询师数字孪生建模的咨询案例。

我们进行人工评估发现，相比于Smile和SoulChat1.0，SoulChat2.0提出的数据生成方法（PsyDT_Prompt），几乎在所有话题上都能很好地构建高质量的数字孪生数据。

<p align="center">
    <img src="./figure/therapeutic_radar_chart.png" width=900px/>
</p>

### （2）心理咨询师数字孪生建模

给定用于心理咨询师数字孪生建模的咨询案例数据，可以通过微调来实现对该咨询师的数字孪生。为了方便研究社区进行对比和复现，我们选用Llama3-8B-Instruct作为基座模型，在SoulChat2.0Corpus的训练集上进行全量微调3个epoches。并且与ChatGPT、GPT-4为代表的闭源模型，Baichuan2-7B-Chat 、GLM4-9B-Chat、Meta-Llama3-8B-Instruct等7个模型为代表的开源模型，以及MeChat、PsyChat、SoulChat1.0、MindChat、EmoLLM、CPsyCounX6个心理健康领域的大模型在PsyDTCorpus的测试集进行自动化对比分析。特别地，我们对MeChat、PsyChat、SoulChat1.0、MindChat、EmoLLM、CPsyCounX以及所提出的SoulChat2.0在**谈话技术**、**状态与态度**、**情感共情**、**认知共情**、**安全性**五个维度进行轮次的对比评估。这7个心理健康大模型在安全性维度上都获得了很高的评分，表明了这些经过微调的领域大模型在安全维度上已经很好地对齐人类目标。在认知共情、会话技术、状态与态度三个维度上，PsyDTLLM相对于其他模型均有较大幅度的提升。这表明了通过心理咨询师数字孪生建模的方式，能很好地提升LLMs的真实心理咨询性能。
