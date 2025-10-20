from fastapi import FastAPI
import uvicorn

from src import logger
from libs.utils.config import HOST, PORT
from libs.utils.middleware.service import ServiceMiddleware
from src.routes.slc import SLC_Router

app = FastAPI()

app.add_middleware(ServiceMiddleware)


@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}

app.include_router(SLC_Router)

if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST or "0.0.0.0", port=PORT)