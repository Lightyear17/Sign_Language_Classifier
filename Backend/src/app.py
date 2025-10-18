from fastapi import FastAPI
import uvicorn

from libs.utils.config import HOST, PORT


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT)