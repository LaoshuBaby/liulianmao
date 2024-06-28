import os


def main() -> None:
    global_const_data = [
        {x.split("=")[0]: x.split("=")[1]}
        for x in open("src/liulianmao/const.py", "r")
        .read()
        .replace(" ", "")
        .replace('"', "")
        .split("\n")
        if x != ""
    ]
    global_const = {}
    for tag in global_const_data:
        global_const = {**global_const, **tag}
    print(global_const)
    # run
    build_file_read = open("pyproject.toml", "r", encoding="utf-8")
    build_file_content = build_file_read.read().replace(
        "__LIULIANMAO_VERSION__", global_const["LIULIANMAO_VERSION"]
    )
    build_file_read.close()
    os.remove("pyproject.toml")
    build_file_write = open("pyproject.toml", "w", encoding="utf-8")
    build_file_write.write(build_file_content)
    build_file_write.close()


if __name__ == "__main__":
    main()
