import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


from liulianmao.client_core import main as core

FEATURE = {
    "core": True,
    "langchain": False
}

if FEATURE["langchain"]:
    from liulianmao.client_langchain import main as langchain

core()
