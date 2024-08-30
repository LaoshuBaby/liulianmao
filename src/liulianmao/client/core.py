import json
import os
import sys
from typing import Dict, List, Union

from .agent import get_agent_judge_template
from .api.llama import llama_completion
from .api.openai import (
    openai_audio_speech,
    openai_chat_completion,
    openai_chat_completion_vision,
    openai_images_generations,
    openai_models,
)
from .api.zhipu import zhipu_completion, zhipu_completion_vision

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.config import load_conf
from module.log import logger
from module.model import select_model
from module.storage import PROJECT_FOLDER, get_user_folder, init


def ask(
    msg: str,
    available_models: List[str] = [],
    default_amount: int = 1,
    model_series: str = "openai",
    no_history: bool = False,
    image_type: str = "none",  # none/base64/url in lower case
    **kwargs,
):
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
    logger.info(f"[model_series]: {model_series}")

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

    config = load_conf()
    if config["environ"]["LIULIANMAO_RUNTIME"]=="SERVERLESS":
        # manually init config with used value
        # indeed all storaged in storage.py but I'm lazy in trying to write only once
        config["system_message"]["content"]="You are a helpful assistant."
        config["settings"]["temperature"]=kwargs.get("temperature",0.5)
        config["model_type"]={
        "openai": "gpt-4-turbo-preview",
        "zhipu": "glm-4"
    }


    import base64
    import re

    image_path = ""
    feature_vision = False

    def get_image_argument():
        logger.trace("尝试使用 get_image_argument 读取图片")
        global image_path, feature_vision
        if (
            kwargs.get("image", None) != None
            and kwargs.get("image", None) != ""
        ):
            image_path = kwargs["image"]
            logger.debug(f"[image_path]: {image_path}")

            feature_vision = True

        else:
            image_path = ""
            feature_vision = False

        if feature_vision:
            return True
        return False

    def get_image_prompt():
        logger.trace("尝试使用 get_image_prompt 读取图片")
        global image_path, feature_vision
        if msg[0:11] == "```IMG_PATH":
            match = re.search(r"IMG_PATH\n(.+)", msg)
            if match:
                image_path = match.group(1)
                logger.debug(f"[image_path]: {image_path}")

                feature_vision = True
        else:
            image_path = ""
            feature_vision = False

        if feature_vision:
            return True
        return False

    def get_image_clip():
        logger.trace("尝试使用 get_image_clip 读取图片")
        global image_path, feature_vision

        def get_windows_clip():
            import platform
            from io import BytesIO
            from PIL import Image, ImageGrab
            import base64

            if platform.system() != "Windows":
                logger.info(
                    "Clipboard image capture is only supported on Windows."
                )
                return ""

            try:
                image = ImageGrab.grabclipboard()
                if image is None or not isinstance(image, Image.Image):
                    logger.info("No image found in clipboard.")
                    return ""

                buffered = BytesIO()
                image.save(buffered, format="PNG")
                return base64.b64encode(buffered.getvalue()).decode("utf-8")
            except ImportError:
                logger.error(
                    "PIL or ImageGrab module not found. Please install pillow."
                )
            except Exception as e:
                logger.error(f"Error capturing clipboard image: {e}")

            return ""

        image_clip = get_windows_clip()
        if image_clip != None and image_clip != "":
            image_path = image_clip
            logger.trace(f"[clip_image]:\n{image_path}")
            logger.debug(f"[clip_image] 图像Base64长度为 {len(image_path)}")

            feature_vision = True

        if feature_vision:
            return True
        return False

    def get_image():
        global image_path, feature_vision
        if get_image_argument():
            logger.warning("[Fairy] 检测到您通过参数传入了一张图片的路径")
            logger.success("[Fairy] 将尝试调用包含视觉功能的模型（若支持）")
        elif get_image_prompt():
            logger.warning("[Fairy] 检测到您在prompt开始处输入了一张图片的路径")
            logger.success("[Fairy] 将尝试调用包含视觉功能的模型（若支持）")
        elif get_image_clip():
            logger.warning("[Fairy] 检测到您剪贴板当前内容为一张图片并成功从Windows剪贴板读取了图片")
            logger.success("[Fairy] 将尝试调用包含视觉功能的模型（若支持）")
        return image_path, feature_vision

    image_path, feature_vision = get_image()

    logger.debug(f"[feature_vision]: {feature_vision}")
    logger.debug(f"[image_path]: {len(image_path)}")

    if image_path != "":
        if image_path[0:4] == "http":
            image = image_path
            logger.debug(f"[Fairy] 图像地址为链接 {image}")
        elif len(image_path) >= 1024:
            # 这么长的肯定是raw数据
            image = image_path
            logger.debug(f"[Fairy] 图像地址为Base64，长度为 {len(image)}")
        else:

            def image_to_base64(image_path):
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                    base64_encoded_data = base64.b64encode(image_data)
                    base64_message = base64_encoded_data.decode("utf-8")
                    return base64_message

            image = image_to_base64(image_path)
            logger.debug(f"[Fairy] 图像地址为Base64，长度为 {len(image)}")

    if model_series == "openai":
        if feature_vision == True:
            response = openai_chat_completion_vision(
                msg=msg,
                image=image,
                prompt_system=config["system_message"]["content"],
                model="gpt-4o",
                temperature=float(config["settings"]["temperature"]),
                amount=default_amount,
                no_history=no_history,
            )
        else:
            response = openai_chat_completion(
                prompt_question=msg,
                prompt_system=config["system_message"]["content"],
                model=select_model(
                    config["model_type"]["openai"],
                    available_models,
                    direct_debug=True,
                ),
                temperature=float(config["settings"]["temperature"]),
                amount=default_amount,
                no_history=no_history,
            )

    elif model_series == "zhipu":
        if feature_vision == True:
            response = zhipu_completion_vision(
                msg=msg,
                image=image,
                model=config["model_type"]["zhipu"],
                no_history=no_history,
            )
        else:
            response = zhipu_completion(
                msg=msg,
                model=config["model_type"]["zhipu"],
                no_history=no_history,
            )
    elif model_series == "llama":
        response = llama_completion(
            prompt_question=msg,
            prompt_system=config["system_message"]["content"],
            model=config["model_type"].get("llama", "llama3"),
            no_history=no_history,
        )
    else:
        response = {"choices": [{"message": {"content": "啊哈？"}}]}

    try:
        # response = json.loads(response.text)
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

        # 使用展平路径的变量名进行日志记录，仅在包含token记录时
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

    except Exception as e:
        # 记录关键错误信息而不是直接退出程序，提供更好的错误上下文
        # logger.error(response)
        # logger.error(response.text)
        logger.exception(f"An error occurred: {e}", exc_info=True)
        # 可以在这里处理特定的清理工作，如果有必要的话
        # 最后，可能会根据程序的需要选择是否退出
        # sys.exit()

    # 根据choices的数量来输出
    for i, choice in enumerate(choices):
        logger.success(
            f"[Answer] ({i + 1}/{len(choices)})\n{choice['message']['content']}"
        )

    # 为了保持函数的兼容性（返回单一或多个答案），返回整个choices列表的消息内容
    return [choice["message"]["content"] for choice in choices]


def agent_judge(msg, available_models, model_series):
    func_file_list = list(
        filter(
            bool,
            [
                i if (i != "__init__.py" and i != "__pycache__") else ""
                for i in os.listdir(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        "utils",
                    )
                )
            ],
        )
    )
    logger.debug(f"[func_file_list]: {func_file_list}")

    func_proto_list = []

    def extract_function_prototypes(code):
        import re

        pattern = r"^def\s+(.*?)\((.*?)\)\s*->\s*(.*?)\s*:"
        matches = re.findall(pattern, code, re.MULTILINE)

        function_prototypes = []
        for match in matches:
            function_name = match[0]
            args = match[1]
            return_annotation = match[2]
            function_prototypes.append(
                f"def {function_name}({args}) -> {return_annotation}"
            )

        return function_prototypes

    func_do_not_use_this_prototype = ["get_search_result"]

    for func_file in func_file_list:
        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "utils",
                func_file,
            ),
            "r",
            encoding="utf-8",
        ) as f:
            code = f.read()
            prototypes = extract_function_prototypes(code)
            for prototype in prototypes:
                logger.trace(prototype)

                def extract_function_name(proto_string):
                    import re

                    pattern = r"^def\s+(\w+)"
                    match = re.search(pattern, proto_string, re.MULTILINE)
                    if match:
                        return match.group(1)
                    return None

                # logger.trace(f"[extract_function_name(prototype)]:`{extract_function_name(prototype)}`")
                if (
                    extract_function_name(prototype)
                    not in func_do_not_use_this_prototype
                ):
                    func_proto_list.append(prototype)

    feature_use_native_functioncall = False
    logger.warning(
        f"Agent设定为启用，即将判断是否需要调用本地函数 (method={'model_native'+'.'+model_series if feature_use_native_functioncall==True else 'liulianmao_agent'})"
    )

    if feature_use_native_functioncall == True and (
        model_series.lower() == "zhipu" and "glm-4" in available_models
    ):
        # 专用schema
        # tools_list后续应根据func_proto_list生成，此处仅为示意
        tools_list = [
            {
                "type": "function",
                "function": {
                    "name": "get_random_shengxiao",
                    "description": "随机选择一个生肖",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "select": {
                                "description": "强制钦点一个生肖",
                                "type": "string",
                            }
                        },
                        "required": [],
                    },
                },
            }
        ]

        # 召唤判定
        agent_judge_conversation = ask(
            msg,
            available_models,
            model_series=model_series,
            no_history=True,
            tools=tools_list,
        )[0]
        logger.trace(
            f"[agent_judge_conversation]:\n{agent_judge_conversation}"
        )
    else:
        # 土法炼钢
        agent_judge_question = (
            get_agent_judge_template()
            .replace("{func_list}", "\n".join(func_proto_list))
            .replace("{question}", msg)
        )
        logger.trace(f"[agent_judge_question]:\n{agent_judge_question}")

        # 召唤判定
        agent_judge_conversation = ask(
            agent_judge_question,
            available_models,
            model_series=model_series,
            no_history=True,
        )[0]
        logger.trace(
            f"[agent_judge_conversation]:\n{agent_judge_conversation}"
        )

    def extract_agent_variables(input_str: str) -> Dict[str, str]:
        slice_input = input_str.split("\n")
        valid_tag = list(
            filter(
                bool,
                [i if "AGENT" in i else "" for i in slice_input],
            )
        )

        agent_dict = {}
        for line in valid_tag:
            parts = line.split(":", 1)  # 限制分割一次，防止冒号在值中出现
            if len(parts) == 2:
                key, value = parts
                agent_dict[key] = value.strip()  # 移除值前后的空格

        return agent_dict

    try:
        agent_judge_result = extract_agent_variables(agent_judge_conversation)
    except Exception as e:
        logger.error(e)
        agent_judge_result = {"AGENT": "FALSE"}
    logger.debug(f"[agent_judge_result]: {agent_judge_result}")
    return agent_judge_result


def chat(
    model_series: str = "openai",
    feature_agent: bool = False,
    feature_continue: Union[bool, int] = True,
):
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

    logger.info(f"[feature_continue]: {feature_continue}")
    logger.info(f"[feature_agent]: {feature_agent}")

    if model_series == "openai":
        available_models = openai_models("gpt")
    elif model_series == "zhipu":
        available_models = ["glm-4", "glm-3-turbo", "glm-4v"]
    elif model_series == "llama":
        available_models = ["llama3"]
    else:
        available_models = []

    with open(
        os.path.join(
            get_user_folder(), PROJECT_FOLDER, "terminal", "question.txt"
        ),
        "r",
        encoding="utf-8",
    ) as file:
        msg = file.read()

    def agent_run(msg, agent_judge_result):
        # 找到 AGENT.ACTION.NAME 对应的函数并调用一下

        logger.trace(
            "\n"
            + f"[run_agent.msg]:\n{msg}"
            + "\n"
            + f"[run_agent.agent_judge_result]:\n{agent_judge_result}"
        )

        ## 构建函数文件库

        func_file_list = list(
            filter(
                bool,
                [
                    i if (i != "__init__.py" and i != "__pycache__") else ""
                    for i in os.listdir(
                        os.path.join(
                            os.path.dirname(os.path.realpath(__file__)),
                            "utils",
                        )
                    )
                ],
            )
        )

        ## 尝试找到需要import的文件

        target_file_name = ""
        for func_file in func_file_list:
            with open(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "utils",
                    func_file,
                ),
                "r",
                encoding="utf-8",
            ) as f:
                code = f.read()
                if agent_judge_result["AGENT.ACTION.NAME"] in code:
                    target_file_name = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        "utils",
                        func_file,
                    )
                    break

        logger.debug(f"[target_file_name]: {target_file_name}")

        ## 尝试import那个文件并调用函数

        import importlib
        import json

        module_name = target_file_name.replace(".py", "")
        spec = importlib.util.spec_from_file_location(
            module_name, target_file_name
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        logger.success("[Agent] dynamical load called file")

        action_name = agent_judge_result["AGENT.ACTION.NAME"]
        params = json.loads(agent_judge_result["AGENT.ACTION.PARA"])

        logger.debug(f"[action_name]: {action_name}")
        logger.debug(f"[params]: {params}")
        logger.debug(f"[type(params)]: {type(params)}")

        try:
            # 获取并执行模块中的函数
            function_to_call = getattr(module, action_name)

            if callable(function_to_call):
                # 调用函数并传入参数

                for k, v in params.items():
                    logger.trace(f"[params.{k}({type(k)},{type(v)})]: {v}")
                result = function_to_call(**params)
                # result = function_to_call(city=params["city"])
                # 打印或返回结果
                if "\n" in result:
                    logger.info(f"\n{result}")
                else:
                    logger.info(result)
            else:
                logger.error(
                    f"Error: {action_name} is not a callable function."
                )
        except Exception as e:
            logger.error(f"[Error]: {e}")

        ## 在msg前面添加内容
        try:
            msg = (
                json.dumps(
                    {
                        "AGENT.ACTION.NAME": agent_judge_result[
                            "AGENT.ACTION.NAME"
                        ],
                        "AGENT.ACTION.PARA": agent_judge_result[
                            "AGENT.ACTION.PARA"
                        ],
                        "AGENT.EXEC.RESULT": result,
                    },
                    indent=2,
                    ensure_ascii=False,
                    sort_keys=False,
                )
                + ("\n" + "-" * 30 + "\n")
                + "上述为执行函数调用的结果，请根据结果回答如下的输入"
                + ("\n" + "-" * 30 + "\n")
                + msg
            )
        except Exception as e:
            logger.error(f"An error occurred while modify msg: {e}")

        return msg

    if type(feature_continue) == type(0):
        logger.warning(f"本次对话最大限制轮数: {feature_continue}")
        max_count_round = feature_continue
    count_round = 0

    # call judge agent
    if feature_agent == True:
        agent_judge_result = agent_judge(msg, available_models, model_series)
    # conduct conversation
    if feature_agent == True and agent_judge_result.get("AGENT", False) in [
        "TRUE",
        True,
    ]:
        msg = agent_run(msg, agent_judge_result)
        logger.trace(f"[modified_msg]:\n{msg}")
    count_round += 1
    conversation = ask(
        msg,
        available_models,
        model_series=model_series,
        image="",
    )

    if not feature_continue:
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
            if type(feature_continue) == type(0):
                logger.warning(f"当前已进行对话轮数：{count_round}")
                if count_round >= max_count_round:
                    logger.error(f"对话轮数达到上限")
                    break

            import time

            # 部分控制台输入是异步的，给足够的时间以保证不会打断输出
            time.sleep(0.05)
            logger.info("[Interaction] 请输入追问")
            append_question = input()
            append_question_normalized = (
                append_question.replace("\n", "")
                .replace(" ", "")
                .replace(" ", "")
            )
            if append_question_normalized not in ["END", "", "/bye"]:
                msg = append_question
                if feature_agent == True:
                    agent_judge_result = agent_judge(
                        msg, available_models, model_series
                    )
                if feature_agent == True and agent_judge_result.get(
                    "AGENT", False
                ) in ["TRUE", True]:
                    msg = agent_run(msg, agent_judge_result)
                    logger.trace(f"[modified_msg]:{msg}")
                conversation = ask(
                    msg,
                    available_models,
                    model_series=model_series,
                )

                count_round += 1
            else:
                flag_end = True
                logger.success("再见！")
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


def draw(model_series: str = "openai"):
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

    if model_series == "openai":
        available_models = openai_models("dall-e")
    elif model_series == "zhipu":
        available_models = ["cogview-3"]
    else:
        available_models = []

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
