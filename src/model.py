from log import logger

MODELS = {
    "gpt-3.5-turbo": 0.75,
    "gpt-4-turbo-preview": 5.00,
    "gpt-4": 15.00,
    "gpt-4-32k": 30.00,
}


def select_model(model_name):
    if model_name in MODELS:
        logger.info(
            f"Selected model: {model_name} (Price: ${MODELS[model_name]})"
        )
        return model_name
    else:
        logger.error("Model not found.")
        return None
