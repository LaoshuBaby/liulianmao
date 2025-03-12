import tkinter as tk
from tkinter import ttk
import pyperclip
import json

# 定义翻译字典
TRANSLATIONS = {
    "description-task": {
        "zh": "从content中提取text中的文字，并翻译为content中lang中的语言。",
        "en": "",
        "ja": ""
    },
    "description-json": {
        "zh": "除非有特殊情况，否则输出为一个json，仅包含text一个key，value为译文。",
        "en": "",
        "ja": ""
    },
    "description-extra": {
        "zh": "如果在extra中存在额外指令（command），请遵守。在返回的json中增加一个名为extra的key，其value为翻译外的结果。这通常是需要理解所翻译内容并按照指令执行操作",   
        "en": "",
        "ja": ""
    },
    "description-keepcrlf": {
        "zh": "原文中如果有换行，输出的时候仍展示为换行。",
        "en": "",
        "ja": ""
    },
    "description-escaped-crlf": {
        "zh": "原文中为\\n的，输出的时候展示为\\n",
        "en": "",
        "ja": ""
    },
    "description-nocodeinstruct": {
        "zh": "不要试图给我一段代码指导我如何运行代码获得结果，我需要的是一段json，请直接输出你认为应该根据这里的提示返回的json文本内容",
        "en": "",
        "ja": ""
    },
    "description-no-markdown": {
        "zh": "输出的json无需使用```json等markdown符号包装",
        "en": "",
        "ja": ""
    },
    "description-keyword": {
        "zh": "如果keyword中有结果，那么这代表着这些词应该按照这样的方式翻译",
        "en": "",
        "ja": ""
    },
    "description-once": {
        "zh": "翻译的json仅输出一次，在输出完整个完整的json后，你将结束translator的工作模式。",
        "en": "",
        "ja": ""
    },
    "command-zh-ja": {
        "zh": "当翻译到zh或者ja的时候，不要用拉丁转写的拼音或注音等来返回结果",
        "en": "",
        "ja": ""
    }
}

# 默认的prompt语言
DEFAULT_PROMPT_LANG = "zh"

# 文本查找函数
def get_translation(key, lang):
    return TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS[key][DEFAULT_PROMPT_LANG])

# 复制到剪贴板的功能
def copy_to_clipboard():
    command = generate_command()
    pyperclip.copy(command)



# 初始化应用程序窗口
root = tk.Tk()
root.title("翻译器")
root.geometry("900x500")  # 调整窗口高度

# 定义变量
lang_var = tk.StringVar()
prompt_lang_var = tk.StringVar(value=DEFAULT_PROMPT_LANG)  # 新增变量
add_keywords_var = tk.BooleanVar()
add_extra_command_var = tk.BooleanVar()

# 左右两个大框
frame = ttk.Frame(root)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# 输入文本框
text_box = tk.Text(frame, height=15, width=50)  # 调整高度
text_box.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

# 生成的 JSON 显示框
output_box = tk.Text(frame, height=15, width=50, state='normal')  # 调整高度
output_box.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)

# 添加一个分隔线
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill=tk.X, pady=5)

# 添加选项框（垂直排列）
options_frame = ttk.Frame(root)
options_frame.pack(pady=5, fill=tk.X)

# 第一列：语言选择和复选框
lang_frame = ttk.Frame(options_frame)
lang_frame.grid(row=0, column=0, padx=5, sticky=tk.N)

# 目标语言选项
lang_label = ttk.Label(lang_frame, text="选择目标语言:")
lang_label.pack(anchor=tk.W, pady=2)
lang_options = ["en", "zh", "ja"]
lang_menu = ttk.Combobox(lang_frame, textvariable=lang_var, values=lang_options)
lang_menu.pack(anchor=tk.W, pady=2)

# prompt语言选项
prompt_lang_label = ttk.Label(lang_frame, text="选择prompt语言:")
prompt_lang_label.pack(anchor=tk.W, pady=2)
prompt_lang_menu = ttk.Combobox(lang_frame, textvariable=prompt_lang_var, values=lang_options)
prompt_lang_menu.pack(anchor=tk.W, pady=2)

# 是否追加关键词
add_keywords_check = ttk.Checkbutton(lang_frame, text="追加关键词", variable=add_keywords_var)
add_keywords_check.pack(anchor=tk.W, pady=2)

# 是否追加额外指令
add_extra_command_check = ttk.Checkbutton(lang_frame, text="追加额外指令", variable=add_extra_command_var)
add_extra_command_check.pack(anchor=tk.W, pady=2)

# 第二列：关键词输入框
keywords_frame = ttk.Frame(options_frame)
keywords_frame.grid(row=0, column=1, padx=5)

keywords_entry = tk.Text(keywords_frame, height=5, width=20)
keywords_entry.pack()

# 第三列：额外指令输入框
extra_commands_frame = ttk.Frame(options_frame)
extra_commands_frame.grid(row=0, column=2, padx=5)

extra_commands_entry = tk.Text(extra_commands_frame, height=5, width=20)
extra_commands_entry.pack()

# 第四列：生成按钮
button_frame = ttk.Frame(options_frame)
button_frame.grid(row=0, column=3, padx=5)

generate_button = tk.Button(button_frame, text="生成并复制", command=copy_to_clipboard, bg='red', font=("Arial", 12))
generate_button.pack()


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
            get_translation("description-once", prompt_lang)
        ],
        "content": {
            "lang": lang_var.get(),
            "text": text
        }
    }
    
    if lang_var.get() in ["zh", "ja"]:
        command["content"]["command"] = get_translation("command-zh-ja", prompt_lang)
    
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
        command["extra"] = {
            "command": extra_commands
        }

    formatted_command = json.dumps(command, indent=2, ensure_ascii=False)
    # 在输出框中显示生成的 JSON
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, formatted_command)
    return formatted_command


# 运行应用程序
root.mainloop()