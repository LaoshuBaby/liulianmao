import argparse
import os
import sys
import time
from typing import List

from const import LIULIANMAO_VERSION
from module.log import logger


@logger.catch(level="CRITICAL")
def init_env():
    """
    Initialize the execution environment by setting system paths.

    This function checks whether the script is running from a PyInstaller
    bundle or a standard Python environment. It adjusts the system path
    accordingly to ensure that all necessary resources and modules are
    accessible.
    """
    if getattr(sys, "frozen", False):
        # Running in a PyInstaller bundle
        bundled_dir = sys._MEIPASS
    else:
        # Running in a normal Python environment
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bundled_dir = current_dir

    parent_dir = os.path.dirname(bundled_dir)

    try:
        logger.debug(f'[ENV] "__file__" = {__file__}')
        logger.debug(f'[ENV] "bundled_dir" = {bundled_dir}')
        logger.debug(f'[ENV] "parent_dir" = {parent_dir}')
        logger.debug(f'[ENV] "os.getcwd()" = {os.getcwd()}')
        logger.debug(
            f'[ENV] "os.listdir(bundled_dir)" = {os.listdir(bundled_dir)}'
        )
        logger.trace(f'[ENV] "time.time()" = {time.time()}')
    except Exception as e:
        print(
            __file__,
            "\n",
            bundled_dir,
            "\n",
            parent_dir,
            "\n",
            os.getcwd(),
            "\n",
            os.listdir(bundled_dir),
        )

    if parent_dir not in sys.path:
        sys.path.append(parent_dir)


@logger.catch(level="CRITICAL")
def main(
    recipe: List[str],
    actions: List[str],
    f_a: bool,
    f_v: bool,
    f_c: bool,
    **kwargs,
):
    """Execute the operations specified in the recipe list.

    根据提供的recipe列表和actions列表执行一系列操作。

    Args:
        recipe: A list of strings representing the operations to be processed.默认为["init", "chat"]。
        actions: A list of strings representing additional actions to be taken.
        f_c: A boolean feature to enable continuous dialogue.
        f_a: A boolean feature to enable the use of an agent.
    """
    logger.trace(f"[f_a]: {f_a}")
    logger.trace(f"[f_v]: {f_v}")
    logger.trace(f"[f_c]: {f_c}")

    if "question" in actions:
        from module.const import PROJECT_FOLDER, get_user_folder

        logger.info("[action]: question")

        question_file_path = os.path.join(
            str(get_user_folder()), PROJECT_FOLDER, "terminal", "question.txt"
        )
        os.startfile(question_file_path)
        sys.exit(0)

    if "answer" in actions:
        from module.const import PROJECT_FOLDER, get_user_folder

        logger.info("[action]: answer")

        answer_file_path = os.path.join(
            str(get_user_folder()), PROJECT_FOLDER, "terminal", "answer.txt"
        )
        os.startfile(answer_file_path)
        sys.exit(0)

    if "config" in actions:
        from module.const import PROJECT_FOLDER, get_user_folder
        from module.runtime import is_serverlsss

        logger.info("[action]: config")

        config_file_path = os.path.join(
            str(get_user_folder()), PROJECT_FOLDER, "assets", "config.json"
        )
        if is_serverlsss():
            logger.error("SERVERLESS ENVIRONMENT'S CONFIG FILE IS MEANINGLESS")
        else:
            os.startfile(config_file_path)
        sys.exit(0)

    if "sync" in actions:
        from module.sync import sync_profiles

        logger.info("[action]: sync")

        sync_profiles()
        sys.exit(0)

    import importlib.util

    FEATURE = {"core": True, "langchain": False}

    spec = importlib.util.find_spec(".core", package="client")
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)

    spec_openai = importlib.util.find_spec(".api.openai", package="client")
    api_openai = importlib.util.module_from_spec(spec_openai)
    spec_openai.loader.exec_module(api_openai)

    recipe_operation_list = {
        "default": core.chat,
        "models": api_openai.openai_models,
        "ask": core.ask,
        "chat": core.chat,
        "talk": core.talk,
        "draw": core.draw,
    }

    logger.debug(f"[Recipe]: {recipe}")
    for operation_name in recipe:
        operation = recipe_operation_list.get(operation_name)
        if operation:
            if operation_name == "ask":
                operation("this is a question")
            if operation_name == "chat" or operation_name == "default":
                operation(
                    model_series=kwargs.get("series", "").lower(),
                    feature_continue=f_c,
                    feature_agent=f_a,
                )
            else:
                operation()
        else:
            print(f"Operation {operation_name} is not defined.")


if __name__ == "__main__":
    init_env()
    logger.success(f"=== LIULIANMAO:{LIULIANMAO_VERSION} ===")
    default_recipe = ["default"]
    parser = argparse.ArgumentParser(description="Process some operations.")
    # argument category: manual
    # -h/-help/--help

    # argument category: io
    parser.add_argument(
        "-q",  # fastkey[Q]
        "-m",  # fastkey[M]
        "-question",  # 有歧义
        "--question",  # 有歧义
        "-msg",  # 无歧义，建议后续分拆有参数的question重定向到msg
        "--msg",  # 无歧义，同上
        nargs="?",
        const=True,
        default=False,
        help=(
            "Open the question.txt file with default program or pass a specific message,"
            + "if this argument has value, it should only work if input argument is not specified."
        ),
    )
    # argument category: io
    parser.add_argument(
        "-a",  # fastkey[A]
        "-answer",
        "--answer",
        action="store_true",
        help="Open the answer.txt file with default program",
    )
    # argument category: io
    parser.add_argument(
        "-i",  # fastkey[I]
        "-input",
        "--input",
        help="Specify input file, read this file as question, not default question.txt",
    )
    # argument category: io
    parser.add_argument(
        "-o",  # fastkey[O]
        "-output",
        "--output",
        help="Specify output file, write answer to this file, not default answer.txt",
    )

    # argument category: show content
    parser.add_argument(
        "-c", # fastkey[C]
        "-config",
        "--config",
        action="store_true",
        help="Open the config.txt file with default program",
    )
    # argument category: show content
    parser.add_argument(
        "-l", # fastkey[L]
        "-log",
        "--log",
        action="store_true",
        help="Open Log folder",
    )
    # argument category: show content
    parser.add_argument(
        "-k", # fastkey[K]
        "-key",
        "--key",
        action="store_true",
        help="Open OPENAI_API_KEY and OPENAI_BASE_URL files with default program",
    )
    # argument category: set content (WIP)
    # user can set config/log/key in pure cli command
    # argument category: set content (WIP)
    parser.add_argument(
        "-sc",
        "--sync",
        action="store_true",
        help="Sync profiles",
    )

    # argument category: response control
    parser.add_argument(
        "-s", # fastkey[S]
        "-series",
        "--series",
        type=str,
        default="openai",
        help="A string representing a series",
    )
    # argument category: response control
    parser.add_argument(
        # 没给fastkey，主要是想不出model怎么简写，以及m到底是给msg好还是给model好
        "-model",
        "-models",
        "--model",
        "--models",
        type=str,
        default="gpt-5.2",
        help="select a special model",
    )

    # argument category: agent and multimodel 
    parser.add_argument(
        "-r", # fastkey[R]
        "-recipe",
        "--recipe",
        nargs="*",
        default=default_recipe,
        help="List of operations to process",
    )
    # argument category: agent and multimodal 
    parser.add_argument(
        "-sm", # fastkey[SM]
        "-search_models",
        "--search_models",
        type=str,
        default="gpt",
        help="select a keyword for search models in a /model api call.",
    )
    # argument category: agent and multimodal  (ability)
    parser.add_argument(
        "-fa", # fastkey[FA]
        "-f_a",
        "--f_a",
        action="store_true",
        default=False,
        help="Enable the use of an agent",
    )
    # argument category: agent and multimodal  (ability)
    parser.add_argument(
        "-fv", # fastkey[FV]
        "-f_v",
        "--f_v",
        action="store_true",
        default=True,
        help="Enable the use of using image",
    )
    # argument category: agent and multimodal  (ability)
    parser.add_argument(
        "-fc", # fastkey[FC]
        "-f_c",
        "--f_c",
        # action="store",
        nargs="?",
        type=int,
        const=True,
        default=True,
        help="""Enable continuous dialogue with a specified integer value, or True by default.
        默认值为 True，但如果用户提供了具体的轮数，这个数字将被使用""",
    )

    args = parser.parse_args()
    logger.trace(args)

    logger.trace(args)

    actions = []
    if args.question is True:
        actions.append("question")
    if args.answer is True:
        actions.append("answer")
    if args.config is True:
        actions.append("config")
    if args.sync is True:
        actions.append("sync")

    logger.trace(actions)

    main(
        recipe=args.recipe,
        actions=actions,
        f_a=args.f_a,
        f_v=args.f_v,
        f_c=args.f_c,
        series=args.series,
        s_m=args.search_models,
    )
