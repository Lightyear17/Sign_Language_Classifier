from fastapi import FastAPI
import uvicorn

from src import logger
from libs.utils.config import HOST, PORT
from libs.utils.middleware.service import ServiceMiddleware

app = FastAPI()

app.add_middleware(ServiceMiddleware)

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT)