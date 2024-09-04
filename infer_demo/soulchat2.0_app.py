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


''' 运行方式

安装依赖
```bash
pip install openai==1.7.1
pip install streamlit==1.27.0
pip install streamlit_authenticator==0.3.1
```
启动服务：
```bash
streamlit run soulchat2.0_app.py --server.port 8002
```

## 测试访问

http://116.57.86.151:9026

'''

# st-chat uses https://www.dicebear.com/styles for the avatar

# https://emoji6.com/emojiall/

import os
import random
import re
import sys
import json
import time
import tiktoken
import requests
import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
from openai import OpenAI, AzureOpenAI
from openai_api_llm import OpenAI_LLM
#Note: The openai-python library support for Azure OpenAI is in preview.
#Note: This code sample requires OpenAI Python library version 1.0.0 or higher.

dialogue_history_dir = './chatgpt_history_with_users'

def get_history_chat_id():
    if not os.path.exists(dialogue_history_dir):
        # 创建保存用户聊天记录的目录
        os.makedirs(dialogue_history_dir)

    json_files = os.listdir(dialogue_history_dir)
    files = [int(os.path.splitext(file)[0]) for file in json_files]
    files = sorted(files, reverse=True)
    files = [str(file) for file in files]
    return files


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

st.set_page_config(
    page_title="心理咨询师数字孪生大模型(内测版)",
    page_icon="👩‍🔬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """     
-   版本：👩‍🔬心理咨询师数字孪生大模型(内测版)
-   版本：v1.0.0
-   机构：华南理工大学未来技术学院
	    """
    }
)

# 用户验证
with open("./user_config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

authenticator.login(
    fields={
        "Form name": "👩‍🔬心理咨询师数字孪生大模型(内测版)",
        "Username": "用户名",
        "Password": "密码",
        "Login": "登录",
    }
)

if st.session_state["authentication_status"]:
    

    if st.session_state["username"]:
        chat_history_dir = os.path.join(dialogue_history_dir, f"{st.session_state['username']}")
        if not os.path.exists(chat_history_dir):
            os.makedirs(chat_history_dir)
    else:
        chat_history_dir = None

    def get_chat_names():
        # 聊天记录命名格式：{chat_id}_{chat_name}.json
        json_names = os.listdir(chat_history_dir)
        chat_names = [x[:-5] for x in json_names if not x.endswith("_delete.json")]
        chat_names = sorted(chat_names, key=lambda x: int(x.split("_")[0]))
        return chat_names

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "total_times" not in st.session_state:
        st.session_state["total_times"] = [] # 每一轮对话的耗时

    if "model_names" not in st.session_state:
        st.session_state["model_names"] = [] # 每一轮对话调用的模型

    if "turn_costs" not in st.session_state:
        st.session_state["turn_costs"] = [] # 每一轮对话的预估成本

    if "current_times" not in st.session_state:
        st.session_state["current_times"] = [] # 每一轮对话的运行日期

    if "total_chat_num" not in st.session_state:
        st.session_state["total_chat_num"] = len(os.listdir(chat_history_dir))

    if "chat_names" not in st.session_state:
        st.session_state["chat_names"] = get_chat_names()

    if "chat_name" not in st.session_state:
        st.session_state["chat_name"] = None

    if "change_name_temp" not in st.session_state:
        st.session_state["change_name_temp"] = "" 


    # 带cache装饰器的初始加载函数
    @st.cache_resource
    def load_llm(llm_used):
        if (
            llm_used.startswith("SoulChat2.0")
        ):
            llm = OpenAI_LLM(model_name=llm_used)

        return llm

    # 侧边栏

    with st.sidebar:
        st.header("👩‍🔬心理咨询师数字孪生大模型(内测版)")
        authenticator.logout(
            button_name="退出登录",  # f"**{st.session_state['username']}**    退出登录"
            location="sidebar",
        )
        with st.expander("ℹ️ - 关于我们", expanded=False):
            st.write(
                """     
        -   版本：👩‍🔬心理咨询师数字孪生大模型(内测版)
        -   版本：v1.0.0
        -   机构：华南理工大学未来技术学院
                """
            )
        st.divider()


        if st.button("**新建对话** 💭", use_container_width=True):
            st.session_state["chat_name"] = None

        # 模型选择
        model_name = st.selectbox(
            '请选择模型的版本',
            (
                "SoulChat2.0-Qwen2-7B",
                "xxx"
             ))
        llm = load_llm(llm_used=model_name)

        temperature = st.slider('设置调用LLM的temperature', min_value = 0.0, max_value = 1.0, value = 0.75, step = 0.01)
        top_p = st.slider('设置调用LLM的top_p', min_value = 0.0, max_value = 1.0, value = 0.9, step = 0.01)
        max_tokens = 4096
        use_system_prompt=True
        disabled_stream_output = st.checkbox("禁用流式返回", key="disabled_stream_output")
        change_name_placeholder = st.empty()

        st.write("**历史对话记录**".center(48, "-"))
        chat_name_cols = []
        for key_id, chat_name in enumerate(reversed(st.session_state["chat_names"])):
            chat_name_cols.append(st.columns([0.8, 0.1, 0.1], gap="small"))
            with chat_name_cols[-1][0]:
                if st.button(
                    f"**{''.join(chat_name.split('_')[1:])}**",
                    use_container_width=True,
                    key=key_id,
                ):
                    st.session_state["chat_name"] = chat_name
            with chat_name_cols[-1][1]:
                if st.button(
                    "🗑️",
                    use_container_width=True,
                    key=f"{key_id}_trash",
                    help="删除",
                ):
                    os.rename(
                        os.path.join(
                            chat_history_dir,
                            f"{chat_name}.json",
                        ),
                        os.path.join(
                            chat_history_dir,
                            f"{chat_name}_delete.json",
                        ),
                    )
                    if st.session_state["chat_name"] == chat_name:
                        st.session_state["chat_name"] = None
                    st.session_state["chat_names"] = get_chat_names()
                    st.rerun()

    # 参数设置
 

    # 显示更改标题文本框
    def clear_input():
        st.session_state["change_name_temp"] = st.session_state["change_name_input"]
        st.session_state["change_name_input"] = ""

    if st.session_state["chat_name"] != None:
        change_name_placeholder.text_input(
            label="**更改当前对话标题**", key="change_name_input", on_change=clear_input
        )
        if st.session_state["change_name_temp"]:
            os.rename(
                os.path.join(
                    chat_history_dir,
                    f"{st.session_state['chat_name']}.json",
                ),
                os.path.join(
                    chat_history_dir,
                    f"{st.session_state['chat_name'].split('_')[0]}_{st.session_state['change_name_temp']}.json",
                ),
            )
            st.session_state["chat_name"] = (
                f"{st.session_state['chat_name'].split('_')[0]}_{st.session_state['change_name_temp']}"
            )
            st.session_state["chat_names"] = get_chat_names()
            st.session_state["change_name_temp"] = ""
            st.rerun()

    # 显示选中对话标记，
    if st.session_state["chat_name"] != None:
        with chat_name_cols[
            list(reversed(st.session_state["chat_names"])).index(
                st.session_state["chat_name"]
            )
        ][2]:
            st.write("🚩")

    # 读取历史消息
    if chat_history_dir != None and st.session_state["chat_name"] != None:
        with open(
            os.path.join(chat_history_dir, f"{st.session_state['chat_name']}.json"),
            "r",
            encoding="utf-8",
        ) as f:
            total_json_data = json.load(f)
            st.session_state["messages"] = total_json_data['messages']
            st.session_state["total_times"] = total_json_data['total_times']
            st.session_state["model_names"] = total_json_data['model_names']
            st.session_state["turn_costs"] = total_json_data['turn_costs']
            st.session_state["current_times"] = total_json_data['current_times']

    else:
        st.session_state["messages"] = []
        st.session_state["total_times"] = [] # 每一轮对话的耗时
        st.session_state["model_names"] = [] # 每一轮对话调用的模型
        st.session_state["turn_costs"] = [] # 每一轮对话的预估成本
        st.session_state["current_times"] = [] # 每一轮对话的运行日期
        


    # 显示对话标题
    if st.session_state["chat_name"] != None:
        st.title("".join(st.session_state["chat_name"].split("_")[1:]))

    # 显示历史对话信息
    i = 0
    for message in st.session_state["messages"]:
            if message["role"] == "system":
                # 不显示system_prompt
                continue
            else:
                avatar = '🧑‍💻' if message["role"] == "user" else '👩‍🔬'
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

                    if message["role"] == "assistant":
                        total_time = st.session_state["total_times"][i]
                        model_name = st.session_state["model_names"][i]
                        turn_cost = st.session_state["turn_costs"][i]
                        current_time = st.session_state["current_times"][i]

                        with st.expander(label="*Related Information*"):
                            st.write(
                                f"time=**{total_time:.2}s**, model_name=**{model_name}**, turn_cost=**{turn_cost:.2}**元，日期：{current_time}"
                            )

    # 当前轮对话处理
    query = st.chat_input("Shift + Enter 换行, Enter 发送")
    if query:

        with st.chat_message(name="user", avatar="🧑‍💻"):
            st.write(query)

        #if len(st.session_state["messages"]) == 0 and use_system_prompt and st.session_state["system_prompt"]:
        #    st.session_state["messages"].append({"role":"system","content":st.session_state["system_prompt"]})


        st.session_state["messages"].append({"role": "user", "content": query}) # 把最新的输入加到messages
        print(f"[user] {query}", flush=True)

        with st.chat_message("assistant", avatar='👩‍🔬'):
            placeholder = st.empty()
            #data = {"model": model_name, "messages": st.session_state["messages"], "stream": False}
            start_time = time.time()


            messages = st.session_state["messages"]

            completion = llm.chat(
                        messages = messages,
                        temperature=temperature,
                        max_tokens=4096,
                        top_p=top_p,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stop=None,
                        stream=not disabled_stream_output,
                        add_system_prompt = use_system_prompt
                    )
            
            response = ""
            if disabled_stream_output:
                response = completion.choices[0].message.content
                placeholder.markdown(response)

            else:
                # 流式返回
                for chunk in completion:
                    #print("chunk=", chunk)
                    if isinstance(llm, OpenAI_LLM):
                        #print("LLM为OpenAI_LLM")
                        if chunk.choices:
                            new_token = chunk.choices[0].delta.content or ""
                        else:
                            new_token = ""
                            continue
                    else:
                        # 本地部署模型
                        new_token = chunk

                    response += new_token
                    placeholder.markdown(response)
    
            end_time = time.time()
            total_time = end_time - start_time
            current_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

            # 可以增加基于tokens的成本计算公式
            turn_cost = 0.00

            with st.expander(label="*Related Information*"):
                st.write(
                    f"time=**{total_time:.2}s**, model_name=**{model_name}**, turn_cost=**{turn_cost:.2}**元, 日期：{current_time}"
            )

        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.session_state["total_times"].append(total_time)
        st.session_state["model_names"].append(model_name)
        st.session_state["turn_costs"].append(turn_cost)
        st.session_state["current_times"].append(current_time)

        total_information = {
            "messages": st.session_state["messages"],
            "total_times": st.session_state["total_times"],
            "model_names": st.session_state["model_names"],
            "turn_costs": st.session_state["turn_costs"],
            "current_times": st.session_state["current_times"],
        } # 保存对话历史及相关信息
 
        print(json.dumps(st.session_state["messages"], ensure_ascii=False), flush=True)

        if st.session_state["chat_name"] == None:

            user_query_0 = st.session_state["messages"][0]['content'][:10].strip()

            st.session_state["chat_name"] = (
                f"{st.session_state['total_chat_num']}_{user_query_0}"
            )
            st.session_state["chat_names"].append(st.session_state["chat_name"])
            with open(
                os.path.join(chat_history_dir, f"{st.session_state['chat_name']}.json"),
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(total_information, f, indent=4, ensure_ascii=False)
            st.session_state["total_chat_num"] += 1
            st.rerun()

        with open(
            os.path.join(chat_history_dir, f"{st.session_state['chat_name']}.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(total_information, f, indent=4, ensure_ascii=False)


elif st.session_state["authentication_status"] is False:
    st.error("用户名/密码 不正确")
elif st.session_state["authentication_status"] is None:
    st.warning("请输入用户名和密码")
