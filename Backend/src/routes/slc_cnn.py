from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from src.helper.slc import load_interpreter, preprocess_image, predict_gesture
from src import logger

SLC_Router = APIRouter(prefix="/slc-static", tags=["Static Model"])
interpreter, labels = load_interpreter("STATIC")

@SLC_Router.post("/predict")
async def predict_static(file: UploadFile = File(...)):
    """Predict gesture from uploaded image (static model)."""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image.")

        img_bytes = await file.read()
        img = preprocess_image(img_bytes)
        result = predict_gesture(img, interpreter, labels)
        return JSONResponse(content=result)

    except Exception as e:
        logger.error(f"Static prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
