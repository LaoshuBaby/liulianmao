import tkinter as tk
from tkinter import ttk
import pyperclip

# 初始化应用程序窗口
root = tk.Tk()
root.title("翻译器")

# 定义变量
lang_var = tk.StringVar()
add_keywords_var = tk.BooleanVar()
add_extra_command_var = tk.BooleanVar()

# 目标语言选项
lang_label = ttk.Label(root, text="选择目标语言:")
lang_label.pack()

lang_options = ["en", "zh", "ja"]
lang_menu = ttk.Combobox(root, textvariable=lang_var, values=lang_options)
lang_menu.pack()

# 是否追加关键词
add_keywords_check = ttk.Checkbutton(root, text="追加关键词", variable=add_keywords_var)
add_keywords_check.pack()

# 关键词输入框
keywords_label = ttk.Label(root, text="输入关键词翻译(格式: 原文=译文):")
keywords_label.pack()

keywords_entry = tk.Text(root, height=5, width=50)
keywords_entry.pack()

# 是否追加额外指令
add_extra_command_check = ttk.Checkbutton(root, text="追加额外指令", variable=add_extra_command_var)
add_extra_command_check.pack()

# 文本框
text_box = tk.Text(root, height=10, width=50)
text_box.pack()

# 复制到剪贴板的功能
def copy_to_clipboard():
    command = generate_command()
    pyperclip.copy(command)

# 生成命令
def generate_command():
    command = {
        "task": "translator",
        "content": {
            "lang": lang_var.get(),
            "text": "今後も継続となります。"
        }
    }

    if lang_var.get() in ["zh", "ja"]:
        command["content"]["command"] = "当翻译到zh或者ja的时候，不要用拉丁转写的拼音或注音等来返回结果"

    if add_keywords_var.get():
        keywords_text = keywords_entry.get("1.0", tk.END).strip()
        keyword_translation = {}
        for line in keywords_text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                keyword_translation[key.strip()] = value.strip()
        command["keyword_translation"] = keyword_translation

    if add_extra_command_var.get():
        command["extra"] = {
            "command": [
                "请你根据翻译文本，不联网找出几篇可能相关的文献",
                "解释这个句子中各部分的语法构成"
            ]
        }

    return str(command)

# 生成按钮
generate_button = ttk.Button(root, text="生成并复制到剪贴板", command=copy_to_clipboard)
generate_button.pack()

# 运行应用程序
root.mainloop()