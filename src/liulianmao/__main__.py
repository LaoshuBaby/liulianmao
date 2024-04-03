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

    # print(__file__)
    # print(bundled_dir)
    # print(parent_dir)
    # print(os.getcwd())
    # print(os.listdir(bundled_dir))

    if parent_dir not in sys.path:
        sys.path.append(parent_dir)


import importlib.util

spec = importlib.util.find_spec(".core", package="client")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


FEATURE = {"core": True, "langchain": False}

if FEATURE["langchain"]:
    # spec = importlib.util.find_spec('.langchain', package='client')
    # langchain = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(langchain)
    from client.langchain import main as langchain

operations = {
    "init": core.init,
    "chat": core.chat,
}


def main(recipe: List[str], question: bool):
    """Execute the operations specified in the recipe list.

    如果question为真，则打开并打印'question.txt'文件的内容。
    根据提供的recipe列表执行一系列操作。

    Args:
        recipe: A list of strings representing the operations to be processed.
            默认为["init", "chat"]。
        question: A boolean flag that, when True, triggers the reading and printing
            of the 'question.txt' file's content.

    示例：
    - `python your_script.py` 将使用默认的recipe（即["init", "chat"]）。
    - `python your_script.py --recipe init other_operation` 将使用自定义的recipe（即["init", "other_operation"]）。
    - `python your_script.py --question` 将打开并打印`question.txt`文件的内容，并使用默认的recipe。
    - `python your_script.py --question --recipe init other_operation` 将打开并打印`question.txt`文件的内容，并使用自定义的recipe。
    """

    if question:
        with open("question.txt", "r") as file:
            print(file.read())

    for operation_name in recipe:
        operation = operations.get(operation_name)
        if operation:
            operation()
        else:
            print(f"Operation {operation_name} is not defined.")


if __name__ == "__main__":
    default_recipe = ["init", "chat"]
    parser = argparse.ArgumentParser(description="Process some operations.")
    parser.add_argument(
        "--question", action="store_true", help="Read the question.txt file"
    )
    parser.add_argument(
        "--recipe",
        nargs="*",
        default=default_recipe,
        help="List of operations to process",
    )
    args = parser.parse_args()
    main(recipe=args.recipe, question=args.question)
