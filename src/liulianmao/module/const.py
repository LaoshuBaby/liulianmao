import os
import platform

PROJECT_NAME = "LIULIANMAO"
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
