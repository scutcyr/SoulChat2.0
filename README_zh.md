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

# 简介
自2023年5月发布SoulChat以来，我们经过对真实世界心理咨询语言风格、心理咨询技术等方面的深入探索，在心理咨询师数字孪生建模能力上取得了显著提升。

ChatGPT诞生以来，国内外已有大量的工作将大模型（LLM）应用于情感陪护、心理健康支持对话、心理咨询对话领域，例如SoulChat、MeChat、QiaoBan、CPsyCoun、MindChat、EmoLLM等等。然而，过往的工作聚焦于借助精心设计的提示词来构建多轮心理健康对话数据集，微调出的“心理健康大模型”很容易造成回答的同质化、模板化，使得这些LLMs难以应对复杂多变的来访者，无法很好模拟现实世界真实心理咨询师的语言表达与疗法技术运用风格。

针对上述问题，华南理工大学未来技术学院-广东省数字孪生人实验室在灵心大模型（SoulChat1.0）基础上，推出了心理咨询师数字孪生大模型SoulChat2.0。SoulChat2.0首次定义了特定心理咨询师的数字孪生（PsyDT, Psychological consultant Digital Twin）任务：

$$
r = f_{LLM}(c|C_{N},D_{st},KB_{the.})
$$
