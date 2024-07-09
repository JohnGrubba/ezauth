from datetime import datetime


def preprocess(kwargs: dict) -> dict:
    kwargs["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return kwargs
