import json
import os
import sys
from typing import List

from .api.openai import (
    openai_audio_speech,
    openai_chat_completion,
    openai_images_generations,
    openai_models,
)

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.log import logger
from module.storage import PROJECT_FOLDER, get_user_folder, init


def ask(msg: str, available_models: List[str], default_amount: int = 1):
    response = openai_chat_completion(
        msg, available_models, amount=default_amount
    )
    try:
        choices = response.get("choices", [])

        # 使用.get()方法更安全地访问字典键值，以避免KeyError异常
        response_usage_completion_tokens = response.get("usage", {}).get(
            "completion_tokens", -1
        )
        response_usage_prompt_tokens = response.get("usage", {}).get(
            "prompt_tokens", -1
        )
        response_usage_total_tokens = response.get("usage", {}).get(
            "total_tokens", -1
        )

        # 假设这里有一些处理response的代码

    except Exception as e:
        # 记录关键错误信息而不是直接退出程序，提供更好的错误上下文
        logger.exception(f"An error occurred: {e}", exc_info=True)
        # 可以在这里处理特定的清理工作，如果有必要的话
        # 最后，可能会根据程序的需要选择是否退出
        # sys.exit()

    # 使用展平路径的变量名进行日志记录
    logger.debug(
        "[Token Usage]\n"
        + json.dumps(
            {
                "response_usage_completion_tokens": response_usage_completion_tokens,
                "response_usage_prompt_tokens": response_usage_prompt_tokens,
                "response_usage_total_tokens": response_usage_total_tokens,
                # 计算验证
                "verify": f"{response_usage_completion_tokens} + {response_usage_prompt_tokens} = {response_usage_completion_tokens + response_usage_prompt_tokens}",
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=False,
        )
    )

    # 根据choices的数量来输出
    for i, choice in enumerate(choices):
        logger.success(
            f"[Answer] ({i + 1}/{len(choices)})\n{choice['message']['content']}"
        )

    # 为了保持函数的兼容性（返回单一或多个答案），返回整个choices列表的消息内容
    return [choice["message"]["content"] for choice in choices]


def chat():
    init()
    available_models = openai_models("gpt")

    with open(
        os.path.join(
            get_user_folder(), PROJECT_FOLDER, "terminal", "question.txt"
        ),
        "r",
        encoding="utf-8",
    ) as file:
        msg = file.read()

    flag_continue = True
    conversation = ask(msg, available_models)

    if not flag_continue:
        with open(
            os.path.join(
                get_user_folder(), PROJECT_FOLDER, "terminal", "answer.txt"
            ),
            "w",
            encoding="utf-8",
        ) as file:
            file.write(conversation)
    else:
        flag_end = False
        while not flag_end:
            import time

            # 部分控制台输入是异步的，给足够的时间以保证不会打断输出
            time.sleep(0.05)
            logger.info("[Interaction] 请输入追问")
            append_question = input()
            append_question_judge = append_question.replace("\n", "").replace(
                " ", ""
            )
            if append_question_judge != "END" and append_question_judge != "":
                conversation = ask(append_question, available_models)
            else:
                flag_end = True
                break


def talk():
    init()
    available_models = openai_models("tts")

    with open(
        os.path.join(
            get_user_folder(), PROJECT_FOLDER, "terminal", "question.txt"
        ),
        "r",
        encoding="utf-8",
    ) as f:
        msg = f.read()
    openai_audio_speech(msg)


def draw():
    init()
    available_models = openai_models("dall-e")
    with open(
        os.path.join(
            get_user_folder(), PROJECT_FOLDER, "terminal", "question.txt"
        ),
        "r",
        encoding="utf-8",
    ) as f:
        msg = f.read()
    openai_images_generations(msg)


def main():
    logger.critical("THIS PROGRAM NOT INTENT TO RUN SUBMODULE".upper())
    exit(0)


if __name__ == "__main__":
    main()
