import requests
import json
import os
from loguru import logger
from datetime import datetime

MODEL = "gpt-3.5-turbo" # price = 0.75
# MODEL = "gpt-4-turbo-preview" # price = 5.00
# MODEL = "gpt-4" # price = 15.00
# MODEL = "gpt-4-32k" # price = 30.00


# 动态获取当前用户的主目录路径
user_home_path = os.path.expanduser("~")
# 定义日志文件存储的路径
log_folder_path = os.path.join(user_home_path, ".openai_utils")

# 检查.log_folder_path是否存在，如果不存在，则创建
if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

# 配置logger，设置日志的存储文件，这里我们使用当前时间为日志文件命名
logger.add(
    os.path.join(
        log_folder_path, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    ),
    format="{time} {level} {message}",
    level="TRACE",
)


with open("api.conf", "r") as file:
    data = json.load(file)
    api_url = data.get("api_url")
    api_key = data.get("api_key")


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
