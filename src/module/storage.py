import os
import platform

from .log import logger

PROJECT_NAME = "LLMUC"
PROJECT_FOLDER = "." + PROJECT_NAME.lower()


def get_user_folder():
    """
    Get the user directory based on the operating system.
    """
    if platform.system() == "Windows":
        path_str = os.environ.get("USERPROFILE", "")
    else:
        path_str = os.environ.get("HOME", "")
    return os.path.abspath(path_str)


def init():
    file_list = [
        ("question.txt", "Hello World!"),
        ("answer.txt", "Hello! How can I assist you today?"),
    ]
    folder_list = ["logs", "audios", "terminal"]

    for folder in folder_list:
        if not os.path.exists(
            os.path.join(get_user_folder(), PROJECT_FOLDER, folder)
        ):
            os.makedirs(
                os.path.join(get_user_folder(), PROJECT_FOLDER, folder)
            )

    for file_name, default_content in file_list:
        try:
            with open(
                os.path.join(
                    get_user_folder(), PROJECT_FOLDER, "terminal", file_name
                ),
                "r",
                encoding="utf-8",
            ) as file:
                file.read()
        except FileNotFoundError:
            logger.error(f"{file_name} not found. Creating a new file.")
            with open(
                os.path.join(
                    get_user_folder(), PROJECT_FOLDER, "terminal", file_name
                ),
                "w",
                encoding="utf-8",
            ) as file:
                file.write(default_content)
