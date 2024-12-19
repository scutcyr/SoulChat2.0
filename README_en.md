# [Psychological Counselor's Digital Twin（SoulChat2.0）](https://github.com/scutcyr/SoulChat2.0)
<p align="center">
    <a href="https://arxiv.org/pdf/2412.13660"><img src="https://img.shields.io/badge/Paper-PDF-red.svg"></a>
    <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache%202-red.svg"></a>
    <a href="support os"><img src="https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/python-3.8+-aff.svg"></a>
    <a href="https://github.com/scutcyr/SoulChat2.0/graphs/contributors"><img src="https://img.shields.io/github/contributors/scutcyr/SoulChat2.0?color=9ea"></a>
    <a href="https://github.com/scutcyr/SoulChat2.0/commits"><img src="https://img.shields.io/github/commit-activity/m/scutcyr/SoulChat2.0?color=3af"></a>
    <a href="https://github.com/scutcyr/SoulChat2.0/issues"><img src="https://img.shields.io/github/issues/scutcyr/SoulChat2.0?color=9cc"></a>
    <a href="https://github.com/scutcyr/SoulChat2.0/stargazers"><img src="https://img.shields.io/github/stars/scutcyr/SoulChat2.0?color=ccf"></a>
</p>

\[ English | [中文](README.md) \]

## News
- 👏🏻  2024.12.19: Our paper has released on the arXiv: [PsyDT: Using LLMs to Construct the Digital Twin of Psychological Counselor with Personalized Counseling Style for Psychological Counseling](https://arxiv.org/pdf/2412.13660)

## Data Download
* [PsyDTCorpus](https://modelscope.cn/datasets/YIRONGCHEN/PsyDTCorpus)

## Model Download
In order to facilitate further research in the mental health dialogue research community, we plan to open source a series of psychological counselor digital twin models that have undergone full parameter fine-tuning, as shown in the table below：

| Models | Download Link | Foundation Model Download Link |
|:------------|:----------:|:------------|
| SoulChat2.0-Qwen2-7B    | [download from modelscope](https://modelscope.cn/models/YIRONGCHEN/SoulChat2.0-Qwen2-7B) | [Qwen2-7B-Instruct](https://www.modelscope.cn/models/qwen/Qwen2-7B-Instruct) |
| SoulChat2.0-internlm2-7b   | [download from modelscope](https://modelscope.cn/models/YIRONGCHEN/SoulChat2.0-internlm2-7b) | [internlm2-chat-7b](https://www.modelscope.cn/models/Shanghai_AI_Laboratory/internlm2-chat-7b) |
| SoulChat2.0-Baichuan2-7B    | [download from modelscope](https://modelscope.cn/models/YIRONGCHEN/SoulChat2.0-Baichuan2-7B) | [Baichuan2-7B-Chat](https://www.modelscope.cn/models/baichuan-inc/Baichuan2-7B-Chat) |
| SoulChat2.0-Llama-3.1-8B | [download from modelscope](https://modelscope.cn/models/YIRONGCHEN/SoulChat2.0-Llama-3.1-8B) | [Meta-Llama-3.1-8B-Instruct](https://www.modelscope.cn/models/LLM-Research/Meta-Llama-3.1-8B-Instruct) |
| SoulChat2.0-Llama-3-8B  | [download from modelscope](https://modelscope.cn/models/YIRONGCHEN/SoulChat2.0-Llama-3-8B) | [Meta-Llama-3-8B-Instruct](https://www.modelscope.cn/models/LLM-Research/Meta-Llama-3-8B-Instruct) |  |
| SoulChat2.0-Yi-1.5-9B    | [download from modelscope](https://modelscope.cn/models/YIRONGCHEN/SoulChat2.0-Yi-1.5-9B) | [Yi-1.5-9B-Chat-16K](https://www.modelscope.cn/models/01ai/Yi-1.5-9B-Chat-16K) |
| SoulChat2.0-glm-4-9b    | [download from modelscope](https://modelscope.cn/models/YIRONGCHEN/SoulChat2.0-glm-4-9b) | [glm-4-9b-chat](https://www.modelscope.cn/models/ZhipuAI/glm-4-9b-chat) |

## Model Inference
Assuming the IP address of your server is 198.0.0.8
### vllm inference
```bash
SERVER_MODEL_NAME=SoulChat2.0-Llama-3.1-8B
MODEL_NAME_OR_PATH=<local path>/SoulChat2.0-Llama-3.1-8B
GPU_MEMORY_UTILIZATION=0.8
PORT=8001
API_KEY=soulchat-rcEmrhVe6zWot67QkJSwqUnNI0EQxxFBMQSAXLtMNsD97PlyGQgjgjW-9jCdQD30
MAX_MODEL_LEN=20000

python -m vllm.entrypoints.openai.api_server \
    --served-model-name $SERVER_MODEL_NAME \
    --model $MODEL_NAME_OR_PATH \
    --gpu-memory-utilization $GPU_MEMORY_UTILIZATION \
    --port $PORT \
    --api-key $API_KEY \
    --max-model-len $MAX_MODEL_LEN
```

### streamlit demo construction
```bash
pip install openai==1.7.1
pip install streamlit==1.27.0
pip install streamlit_authenticator==0.3.1
cd infer_demo
streamlit run soulchat2.0_app.py --server.port 8002
```

## Citation
```bibtex
@misc{xie2024psydtusingllmsconstruct,
      title={PsyDT: Using LLMs to Construct the Digital Twin of Psychological Counselor with Personalized Counseling Style for Psychological Counseling}, 
      author={Haojie Xie and Yirong Chen and Xiaofen Xing and Jingkai Lin and Xiangmin Xu},
      year={2024},
      eprint={2412.13660},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2412.13660}, 
}
```
