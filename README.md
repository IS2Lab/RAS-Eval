# Agent Safety Benchmark

[![GitHub](https://img.shields.io/badge/github-IS2Lab-blue.svg?style=flat&logo=github)](https://is2lab.github.io/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)


# 1. Quick Start
## 1.1 Installation
Firstly, make sure you have installed `uv`, if not, please install it referenced by https://docs.astral.sh/uv/

Then install the dependencies:
```bash
uv sync
```

create a file named `.env` in the root directory, 
```bash
touch .env
```

## 1.2 Apply LLM API keys
Apply API keys for LLM providers, and add them to `.env` file, for example:
```bash
ZHIPUAI_API_KEY = ""
ZHIPUAI_BASE_URL = ""

ALIYUN_API_KEY = ""
ALIYUN_BASE_URL = ""

OPENAI_API_KEY = ""
OPENAI_BASE_URL = ""
```

We support the following LLM providers:
|Model|LLM Provider|API Key Name|Apply Address|
|:---:|:---:|:---:|:---:|
|`qwen-max`|aliyun|`ALIYUN_API_KEY`, `ALIYUN_BASE_URL`|https://bailian.console.aliyun.com/|
|`qwen-max`|aliyun|`ALIYUN_API_KEY`, `ALIYUN_BASE_URL`|https://bailian.console.aliyun.com/|
|`qwen-plus`|aliyun|`ALIYUN_API_KEY`, `ALIYUN_BASE_URL`|https://bailian.console.aliyun.com/|
|`qwen-turbo`|aliyun|`ALIYUN_API_KEY`, `ALIYUN_BASE_URL`|https://bailian.console.aliyun.com/|
|`qwen2.5-xb-instruct`|aliyun|`ALIYUN_API_KEY`, `ALIYUN_BASE_URL`|https://bailian.console.aliyun.com/|
|`ollama/llama3.3-70b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/llama3.2-3b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/llama3.2-1b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/llama3.1-8b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/qwen2.5-0.5b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/qwen2.5-1.5b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/qwen2.5-3b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/qwen2.5-7b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/qwen2.5-14b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/qwen2.5-32b`|ollama|/|https://ollama.com/search?c=tools|
|`ollama/qwen2.5-72b`|ollama|/|https://ollama.com/search?c=tools|
|`glm-4-plus`|zhipu|/|https://www.bigmodel.cn/|
|`glm-4-flash`|zhipu|/|https://www.bigmodel.cn/|

## 1.3 Apply API keys for real tools

Apply 

|API Key Name|Apply Address|
|:---:|:---:|
|`BAIDU_MAP_AK`|[BaiduMap](https://lbsyun.baidu.com/)|
|`TUSHARE_TOKEN`|[Tushare](https://tushare.pro/)|
|`TAVILY_API_KEY`|[Tavily](https://tavily.com/)|
|`OPENWEATHERMAP_API_KEY`|[OpenWeatherMap](https://openweathermap.org/)|

Then add them to `.env` file, for example:
```bash
BAIDU_MAP_AK = "YOUR_API_KEY"
TUSHARE_TOKEN = "YOUR_API_KEY"
TAVILY_API_KEY = "YOUR_API_KEY"
OPENWEATHERMAP_API_KEY = "YOUR_API_KEY"
```

## 1.4 Test
```bash
uv run main.py
```