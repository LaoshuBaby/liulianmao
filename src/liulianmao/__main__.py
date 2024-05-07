import argparse
import os
import sys
from typing import List

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
def main(recipe: List[str], actions: List[str], **kwargs):
    """Execute the operations specified in the recipe list.

    根据提供的recipe列表和actions列表执行一系列操作。

    Args:
        recipe: A list of strings representing the operations to be processed.默认为["init", "chat"]。
        actions: A list of strings representing additional actions to be taken.
    """
    if "question" in actions:
        from module.const import PROJECT_FOLDER, get_user_folder

        question_file_path = os.path.join(
            str(get_user_folder()), PROJECT_FOLDER, "terminal", "question.txt"
        )
        os.startfile(question_file_path)
        sys.exit(0)

    if "answer" in actions:
        from module.const import PROJECT_FOLDER, get_user_folder

        answer_file_path = os.path.join(
            str(get_user_folder()), PROJECT_FOLDER, "terminal", "answer.txt"
        )
        os.startfile(answer_file_path)
        sys.exit(0)

    if "config" in actions:
        from module.const import PROJECT_FOLDER, get_user_folder

        config_file_path = os.path.join(
            str(get_user_folder()), PROJECT_FOLDER, "assets", "config.json"
        )
        os.startfile(config_file_path)
        sys.exit(0)

    import importlib.util

    FEATURE = {"core": True, "langchain": False}

    spec = importlib.util.find_spec(".core", package="client")
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)

    spec_openai = importlib.util.find_spec(".api.openai", package="client")
    api_openai = importlib.util.module_from_spec(spec_openai)
    spec_openai.loader.exec_module(api_openai)

    if FEATURE["langchain"]:
        # spec = importlib.util.find_spec('.langchain', package='client')
        # langchain = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(langchain)
        from client.langchain import main as langchain

    operations = {
        "default": core.chat,
        "models": api_openai.openai_models,
        "ask": core.ask,
        "chat": core.chat,
        "talk": core.talk,
        "draw": core.draw,
    }

    logger.debug(f"[Recipe]: {recipe}")
    for operation_name in recipe:
        operation = operations.get(operation_name)
        if operation:
            if operation_name == "ask":
                operation("this is a question")
            if operation_name == "chat" or operation_name == "default":
                operation(model_series=kwargs.get("series", "").lower())
            else:
                operation()
        else:
            print(f"Operation {operation_name} is not defined.")


if __name__ == "__main__":
    init_env()
    default_recipe = ["default"]
    parser = argparse.ArgumentParser(description="Process some operations.")
    parser.add_argument(
        "-q",
        "-question",
        "--question",
        nargs="?",
        const=True,
        default=False,
        help="Open the question.txt file with default program or pass a specific message",
    )
    parser.add_argument(
        "-a",
        "-answer",
        "--answer",
        action="store_true",
        help="Open the answer.txt file with default program",
    )
    parser.add_argument(
        "-c",
        "-config",
        "--config",
        action="store_true",
        help="Open the config.txt file with default program",
    )
    parser.add_argument(
        "-l",
        "-log",
        "--log",
        action="store_true",
        help="Open Log folder",
    )
    parser.add_argument(
        "-k",
        "-key",
        "--key",
        action="store_true",
        help="Open OPENAI_API_KEY and OPENAI_BASE_URL files with default program",
    )
    parser.add_argument(
        "-i",
        "-input",
        "--input",
        help="Specify input file, read this file as question, not default question.txt",
    )
    parser.add_argument(
        "-o",
        "-output",
        "--output",
        help="Specify output file, write answer to this file, not default answer.txt",
    )
    parser.add_argument(
        "-r",
        "-recipe",
        "--recipe",
        nargs="*",
        default=default_recipe,
        help="List of operations to process",
    )
    parser.add_argument(
        "-s",
        "-series",
        "--series",
        type=str,
        help="A string representing a series",
    )
    args = parser.parse_args()

    actions = []
    if args.question is True:
        actions.append("question")
    if args.answer is True:
        actions.append("answer")
    if args.config is True:
        actions.append("config")

    if args.series != None and args.series != "":
        series = args.series
    else:
        series = "openai"

    main(recipe=args.recipe, actions=actions, series=series)
