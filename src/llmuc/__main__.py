FEATURE={
    "core":True,
    "langchain":False
}

from .client_core import main as core
if FEATURE["langchain"]:
    from .client_langchain import main as langchain

core()
