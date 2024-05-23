import json
import os

from .const import PROJECT_FOLDER, get_user_folder
from .log import logger


def init():
    # 假设file_list中的JSON字符串需要格式化
    file_list = [
        (["terminal", "question.txt"], "Hello World!"),
        (["terminal", "answer.txt"], "Hello! How can I assist you today?"),
        # 使用json.dumps()格式化JSON字符串，并指定缩进为4个空格
        (
            ["assets", "config.json"],
            json.dumps(
                {
                    "model_type": {
                        "openai": "gpt-4-turbo-preview",
                        "zhipu": "glm-4",
                    },
                    "system_message": {
                        "content": "You are a helpful assistant."
                    },
                    "settings": {"temperature": 0.5},
                },
                indent=4,
            ),
        ),
    ]
    folder_list = ["logs", "audios", "images", "terminal", "assets"]

    for folder in folder_list:
        folder_path = os.path.join(get_user_folder(), PROJECT_FOLDER, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    for file_path_parts, default_content in file_list:
        file_path = os.path.join(
            get_user_folder(), PROJECT_FOLDER, *file_path_parts
        )
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file.read()
        except FileNotFoundError:
            logger.error(
                f"{'/'.join(file_path_parts)} not found. Creating a new file."
            )
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(default_content)
