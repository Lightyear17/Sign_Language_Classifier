from os import path
from dotenv import dotenv_values

env_path = ".env"

if not path.exists(env_path):
    raise Exception(".env file not found")

config = dotenv_values(env_path)

HOST = config.get("HOST", "127.0.0.1")

_port_raw = config.get("PORT")
PORT = int(_port_raw) if _port_raw else 8000

MODEL_PATHS = {
    "STATIC_MODEL": config.get("STATIC_MODEL_PATH"),
    "REALTIME_MODEL": config.get("REALTIME_MODEL_PATH"),
}

MODEL_LABELS = {
    "STATIC_LABELS": config.get("STATIC_LABELS_PATH"),
    "REALTIME_LABELS": config.get("REALTIME_LABELS_PATH"),
}

