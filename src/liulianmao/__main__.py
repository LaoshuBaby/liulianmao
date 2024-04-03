import os
import sys

if getattr(sys, "frozen", False):
    # we are running in a |PyInstaller| bundle
    bundled_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bundled_dir = current_dir
parent_dir = os.path.dirname(bundled_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# print(__file__)
# print(bundled_dir)
# print(parent_dir)
# print(os.getcwd())
# print(os.listdir(bundled_dir))

import importlib.util

spec = importlib.util.find_spec(".core", package="client")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


FEATURE = {"core": True, "langchain": False}

if FEATURE["langchain"]:
    # spec = importlib.util.find_spec('.langchain', package='client')
    # langchain = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(langchain)
    from liulianmao.langchain import main as langchain

operations = {
    "init": core.init,
    "chat": core.chat,
}


def main(recipe):
    for operation_name in recipe:
        operation = operations.get(operation_name)
        if operation:
            operation()
        else:
            print(f"Operation {operation_name} is not defined.")


if __name__ == "__main__":
    recipe = ["init", "chat"]
    main(recipe)
