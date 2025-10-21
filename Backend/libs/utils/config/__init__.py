from os import path
from dotenv import dotenv_values

env_path = ".env"

if not path.exists(env_path):
    raise Exception(".env request_file not found")

config = dotenv_values(env_path)


HOST = config.get("HOST")
_port_raw = config.get("PORT")
PORT = int(_port_raw) if _port_raw else 8000
MODEL_PATH = config.get("MODEL_PATH")