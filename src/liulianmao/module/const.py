import os
import platform

PROJECT_NAME = "LIULIANMAO"
PROJECT_FOLDER = "." + PROJECT_NAME.lower()

default_config_json = {
    "model_type": {
        "openai": "gpt-4-turbo-preview",
        "openai.normal": "gpt-4-turbo-preview",
        "openai.vision": "gpt-4v",
        "zhipu": "glm-4-plus",
        "zhipu.normal": "glm-4-plus",
        "zhipu.vision": "glm-4v-plus",
        "deepseek": "deepseek-chat",
    },
    "system_message": {"content": "You are a helpful assistant."},
    "settings": {"temperature": 0.5},
}

all_available_languages = [
    "abq",
    "ady",
    "af",
    "ang",
    "ar",
    "as",
    "ava",
    "az",
    "be",
    "bg",
    "bh",
    "bho",
    "bn",
    "bs",
    "ch_sim",
    "ch_tra",
    "che",
    "cs",
    "cy",
    "da",
    "dar",
    "de",
    "en",
    "es",
    "et",
    "fa",
    "fr",
    "ga",
    "gom",
    "hi",
    "hr",
    "hu",
    "id",
    "inh",
    "is",
    "it",
    "ja",
    "kbd",
    "kn",
    "ko",
    "ku",
    "la",
    "lbe",
    "lez",
    "lt",
    "lv",
    "mah",
    "mai",
    "mi",
    "mn",
    "mr",
    "ms",
    "mt",
    "ne",
    "new",
    "nl",
    "no",
    "oc",
    "pi",
    "pl",
    "pt",
    "ro",
    "ru",
    "rs_cyrillic",
    "rs_latin",
    "sck",
    "sk",
    "sl",
    "sq",
    "sv",
    "sw",
    "ta",
    "tab",
    "te",
    "th",
    "tjk",
    "tl",
    "tr",
    "ug",
    "uk",
    "ur",
    "uz",
    "vi",
]


def get_user_folder():
    """
    Get the user directory based on the operating system.
    """
    if platform.system() == "Windows":
        path_str = os.environ.get("USERPROFILE", "")
    else:
        path_str = os.environ.get("HOME", "")
    return os.path.abspath(path_str)
