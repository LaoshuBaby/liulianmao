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


def ask(msg: str, available_models: List[str] = [], default_amount: int = 1):
    """
    Sends a message to the OpenAI chat completion API and processes the response.

    This function sends a given message to the OpenAI API, specifying the models
    to be used and the default amount of completions to return. It processes the
    API's response, logs token usage, and returns the content of the choices.

    Args:
        msg: A string containing the message to be sent to the OpenAI API.
        available_models: A list of strings representing the models available for completion.
        default_amount: An optional integer specifying the number of completions to return. Defaults to 1.

    Returns:
        A list of strings containing the content of the responses from the API.

    Raises:
        Exception: An error occurred in processing the API response or in logging.
    向OpenAI聊天完成API发送消息并处理响应。

    此函数将给定消息发送到OpenAI API，指定要使用的模型和返回的默认完成数量。它处理API的响应，记录令牌使用情况，并返回选择内容。

    参数：
        msg: 一个字符串，包含要发送到OpenAI API的消息。
        available_models: 一个字符串列表，代表完成任务可用的模型。
        default_amount: 一个可选的整数，指定要返回的完成数量。默认为1。

    返回：
        一个字符串列表，包含来自API的响应内容。

    抛出：
        Exception: 处理API响应或记录时发生错误。
    """
    if msg == "":
        logger.warning(
            "\n"
            + "You run /client.core.ask() without pass a question to it."
            + "\n"
            + "Maybe you are run headless want a one-time-one-sentence ask and don't want to chat a lot"
        )
        msg = "你好！你会喵喵叫吗！"
    if available_models == []:
        logger.info(
            "\n"
            + "You run /client.core.ask() without pass available model to it. "
            + "\n"
            + "Don't worry, liulianmao will auto fetch this."
        )
        available_models = openai_models("gpt")
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
    """
    Initiates a chat conversation by reading a question from a file and calling the OpenAI API.

    This function initializes the environment, reads a question from a specified file,
    and uses the OpenAI API to generate a conversation based on the available models.
    It handles user input for follow-up questions and writes the conversation to a file if desired.

    No arguments or return values. This function operates through side effects such as file IO and logging.

    通过从文件中读取一个问题并调用OpenAI API来启动一个聊天对话。

    此功能初始化环境，从指定文件读取一个问题，并使用OpenAI API根据可用模型生成对话。
    它处理用户输入的后续问题，并在需要时将对话写入文件。

    没有参数或返回值。此功能通过文件IO和日志记录等副作用进行操作。
    """
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
    """
    Generates audio speech from a text question using the OpenAI API.

    This function initializes the environment, reads a question from a specified file,
    and sends the question to the OpenAI API for audio speech generation based on the available models.

    No arguments or return values. This function operates through side effects such as file IO and API communication.

    使用OpenAI API从文本问题生成音频语音。

    此功能初始化环境，从指定文件读取一个问题，并将该问题发送到OpenAI API以基于可用模型生成音频语音。

    没有参数或返回值。这个函数通过文件IO和API通信等副作用来操作。
    """
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
    """
    Generates image content from a text prompt using the OpenAI API.

    This function initializes the environment, reads a prompt from a specified file,
    and sends the prompt to the OpenAI API for image generation based on the available models.

    No arguments or return values. This function operates through side effects such as file IO and API communication.

    使用OpenAI API根据文本提示生成图像内容。

    此函数初始化环境，从指定文件读取提示，并将提示发送到OpenAI API以基于可用模型生成图像。

    此函数没有参数或返回值。此函数通过文件IO和API通信等副作用进行操作。
    """
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
    """
    Main function intended as the entry point of the program when run as a script.

    This function logs a critical message and exits, indicating that the program
    is not intended to run as a submodule.

    No arguments or return values. This function operates through side effects such as logging and exiting the program.

    主要功能旨在作为程序运行为脚本时的入口点。

    此函数记录关键消息并退出，指示该程序不打算作为子模块运行。

    没有参数或返回值。此函数通过日志记录和退出程序等副作用进行操作。
    """
    logger.critical("THIS PROGRAM NOT INTENT TO RUN SUBMODULE".upper())
    exit(0)


if __name__ == "__main__":
    main()
