from openai_utils import show
from log import logger
import json


def chat():
    try:
        with open("question.txt", "r") as file:
            msg = file.read()
    except FileNotFoundError:
        print("File not found. Creating a new file.")
        with open("question.txt", "w") as file:
            file.write("Enter your question here.")
        return

    response = show(msg)
    # print(response)


chat()