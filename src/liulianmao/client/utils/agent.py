flag_agent_debug=False

agent_judge_template_raw = """
请你判断下列提问过程中是否需要调用外部程序？

目前支持的外部程序的列表有：

```python
{func_list}
```

如果你认为需要，则请输出{{{no_debug_only_return}}}如下pagentcommand代码段中内容:

```pagentcommand
PSEUDO_AGENT:TRUE
PSEUDO_AGENT.ACTION:{{Prototype of function you think need to call, including parameters and typing}}
PSEUDO_AGENT.ACTION.NAME:{{The function's name}}
PSEUDO_AGENT.ACTION.PARA:{{The function's parameters in json}}
=+=+=
```

如果你认为不需要调用外部程序，则请输出{{{no_debug_only_return}}}如下pagentcommand代码段中内容：

```pagentcommand
PSEUDO_AGENT:FALSE
=+=+=
```


如下代码段中是一段需要发送给AI进行提问的内容:

```plaintext
{question}
```

请根据是否需要调用外部程序，仅输出对应代码段内的内容，{{{action_debug_or_action_return}}}。

"""

if flag_agent_debug == True:
    agent_judge_template_raw.replace("{{{no_debug_only_return}}}","")
else:
    agent_judge_template_raw.replace("{{{no_debug_only_return}}}","且仅输出")

if flag_agent_debug == True:
    agent_judge_template_raw.replace("{{{action_debug_or_action_return}}}","并解释为什么不匹配所有函数的原因，需要逐个函数的解释")
else:
    agent_judge_template_raw.replace("{{{action_debug_or_action_return}}}","且无需输出任何其他内容")

agent_judge_template=agent_judge_template_raw