import requests
import json
import os
from log import logger

MODEL = "gpt-3.5-turbo"  # price = 0.75
# MODEL = "gpt-4-turbo-preview" # price = 5.00
# MODEL = "gpt-4" # price = 15.00
# MODEL = "gpt-4-32k" # price = 30.00


api_url = "https://aihubmix.com/v1/chat/completions"
api_key = os.environ.get(
    "OPENAI_TOKEN",
    "You may need to check your environment variables' confogure.",
)


# 函数：向ChatGPT提问并记录日志
def ask_chatgpt(question):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
    }
    # 在发送请求前记录用户的提问
    logger.trace(f"User question: {question}")
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        response_dict = response.json()
        # 在得到响应后记录整个响应体，保留原样
        logger.trace(
            f"OpenAI Response: {json.dumps(response_dict, ensure_ascii=False, indent=4)}"
        )
        return response_dict
    else:
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}


def show(msg: str):
    response = ask_chatgpt(msg)  # 调用ask_chatgpt函数获取OpenAI Response
    content = response["choices"][0]["message"]["content"]  # 提取content部分的内容
    logger.success(content)
    return content
