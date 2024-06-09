# 各模型提供方的调用API相关文档

虽然我觉得正常用户用不到这东西，给自己看方便debug的

## OpenAI

### API文档

* [`/v1/audio/speech`](https://platform.openai.com/docs/api-reference/audio/createSpeech)
* [`/v1/chat/completions`](https://platform.openai.com/docs/api-reference/chat/create)
* [`/v1/images/generations`](https://platform.openai.com/docs/api-reference/images/create)

### 指导手册

* 对话：https://platform.openai.com/docs/guides/text-generation/chat-completions-api
* 语音合成：https://platform.openai.com/docs/guides/text-to-speech
* 图像合成：https://platform.openai.com/docs/guides/images/language-specific-tips

## llama (Run by Ollama)

Ollama 提供了两种文档：
* [兼容OpenAI](https://github.com/ollama/ollama/blob/main/docs/openai.md)
* [原生](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion)

## llama (Run by Jan)

WIP

## 智谱清言

### API文档

* [`/paas/v4/chat/completions`](https://open.bigmodel.cn/dev/api#glm-4)
* [`/paas/v4/batches`](https://open.bigmodel.cn/dev/api#batch-api)

## 通义千问/文心一言

什么JB，想让API一致需要做出各种适配，而想自研一套不兼容的实在容易。

搞建设和统一难，搞分裂的话信创是有一手的。