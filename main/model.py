# import os module to interact with the operating system
import os

# import YOLO from the ultralytics library
from ultralytics import YOLO


def load_model(model_path=None):
    # use environment variable if model path is not passed
    # if model_path is not provided, get it from the environment variable, else use the default path
    model_path = model_path or os.getenv("MODEL_PATH", "weight/best.pt")

    # check if the model file exists at the given path
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at path: {model_path}"
        )  # raise an error if the model file doesn't exist

    # return the YOLO model initialized with the model file
    return YOLO(model_path)
