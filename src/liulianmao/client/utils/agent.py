agent_judge_template = """
请你判断下列提问过程中是否需要调用外部程序？

目前支持的外部程序的列表有：

```python
{func_list}
```

如果你认为需要，则请输出且仅输出如下pagentcommand代码段中内容:

```pagentcommand
PSEUDO_AGENT:TRUE
PSEUDO_AGENT.ACTION:{{Prototype of function you think need to call, including parameters and typing}}
PSEUDO_AGENT.ACTION.NAME:{{The function's name}}
PSEUDO_AGENT.ACTION.PARA:{{The function's parameters in json}}
=+=+=
```

如果你认为不需要调用外部程序，则请输出且仅输出如下pagentcommand代码段中内容：

```pagentcommand
PSEUDO_AGENT:FALSE
=+=+=
```


如下代码段中是一段需要发送给AI进行提问的内容:

```plaintext
{question}
```

请根据是否需要调用外部程序，仅输出对应代码段内的内容，且无需输出任何其他内容。

"""
