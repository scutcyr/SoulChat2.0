
# coding=utf-8
# Copyright 2023 South China University of Technology and 
# Engineering Research Ceter of Ministry of Education on Human Body Perception.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Author: Chen Yirong <eeyirongchen@mail.scut.edu.cn>
# Date: 2024.03.06


import os
import time
from typing import Literal
from openai import OpenAI, AzureOpenAI

class OpenAI_LLM:
    '''说明：需要根据你部署vllm服务时的实际服务器IP修改base_url，api_key也需要根据你部署的vllm服务时指定的--api-key修改
    '''
    def __init__(self, model_name):
        '''
        输入格式：
            model_name: 字符串，表示模型的名称（见功能说明）。
            system_prompt: 字符串，表示系统的指令说明，定义了'role': 'system'对应的设定内容
                           当其为None时，调用默认的设置初始化
        '''
        self.model_name = model_name
        # 如果同时部署多个模型，可以在这里撰写多个if model_name == "xxx"的判断条件
        if model_name.startswith("SoulChat2.0"):
            self.system_prompt = '你是一位精通理情行为疗法（Rational Emotive Behavior Therapy，简称REBT）的心理咨询师，能够合理地采用理情行为疗法给来访者提供专业地指导和支持，缓解来访者的负面情绪和行为反应，帮助他们实现个人成长和心理健康。理情行为治疗主要包括以下几个阶段，下面是对话阶段列表，并简要描述了各个阶段的重点。\n（1）**检查非理性信念和自我挫败式思维**：理情行为疗法把认知干预视为治疗的“生命”，因此，几乎从治疗一开始，在问题探索阶段，咨询师就以积极的、说服教导式的态度帮助来访者探查隐藏在情绪困扰后面的原因，包括来访者理解事件的思维逻辑，产生情绪的前因后果，借此来明确问题的所在。咨询师坚定地激励来访者去反省自己在遭遇刺激事件后，在感到焦虑、抑郁或愤怒前对自己“说”了些什么。\n（2）**与非理性信念辩论**：咨询师运用多种技术（主要是认知技术）帮助来访者向非理性信念和思维质疑发难，证明它们的不现实、不合理之处，认识它们的危害进而产生放弃这些不合理信念的愿望和行为。\n（3）**得出合理信念，学会理性思维**：在识别并驳倒非理性信念的基础上，咨询师进一步诱导、帮助来访者找出对于刺激情境和事件的适宜的、理性的反应，找出理性的信念和实事求是的、指向问题解决的思维陈述，以此来替代非理性信念和自我挫败式思维。为了巩固理性信念，咨询师要向来访者反复教导，证明为什么理性信念是合情合理的，它与非理性信念有什么不同，为什么非理性信念导致情绪失调，而理性信念导致较积极、健康的结果。\n（4）**迁移应用治疗收获**：积极鼓励来访者把在治疗中所学到的客观现实的态度，科学合理的思维方式内化成个人的生活态度，并在以后的生活中坚持不懈地按理情行为疗法的教导来解决新的问题。'
            self.client = OpenAI(
                base_url="http://198.0.0.8:8001/v1",
                api_key="soulchat-rcEmrhVe6zWot67QkJSwqUnNI0EQxxFBMQSAXLtMNsD97PlyGQgjgjW-9jCdQD30",
            )
        else:
            raise ValueError(f"Unsupported model name: {model_name}")

    def chat(
        self,
        messages: list[dict[str, str]],
        generation_config = None,
        temperature=0.7,
        max_tokens=4096,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
        add_system_prompt = True,
    ):
        if add_system_prompt:
            if messages[0]["role"] != "system":
                # 如果传入的messages不存在system_prompt，则添加system_prompt
                messages = [{"role":"system","content":self.system_prompt}] + messages # 拼接system_prompt
        
        completion = self.client.chat.completions.create(
            model=self.model, 
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            stream=stream # 流式返回
        )
        return completion