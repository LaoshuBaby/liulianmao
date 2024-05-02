# 给开发者

## 我希望把它打包成exe给小白用

虽然可能并不会有我以外的人这么干，但如果你想要打包可以按照如下流程

0. 确保您的pwd在 `__main__.py` 的同目录下
1. 安装pyinstaller： `pip install pyinstaller`
2. 安装venv： `pip install venv` (这一步通常可以跳过，因为它是默认库的一部分 https://docs.python.org/3/library/venv.html )
3. 创建一个名为llm的venv： `python -m venv myllm`
4. 激活venv： `myllm\Scripts\activate`
5. 安装如下依赖项： `pip install loguru requests hellologger`
6. 在venv中安装pyinstaller： `pip install pyinstaller`
7. 返回上一级文件夹： `cd ..`
8. 执行打包命令： `pyinstaller --onefile --name=liulianmao liulianmao/__main__.py`

此外我不推荐你这么做，本项目更新的速度一定会累死打包的，而我不打算直接用二进制因此也不会为这种打包写CI配置文件。

## 各个文件是干嘛的

* __init__.py 决定这是包
* __main__.py 接受命令行传参和import，解析recipe并执行
* /client/core.py 平凡的restful客户端
* /client/openai.py 使用openai的py库的客户端
* /client/langchain.py 使用langchain的客户端
* /module 下面都是无论如何都会用到的各个模块
* /client/api 这个和模型提供方有关，不同模型提供方会有不同的API