from .log import logger

# 使用Python字典和列表表示JSON结构
MODELS = [
    {"name": "gpt-3.5-turbo", "ratio": 0.75},
    {"name": "gpt-4-turbo-preview", "ratio": 5.00},
    {"name": "gpt-4", "ratio": 15.00},
    {"name": "gpt-4-32k", "ratio": 30.00},
]


def select_model(model_name):
    for model in MODELS:
        if model["name"] == model_name:
            logger.info(f"[Model] {model['name']} ({model['ratio']}x)")
            return model_name
    logger.error("[Model] Model not found.")
    return None
