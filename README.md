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

\[ English | [中文](README_zh.md) \]

## Introduction
Since the release of [SoulChat](https://github.com/scutcyr/SoulChat) in May 2023, we have made significant improvements in the digital twin modeling ability of psychological counselors through in-depth exploration of real-world psychological counseling language styles, psychological counseling techniques, and other aspects.

Since the birth of ChatGPT, a large amount of work has applied the Large Model (LLM) to the fields of emotional accompaniment, mental health support dialogue, and psychological counseling dialogue both domestically and internationally, such as SoulChat, MeChat, QiaoBan, CPsyCoun, MindChat, EmoLLM, and so on. However, previous work has focused on using carefully designed prompt words to construct multiple rounds of mental health dialogue datasets. The fine tuned "mental health big model" can easily lead to homogenization and templating of answers, making it difficult for these LLMs to cope with complex and changing visitors, and unable to simulate the language expression and therapeutic techniques of real psychological counselors in the real world.

In response to the above issues, Guangdong Provincial Key Laboratory of Human Digital Twin, School of Future Technology, South China University of Technology has launched the 
psychological counselor digital twin model **SoulChat 2.0** based on the SoulChat 1.0 model. SoulChat 2.0 defines the Psychological Consultant Digital Twin (PsyDT) task for specific psychological counselors for the first time :

$$
r = f_{LLM}(c|C_{N},D_{st},KB_{the.})
$$

where $c$ denotes the counseling context of a client. $C_{N}$ denotes $N$ real-world counseling cases of specific psychological counselor. $D_{st}$ represents the single-turn mental counseling dialogue dataset, while $KB_{the.}$ signifies the therapeutic strategy knowledge base. 