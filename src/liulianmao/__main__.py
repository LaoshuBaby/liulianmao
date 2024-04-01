import os
import sys


if getattr(sys, 'frozen', False):
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

# 动态加载 client_core 模块
spec = importlib.util.find_spec('.client_core', package='liulianmao')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


# FEATURE = {
#     "core": True,
#     "langchain": False
# }

# if FEATURE["langchain"]:
#     spec = importlib.util.find_spec('.client_langchain', package='liulianmao')
#     langchain = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(langchain)

FEATURE = {
    "core": True,
    "langchain": False
}

if FEATURE["langchain"]:
    from liulianmao.client_langchain import main as langchain

core.main()

