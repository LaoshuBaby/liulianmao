import json
import os
import sys
from typing import Dict, List

from .api.openai import (
    openai_audio_speech,
    openai_chat_completion,
    openai_images_generations,
    openai_models,
)
from .api.zhipu import zhipu_completion
from .utils.agent import get_agent_judge_template

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from client.utils.config import load_conf
from module.log import logger
from module.model import select_model
from module.storage import PROJECT_FOLDER, get_user_folder, init


def ask(
    msg: str,
    available_models: List[str] = [],
    default_amount: int = 1,
    model_series: str = "openai",
    no_history: bool = False,
):
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

    if model_series == "openai":
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
        response = zhipu_completion(
            prompt_question=msg,
            prompt_system=config["system_message"]["content"],
            model=config["model_type"]["zhipu"],
            no_history=no_history,
        )
    else:
        response = {"choices": [{"message": {"content": "啊哈？"}}]}

    try:
        choices = response.get("choices", [])

        response_usage_completion_tokens = response.get("usage", {}).get(
            "completion_tokens", -1
        )
        response_usage_prompt_tokens = response.get("usage", {}).get(
            "prompt_tokens", -1
        )
        response_usage_total_tokens = response.get("usage", {}).get(
            "total_tokens", -1
        )

        logger.debug(
            "[Token Usage]\n"
            + json.dumps(
                {
                    "response_usage_completion_tokens": response_usage_completion_tokens,
                    "response_usage_prompt_tokens": response_usage_prompt_tokens,
                    "response_usage_total_tokens": response_usage_total_tokens,
                    "verify": f"{response_usage_completion_tokens} + {response_usage_prompt_tokens} = {response_usage_completion_tokens + response_usage_prompt_tokens}",
                },
                indent=2,
                ensure_ascii=False,
                sort_keys=False,
            )
        )

    except Exception as e:
        logger.exception(f"An error occurred: {e}", exc_info=True)

    for i, choice in enumerate(choices):
        logger.success(
            f"[Answer] ({i + 1}/{len(choices)})\n{choice['message']['content']}"
        )

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
                        "pseudo_agent",
                    )
                )
            ],
        )
    )
    logger.debug(f"[func_file_list]: {func_file_list}")

    func_proto_list = []

    def extract_function_prototypes(code):
        import re

        pattern = r"def\s+(.*?)\((.*?)\)\s*->\s*(.*?):"
        matches = re.findall(pattern, code)

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
                "pseudo_agent",
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

                if (
                    extract_function_name(prototype)
                    not in func_do_not_use_this_prototype
                ):
                    func_proto_list.append(prototype)

    agent_judge_question = (
        get_agent_judge_template()
        .replace("{func_list}", "\n".join(func_proto_list))
        .replace("{question}", msg)
    )
    logger.trace(f"[agent_judge_question]:\n{agent_judge_question}")

    logger.warning("Agent设定为启用，即将判断是否需要调用本地函数")
    agent_judge_conversation = ask(
        agent_judge_question,
        available_models,
        model_series=model_series,
        no_history=True,
    )[0]
    logger.trace(f"[agent_judge_conversation]:\n{agent_judge_conversation}")

    def extract_pseudo_agent_variables(input_str: str) -> Dict[str, str]:
        slice_input = input_str.split("\n")
        valid_tag = list(
            filter(
                bool,
                [i if "PSEUDO_AGENT" in i else "" for i in slice_input],
            )
        )

        pseudo_agent_dict = {}
        for line in valid_tag:
            parts = line.split(":", 1)
            if len(parts) == 2:
                key, value = parts
                pseudo_agent_dict[key] = value.strip()

        return pseudo_agent_dict

    try:
        agent_judge_result = extract_pseudo_agent_variables(
            agent_judge_conversation
        )
    except Exception as e:
        logger.error(e)
        agent_judge_result = {"PSEUDO_AGENT": "FALSE"}
    logger.debug(f"[agent_judge_result]: {agent_judge_result}")
    return agent_judge_result


def chat(model_series: str = "openai", flag_continue: bool = True, flag_agent: bool = False):
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
        logger.trace(
            "\n"
            + f"[run_agent.msg]:\n{msg}"
            + "\n"
            + f"[run_agent.agent_judge_result]:\n{agent_judge_result}"
        )

        func_file_list = list(
            filter(
                bool,
                [
                    i if (i != "__init__.py" and i != "__pycache__") else ""
                    for i in os.listdir(
                        os.path.join(
                            os.path.dirname(os.path.realpath(__file__)),
                            "pseudo_agent",
                        )
                    )
                ],
            )
        )

        target_file_name = ""
        for func_file in func_file_list:
            with open(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "pseudo_agent",
                    func_file,
                ),
                "r",
                encoding="utf-8",
            ) as f:
                code = f.read()
                if agent_judge_result["PSEUDO_AGENT.ACTION.NAME"] in code:
                    target_file_name = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        "pseudo_agent",
                        func_file,
                    )
                    break

        logger.debug(f"[target_file_name]: {target_file_name}")

        import importlib
        import json

        module_name = target_file_name.replace(".py", "")
        spec = importlib.util.spec_from_file_location(
            module_name, target_file_name
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        logger.success("[Agent] dynamical load called file")

        action_name = agent_judge_result["PSEUDO_AGENT.ACTION.NAME"]
        params = json.loads(agent_judge_result["PSEUDO_AGENT.ACTION.PARA"])

        logger.debug(f"[action_name]: {action_name}")
        logger.debug(f"[params]: {params}")
        logger.debug(f"[type(params)]: {type(params)}")

        try:
            function_to_call = getattr(module, action_name)

            if callable(function_to_call):
                for k, v in params.items():
                    logger.trace(f"[params.{k}]: {v}")
                result = function_to_call(**params)
                logger.info(result)
            else:
                logger.error(
                    f"Error: {action_name} is not a callable function."
                )
        except AttributeError as e:
            logger.error(f"Error: Function {action_name} not found in module.")
        except Exception as e:
            logger.error(f"An error occurred while running the function: {e}")

        try:
            msg = (
                json.dumps(
                    {
                        "AGENT.ACTION.NAME": agent_judge_result[
                            "PSEUDO_AGENT.ACTION.NAME"
                        ],
                        "AGENT.ACTION.PARA": agent_judge_result[
                            "PSEUDO_AGENT.ACTION.PARA"
                        ],
                        "AGENT.EXEC.RESULT": result,
                    },
                    indent=2,
                    ensure_ascii=False,
                    sort_keys=False,
                )
                + ("-" * 30 + "\n" + "上述为执行函数调用的结果，请根据结果回答如下的输入")
                + ("-" * 30 + "\n" + msg)
            )
        except Exception as e:
            logger.error(f"An error occurred while modify msg: {e}")

        return msg

    if flag_agent == True:
        agent_judge_result = agent_judge(msg, available_models, model_series)
    if flag_agent == True and agent_judge_result.get(
        "PSEUDO_AGENT", False
    ) in ["TRUE", True]:
        msg = agent_run(msg, agent_judge_result)
        logger.trace(f"[modified_msg]:\n{msg}")
    conversation = ask(msg, available_models, model_series=model_series, no_history=not flag_continue)

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

            time.sleep(0.05)
            logger.info("[Interaction] 请输入追问")
            append_question = input()
            append_question_normalized = (
                append_question.replace("\n", "")
                .replace(" ", "")
                .replace(" ", "")
            )
            if (
                append_question_normalized != "END"
                and append_question_normalized != ""
            ):
                msg = append_question
                if flag_agent == True:
                    agent_judge_result = agent_judge(
                        msg, available_models, model_series
                    )
                if flag_agent == True and agent_judge_result.get(
                    "PSEUDO_AGENT", False
                ) in ["TRUE", True]:
                    msg = agent_run(msg, agent_judge_result)
                    logger.trace(f"[modified_msg]:{msg}")
                conversation = ask(
                    msg,
                    available_models,
                    model_series=model_series,
                )
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


def draw(model_series: str = "openai"):
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
    logger.critical("THIS PROGRAM NOT INTENT TO RUN SUBMODULE".upper())
    exit(0)


if __name__ == "__main__":
    main()
