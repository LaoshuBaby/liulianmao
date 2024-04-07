from .log import logger

# 合并后的模型和变体信息
MODEL_INFO = {
    "gpt-3.5-turbo": {
        "ratio": 0.75,
        "variants": [
            "gpt3", "gpt-3", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0125",  "gpt-3.5-turbo-instruct"
        ]
    },
    "gpt-3.5-turbo-16k": {
        "ratio": 1.5,
        "variants": [
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-16k-0613"
        ]
    },
    "gpt-4-turbo-preview": {
        "ratio": 5.00,
        "variants": [
            "gpt-4-1106-preview", "gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-4-turbo"
        ]
    },
    "gpt-4": {
        "ratio": 15.00,
        "variants": [
            "gpt4", "GPT-4", "gpt-4-0314", "gpt-4-0613"
        ]
    },
    "gpt-4-32k": {
        "ratio": 30.00,
        "variants": [
            "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-0613"
        ]
    },
    "gpt-4-vision-preview": {
        "ratio": None,  # Assuming we don't have a ratio for this model yet
        "variants": [
            "gpt-4-vision-preview"
        ]
    }
}

def select_model(input_model_name, available_models, direct_debug:bool=False):
    if direct_debug == True:
        return input_model_name
    input_model_name = input_model_name.lower()
    for model_name, model_info in MODEL_INFO.items():
        variants = model_info["variants"]
        if input_model_name in variants:
            available_variants = [v for v in variants if v in available_models]
            if available_variants:
                # 选择最新的变体
                selected_variant = max(available_variants)
                ratio = model_info["ratio"]
                if ratio is not None:
                    logger.info(f"[Model] {selected_variant} ({ratio}x)")
                    return selected_variant
                else:
                    logger.error(f"[Model] No ratio defined for {selected_variant}.")
                    return None
    logger.error("[Model] Model not found.")
    return None
