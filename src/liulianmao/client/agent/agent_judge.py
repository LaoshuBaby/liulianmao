import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))


from module.log import logger


def get_agent_judge_template():
    flag_agent_debug = False

    agent_judge_template = """
    请你判断下列提问过程中是否需要调用外部程序？

    目前支持的外部程序的列表有：

    ```python
{func_list}
    ```

    如果你认为需要，则请输出{{{no_debug_only_return}}}如下agentcommand代码段中内容:

    ```agentcommand
    AGENT:TRUE
    AGENT.ACTION:{{Prototype of function you think need to call, including parameters and typing}}
    AGENT.ACTION.NAME:{{The function's name}}
    AGENT.ACTION.PARA:{{The function's parameters in JSON, list each parameter as key and its value. This SHOULD be a JSON.}}
    =+=+=
    ```

    如果你认为不需要调用外部程序，则请输出{{{no_debug_only_return}}}如下agentcommand代码段中内容：

    ```agentcommand
    AGENT:FALSE
    =+=+=
    ```


    如下代码段中是一段需要发送给AI进行提问的内容:

    ```plaintext
    {question}
    ```

    请根据是否需要调用外部程序，仅输出对应代码段内的内容，{{{action_debug_or_action_return}}}。

    """

    if flag_agent_debug == True:
        agent_judge_template = agent_judge_template.replace(
            "{{{no_debug_only_return}}}", ""
        )
    else:
        agent_judge_template = agent_judge_template.replace(
            "{{{no_debug_only_return}}}", "且仅输出"
        )

    if flag_agent_debug == True:
        agent_judge_template = agent_judge_template.replace(
            "{{{action_debug_or_action_return}}}",
            "并解释为什么不匹配所有函数的原因，需要逐个函数的解释",
        )
    else:
        agent_judge_template = agent_judge_template.replace(
            "{{{action_debug_or_action_return}}}", "且无需输出任何其他内容"
        )

    logger.trace(f"[flag_agent_debug]: {flag_agent_debug}")
    logger.trace(f"[agent_judge_template (replaced)]:\n{agent_judge_template}")

    if flag_agent_debug == True:
        logger.info(
            "检测到您开启了flag_agent_debug变量，这意味着您希望解释为什么选择函数，请注意这可能干扰最终的结果判定"
        )
    return agent_judge_template
