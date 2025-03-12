import tkinter as tk
from tkinter import ttk
import pyperclip
import json

# 初始化应用程序窗口
root = tk.Tk()
root.title("翻译器")
root.geometry("900x500")  # 调整窗口高度

# 定义变量
lang_var = tk.StringVar()
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

# 添加选项框（水平排列）
options_frame = ttk.Frame(root)
options_frame.pack(pady=5, fill=tk.X)

# 目标语言选项
lang_label = ttk.Label(options_frame, text="选择目标语言:")
lang_label.grid(row=0, column=0, padx=5)
lang_options = ["en", "zh", "ja"]
lang_menu = ttk.Combobox(options_frame, textvariable=lang_var, values=lang_options)
lang_menu.grid(row=0, column=1, padx=5)

# 是否追加关键词
add_keywords_check = ttk.Checkbutton(options_frame, text="追加关键词", variable=add_keywords_var)
add_keywords_check.grid(row=0, column=2, padx=5)

# 关键词输入框
keywords_entry = tk.Text(options_frame, height=5, width=20)
keywords_entry.grid(row=0, column=3, padx=5)

# 是否追加额外指令
add_extra_command_check = ttk.Checkbutton(options_frame, text="追加额外指令", variable=add_extra_command_var)
add_extra_command_check.grid(row=0, column=4, padx=5)

# 额外指令输入框
extra_commands_entry = tk.Text(options_frame, height=5, width=20)
extra_commands_entry.grid(row=0, column=5, padx=5)

# 生成命令
def generate_command():
    text = text_box.get("1.0", tk.END).strip()
    command = {
        "task": "translator",
        "description": [
            "从content中提取text中的文字，并翻译为content中lang中的语言。",
            "除非有特殊情况，否则输出为一个json，仅包含text一个key，value为译文。",
            "如果在extra中存在额外指令（command），请遵守。在返回的json中增加一个名为extra的key，其value为翻译外的结果。这通常是需要理解所翻译内容并按照指令执行操作",     
            "原文中如果有换行，输出的时候仍展示为换行。",
            "原文中为\\n的，输出的时候展示为\\n",
            "不要试图给我一段代码指导我如何运行代码获得结果，我需要的是一段json，请直接输出你认为应该根据这里的提示返回的json文本内容",
            "输出的json无需使用```json等markdown符号包装",
            "如果keyword中有结果，那么这代表着这些词应该按照这样的方式翻译",
            "翻译的json仅输出一次，在输出完整个完整的json后，你将结束translator的工作模式。"
        ],
        "content": {
            "lang": lang_var.get(),
            "text": text
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

# 复制到剪贴板的功能
def copy_to_clipboard():
    command = generate_command()
    pyperclip.copy(command)

# 生成按钮
generate_button = tk.Button(options_frame, text="生成并复制", command=copy_to_clipboard, bg='red', font=("Arial", 12))
generate_button.grid(row=0, column=6, padx=5)

# 运行应用程序
root.mainloop()