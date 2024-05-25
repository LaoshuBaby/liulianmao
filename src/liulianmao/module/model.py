from .log import logger

# 合并后的模型和变体信息
MODEL_INFO = {
    "gpt-3.5-turbo": {
        "ratio": 0.75,
        "variants": [
            "gpt3",
            "gpt-3",
            "gpt-3.5-turbo-0301",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-0125",
            "gpt-3.5-turbo-instruct",
        ],
    },
    "gpt-3.5-turbo-16k": {
        "ratio": 1.5,
        "variants": ["gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"],
    },
    "gpt-4-turbo-preview": {
        "ratio": 5.00,
        "variants": [
            "gpt-4-1106-preview",
            "gpt-4-0125-preview",
            "gpt-4-turbo-preview",
            "gpt-4-turbo",
        ],
    },
    "gpt-4": {
        "ratio": 15.00,
        "variants": ["gpt4", "GPT-4", "gpt-4-0314", "gpt-4-0613"],
    },
    "gpt-4-32k": {
        "ratio": 30.00,
        "variants": ["gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-0613"],
    },
    "gpt-4-vision-preview": {
        "ratio": None,  # Assuming we don't have a ratio for this model yet
        "variants": ["gpt-4-vision-preview"],
    },
}


def select_model(
    input_model_name, available_models, direct_debug: bool = False
):
    def log_and_return(model_name, ratio="NaN"):
        """
        辅助函数，用于记录日志并返回模型名称。
        如果在直接调试模式下，比率记录为NaN；否则，记录实际的比率。
        """
        logger.info(f"[Model] {model_name} ({ratio} x)")
        return model_name

    if direct_debug:
        # 直接调试模式下，不查找MODEL_INFO，直接记录日志并返回模型名称
        logger.trace("[Model] directly log_and_return")
        return log_and_return(input_model_name)

    input_model_name = input_model_name.lower()
    for model_name, model_info in MODEL_INFO.items():
        variants = model_info["variants"]
        if input_model_name in variants:
            available_variants = [v for v in variants if v in available_models]
            if available_variants:
                # 选择最新的变体
                selected_variant = max(available_variants)
                return log_and_return(
                    selected_variant, model_info.get("ratio")
                )

    logger.error("[Model] Model not found.")
    return None
