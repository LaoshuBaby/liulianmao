import subprocess
import os

import tkinter as tk
from tkinter import ttk
import pyperclip
import json

# 定义翻译字典
TRANSLATIONS = {
    "description-task": {
        "zh": "从content中提取text中的文字，并翻译为content中lang中的语言。",
        "en": "Extract the text in content and translate it into the language specified in lang in content. ",
        "ja": "「content」の「text」からテキストを抽出し、「lang」で指定された言語に翻訳します。",
    },
    "description-json": {
        "zh": "除非有特殊情况，否则输出为一个json，仅包含text一个key，value为译文。",
        "en": "Unless there are special circumstances, output as a json with only one key, text, and the value as the translation.",
        "ja": "特別な状況がない限り、「text」というキーのみを含むjsonとして出力し、値は翻訳です。",
    },
    "description-extra": {
        "zh": "如果在extra中存在额外指令（command），请遵守。在返回的json中增加一个名为extra的key，其value为翻译外的结果。这通常是需要理解所翻译内容并按照指令执行操作",
        "en": "",
        "ja": "",
    },
    "description-keepcrlf": {
        "zh": "原文中如果有换行，输出的时候仍展示为换行。",
        "en": "Additionally, if there are line breaks in the original text, they should be displayed as line breaks in the output.",
        "ja": "原文に改行がある場合、出力でも改行を表示します。",
    },
    "description-escaped-crlf": {
        "zh": "原文中为\\n的，输出的时候展示为\\n",
        "en": "If the original text contains \n, it should be displayed as \n in the output.",
        "ja": "原文に「\n」が含まれている場合、出力でも「\n」として表示します。",
    },
    "description-nocodeinstruct": {
        "zh": "不要试图给我一段代码指导我如何运行代码获得结果，我需要的是一段json，请直接输出你认为应该根据这里的提示返回的json文本内容",
        "en": "Do not attempt to give me a piece of code to guide me on how to run the code to get the result; I need a json output that you think should be returned based on these instructions.",
        "ja": "ソースコードを実行する方法を教えるためのコードを提供しようとしないで ください。私が必要なのは、ここでの指示に基づいて返されるべきjsonテキストコンテンツです。",
    },
    "description-no-markdown": {
        "zh": "输出的json无需使用```json等markdown符号包装",
        "en": "",
        "ja": "",
    },
    "description-keyword": {
        "zh": "如果keyword中有结果，那么这代表着这些词应该按照这样的方式翻译",
        "en": "",
        "ja": "",
    },
    "description-once": {
        "zh": "翻译的json仅输出一次，在输出完整个完整的json后，你将结束translator的工作模式。",
        "en": "",
        "ja": "",
    },
    "command-cjk-no-romanization": {
        "zh": "当翻译到zh或者ja的时候，不要用拉丁转写的拼音或注音等来返回结果",
        "en": "",
        "ja": "",
    },
}


# 默认的prompt语言
DEFAULT_PROMPT_LANG = "zh"


# 文本查找函数
def get_translation(key, lang):
    return TRANSLATIONS.get(key, {}).get(
        lang, TRANSLATIONS[key][DEFAULT_PROMPT_LANG]
    )


# 复制到剪贴板的功能
def action_copy_to_clipboard():
    command = generate_command()
    pyperclip.copy(command)


# 生成命令
def generate_command():
    text = text_box.get("1.0", tk.END).strip()
    prompt_lang = prompt_lang_var.get()
    command = {
        "task": "translator",
        "description": [
            get_translation("description-task", prompt_lang),
            get_translation("description-json", prompt_lang),
            get_translation("description-extra", prompt_lang),
            get_translation("description-keepcrlf", prompt_lang),
            get_translation("description-escaped-crlf", prompt_lang),
            get_translation("description-nocodeinstruct", prompt_lang),
            get_translation("description-no-markdown", prompt_lang),
            get_translation("description-keyword", prompt_lang),
            get_translation("description-once", prompt_lang),
        ],
        "content": {"lang": lang_var.get(), "text": text},
    }

    if lang_var.get() in ["zh", "ja"]:
        command["content"]["command"] = get_translation(
            "command-cjk-no-romanization", prompt_lang
        )

    if add_keywords_var.get():
        keywords_text = keywords_entry.get("1.0", tk.END).strip()
        keyword_translation = {}
        for line in keywords_text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                keyword_translation[key.strip()] = value.strip()
        command["keyword_translation"] = keyword_translation

    if add_extra_command_var.get():
        extra_commands_text = extra_commands_entry.get("1.0", tk.END).strip()
        extra_commands = extra_commands_text.splitlines()
        command["extra"] = {"command": extra_commands}

    formatted_command = json.dumps(command, indent=2, ensure_ascii=False)
    # 在输出框中显示生成的 JSON
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, formatted_command)
    return formatted_command


def action_open_question_file():
    try:
        home_directory = os.path.expanduser("~")
        os.chdir(home_directory)

        if os.name == "posix" or os.name == "mac":
            os.system("python3 -m liulianmao --question")
        elif os.name == "nt":
            os.system("python -m liulianmao --question")
    except Exception as e:
        print(f"Error opening question file: {e}")


def action_run_liulianmao():
    try:
        home_directory = os.path.expanduser("~")
        os.chdir(home_directory)

        if os.name == "posix" or os.name == "mac":
            os.system("gnome-terminal -- python3 -m liulianmao")
        elif os.name == "nt":
            os.system("start cmd /k python -m liulianmao")
    except Exception as e:
        print(f"Error running liulianmao: {e}")


# Initialize the application window
root = tk.Tk()
root.title("翻译器")
root.geometry("900x500")

# Define variables
lang_var = tk.StringVar()
prompt_lang_var = tk.StringVar(value=DEFAULT_PROMPT_LANG)
add_keywords_var = tk.BooleanVar()
add_extra_command_var = tk.BooleanVar()

# Main frame
frame = ttk.Frame(root)
frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

# Input text box
text_box = tk.Text(frame, height=15, width=50)
text_box.pack(side=tk.LEFT, padx=3, pady=3, fill=tk.BOTH, expand=True)

# Output JSON display box
output_box = tk.Text(frame, height=15, width=50, state="normal")
output_box.pack(side=tk.RIGHT, padx=3, pady=3, fill=tk.BOTH, expand=True)

# Separator
separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill=tk.X, pady=5)

# Options frame
options_frame = ttk.Frame(root)
options_frame.pack(pady=5, fill=tk.X)

# Language and checkboxes column
lang_frame = ttk.Frame(options_frame)
lang_frame.grid(row=0, column=0, padx=5, sticky=tk.N)

# Target language selection
lang_label = ttk.Label(lang_frame, text="选择target语言:")
lang_label.pack(anchor=tk.W, pady=2)
lang_options = ["en", "zh", "ja"]
lang_menu = ttk.Combobox(
    lang_frame, textvariable=lang_var, values=lang_options
)
lang_menu.pack(anchor=tk.W, pady=2)

# Prompt language selection
prompt_lang_label = ttk.Label(lang_frame, text="选择prompt语言:")
prompt_lang_label.pack(anchor=tk.W, pady=2)
prompt_lang_menu = ttk.Combobox(
    lang_frame, textvariable=prompt_lang_var, values=lang_options
)
prompt_lang_menu.pack(anchor=tk.W, pady=2)

# Add keywords checkbox
add_keywords_check = ttk.Checkbutton(
    lang_frame, text="追加关键词", variable=add_keywords_var
)
add_keywords_check.pack(anchor=tk.W, pady=2)

# Add extra command checkbox
add_extra_command_check = ttk.Checkbutton(
    lang_frame, text="追加额外指令", variable=add_extra_command_var
)
add_extra_command_check.pack(anchor=tk.W, pady=2)

# Keywords input column
keywords_frame = ttk.Frame(options_frame)
keywords_frame.grid(row=0, column=1, padx=5, sticky="ns")
keywords_label = ttk.Label(keywords_frame, text="关键词 (每行一组)")
keywords_label.pack(anchor=tk.W)
keywords_entry = tk.Text(keywords_frame, height=5, width=20)
keywords_entry.pack(fill=tk.BOTH, expand=True)

# Extra commands input column
extra_commands_frame = ttk.Frame(options_frame)
extra_commands_frame.grid(row=0, column=2, padx=5, sticky="ns")
extra_commands_label = ttk.Label(
    extra_commands_frame, text="额外指令 (每行一条)"
)
extra_commands_label.pack(anchor=tk.W)
extra_commands_entry = tk.Text(extra_commands_frame, height=5, width=20)
extra_commands_entry.pack(fill=tk.BOTH, expand=True)

# Button column
button_frame = ttk.Frame(options_frame)
button_frame.grid(row=0, column=3, padx=5, sticky=tk.N)

button_generate_json = tk.Button(
    button_frame,
    text="生成并复制",
    command=action_copy_to_clipboard,
    bg="yellow",
    font=("Arial", 12),
    width=14,
)
button_generate_json.pack(anchor=tk.W, pady=2)

button_open_question = tk.Button(
    button_frame,
    text="打开question文件",
    command=action_open_question_file,
    bg="green",
    font=("Arial", 12),
    width=14,
)
button_open_question.pack(anchor=tk.W, pady=2)

button_run_liulianmao = tk.Button(
    button_frame,
    text="运行liulianmao",
    command=action_run_liulianmao,
    bg="red",
    font=("Arial", 12),
    width=14,
)
button_run_liulianmao.pack(anchor=tk.W, pady=2)

# Ensure each frame or widget in the columns can expand using grid
lang_frame.grid(row=0, column=0, padx=5, sticky="nsew")
keywords_frame.grid(row=0, column=1, padx=5, sticky="nsew")
extra_commands_frame.grid(row=0, column=2, padx=5, sticky="nsew")
button_frame.grid(row=0, column=3, padx=5, sticky="nsew")

# Adjust the weight for each column to control their relative width
options_frame.columnconfigure(0, weight=1)  # Language and checkboxes
options_frame.columnconfigure(1, weight=4)  # Keywords input
options_frame.columnconfigure(2, weight=4)  # Extra commands input
options_frame.columnconfigure(3, weight=2)  # Buttons

# Allow rows to expand vertically
options_frame.rowconfigure(0, weight=1)

# Run the application
root.mainloop()
