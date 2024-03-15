# LLM Unified Client

**LLMUC**是LaoshuBaby自用的一个在命令行或者IDE中使用的大语言模型客户端。本项目主要为鼠宝宝及友人提供服务，亦用作个人codebase在各种机器人和实验性项目中快速调用。

目前仅测试了OpenAI提供的服务。理论上亦可直接用于零一万物或通义千问的服务。

若需要快速切换不同模型，可使用通过one-api或new-api聚合后的token。

## 配置方法

安装所需要的库：

```shell
pip install requests loguru
```

若需使用langchain，还需安装：

```shell
pip install langchain langchain_openai
```

在系统环境变量中配置`OPENAI_API_KEY`的值为你所使用的API。当然您亦可在代码中硬编码，但鼠宝宝不推荐这么做。（如果您配置过langchain，那就不需要再次配置了！）

## 联系我

Telegram [@laoshubaby](https://t.me/laoshubaby)

~~( 虽然是MIT协议，您可以自由使用，但如果您是在GitHub上搜到的这个项目，建议使用前先与我咨询，因为可能真的不好用。若能帮到您，就算交个朋友啦！**φ(゜▽゜*)♪** )~~