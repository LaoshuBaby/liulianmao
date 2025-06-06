import os
import platform

PROJECT_NAME = "LIULIANMAO"
PROJECT_FOLDER = "." + PROJECT_NAME.lower()

# default series will be set to compatiable to avoid openai center prospective.
default_config_json = {
    "model_type": {
        "compatiable":"DeepSeek-R1-0528",
        "compatiable.complication":"DeepSeek-R1-0528",
        "compatiable.vision":"DeepSeek-R1-0528",
        "compatiable.reasoning":"DeepSeek-R1-0528",
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

series_list=[
    "openai",
    "deepseek",
    "anthropic"
    "meta",
    "zhipu",
    "xai",
    "mistral"
]

provider_list=series_list+["github"
                           "cloudflare",
                           "one-api(selfhost)",
                           "litellm(selfhost)"]

def get_endpoint():
    pass

def get_endpoint_profile():
    pass

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
