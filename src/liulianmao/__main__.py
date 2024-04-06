import argparse
import os
import sys
from typing import List


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
        from module.log import logger

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


def main(recipe: List[str], actions: List[str]):
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

    if FEATURE["langchain"]:
        # spec = importlib.util.find_spec('.langchain', package='client')
        # langchain = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(langchain)
        from client.langchain import main as langchain

    operations = {
        "chat": core.chat,
        "talk": core.talk,
        "models": core.models,
    }

    for operation_name in recipe:
        operation = operations.get(operation_name)
        if operation:
            operation()
        else:
            print(f"Operation {operation_name} is not defined.")


if __name__ == "__main__":
    init_env()
    default_recipe = ["models"]
    parser = argparse.ArgumentParser(description="Process some operations.")
    parser.add_argument(
        "--question", action="store_true", help="Read the question.txt file"
    )
    parser.add_argument(
        "--config", action="store_true", help="Read the config.txt file"
    )
    parser.add_argument(
        "--recipe",
        nargs="*",
        default=default_recipe,
        help="List of operations to process",
    )
    args = parser.parse_args()

    actions = []
    if args.question:
        actions.append("question")
    if args.config:
        actions.append("config")

    main(recipe=args.recipe, actions=actions)
