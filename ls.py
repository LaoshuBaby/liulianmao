import os


def should_ignore(directory, root, ignore_rules):
    """
    根据忽略规则判断目录是否应该被忽略。
    :param directory: 当前目录路径
    :param root: 根目录路径
    :param ignore_rules: 忽略规则列表，每个规则是一个二元组，包含目录名和是否只在根目录下忽略
    :return: 如果应该忽略，返回True；否则返回False。
    # 如果只在根目录下忽略，检查当前目录是否为根目录下的直接子目录
    # 如果在任意位置都忽略，检查当前目录名是否匹配
    """
    for ignore_dir, only_root in ignore_rules:
        if only_root:
            if (
                os.path.basename(directory) == ignore_dir
                and os.path.dirname(directory) == root
            ):
                return True
        else:
            if os.path.basename(directory) == ignore_dir:
                return True
    return False


def print_tree(directory, prefix="", ignore_rules=None, root=""):
    if ignore_rules is None:
        ignore_rules = []
    if root == "":
        root = directory
    files = []
    if prefix == "":
        print(directory)
    else:
        print(prefix + os.path.basename(directory))
    prefix = prefix.replace("├──", "│  ").replace("└──", "   ")

    try:
        files = os.listdir(directory)
    except PermissionError as e:
        print(f"PermissionError: {e}")
        return
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return

    files.sort()
    entries = [os.path.join(directory, f) for f in files]

    for i, entry in enumerate(entries):
        if os.path.isdir(entry) and should_ignore(entry, root, ignore_rules):
            continue
        connector = "├──" if i < len(entries) - 1 else "└──"
        if os.path.isdir(entry):
            print_tree(
                entry,
                prefix=prefix + connector,
                ignore_rules=ignore_rules,
                root=root,
            )
        else:
            print(prefix + connector + os.path.basename(entry))


def gather_files(directory, ignore_rules=None, root="", extensions=None):
    if ignore_rules is None:
        ignore_rules = []
    if root == "":
        root = directory
    if extensions is None:
        extensions = [".py", ".rs", ".json"]
    all_files_content = ""
    for root, dirs, files in os.walk(directory):
        dirs[:] = [
            d
            for d in dirs
            if not should_ignore(os.path.join(root, d), root, ignore_rules)
        ]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                all_files_content += f"File: {file_path}\n```\n"
                with open(file_path, "r", encoding="utf-8") as f:
                    all_files_content += f.read()
                all_files_content += "\n```\n\n"
    return all_files_content


def main(directory_to_search):
    """
    # 任意位置的__pycache__都忽略
    # 只有根目录下的.git忽略
    """
    ignore_rules = [("__pycache__", False), (".git", True)]

    print("Generating file tree...")
    print_tree(directory_to_search, ignore_rules=ignore_rules)
    print("\nGathering files...")
    combined_code = gather_files(
        directory_to_search, ignore_rules=ignore_rules
    )
    print(combined_code)


if __name__ == "__main__":
    """
    # 把directory_to_search替换为你的代码目录
    """
    directory_to_search = "D:\\Git\\LaoshuBaby\\llm_unified_client"
    main(directory_to_search)
