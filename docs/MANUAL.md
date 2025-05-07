# 给开发者 / For Developer

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
* /module 下面都是无论如何都会用到的各个模块
* /client/api 这个和模型提供方有关，不同模型提供方会有不同的API(如openai、llama、zhipu、enrie)

## GitHub Actions 和 Sphinx 文档生成

本项目使用 GitHub Actions 自动构建和部署 Sphinx 文档到 GitHub Pages。以下是相关配置和步骤的说明：

- GitHub Actions 工作流配置文件位于 `.github/workflows/sphinx.yml`。
- 文档源文件位于 `docs/` 目录下。
- Sphinx 配置文件为 `docs/conf.py`，其中定义了项目名称、作者等信息。
- 依赖项（包括 Sphinx 和主题）列在 `docs/requirements.txt` 中，GitHub Actions 会自动安装这些依赖。
- 文档构建命令为 `sphinx-build -b html docs/ _build/html`，该命令会在 `docs/` 目录下生成 HTML 格式的文档。
- 构建完成的文档通过 `peaceiris/actions-gh-pages@v3` 部署到 GitHub Pages。

这样配置后，每次向 `main` 分支推送更新时，GitHub Actions 会自动构建和部署最新的文档，无需手动干预。

## 部分概念解析：

在本项目中有一些名词长得很像或者因为它并不是在常见的接口容易提到而是我们为了更好的抽象而造出来的概念

因此在这里统一文档化和描述它们。

* `model_series`

代表模型的代系，一般来说属于同一家公司的或者衍生自同一个基座模型的属于同一代系。

例如OpenAI公司的`gpt-3.5-turbo`或者`gpt-4-turbo-preview`等，都可属于`openai`这一代系。

而所有基于`llama`衍生的模型，都可属于`llama`这一代系。

* `model`

具体的模型名称，很好解释
