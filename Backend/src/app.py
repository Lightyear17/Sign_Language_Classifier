from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src import logger
from libs.utils.config import HOST, PORT
from libs.utils.middleware.service import ServiceMiddleware
from src.routes.slc import SLC_Router

app = FastAPI()

app.add_middleware(ServiceMiddleware)

app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}

app.include_router(SLC_Router)

if __name__ == "__main__":
    uvicorn.run("src.app:app", host=HOST or "0.0.0.0", port=PORT)