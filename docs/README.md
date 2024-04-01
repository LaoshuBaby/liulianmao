# 给开发者

虽然可能并不会有我以外的人，但如果你想要打包可以按照如下流程

0. 确保您的pwd在 `__main__.py` 的同目录下
1. 安装pyinstaller： `pip install pyinstaller`
2. 安装venv： `pip install venv` (这一步通常可以跳过，因为它是默认库的一部分 https://docs.python.org/3/library/venv.html )
3. 创建一个名为llm的venv： `python -m venv myllm`
4. 激活venv： `myllm\Scripts\activate`
5. 安装如下依赖项： `pip install loguru requests hellologger`
6. 在venv中安装pyinstaller： `pip install pyinstaller`
7. 返回上一级文件夹： `cd ..`
8. 执行打包命令： `pyinstaller --onefile --name=liulianmao liulianmao/__main__.py`