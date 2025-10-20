from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional
import base64

from src.helper.slc import ModelHelper
from src import logger

model_helper = ModelHelper()

SLC_Router = APIRouter(prefix="/slc", tags=["Sign Language Classification"])

class ImageUrlRequest(BaseModel):
    """Request model for URL-based prediction"""
    image_url: HttpUrl


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    success: bool
    letter: Optional[str] = None
    confidence: Optional[float] = None
    error: Optional[str] = None


@SLC_Router.post("/predict", response_model=PredictionResponse)
async def predict_from_file(file: UploadFile = File(...)):
    """
    Predict sign language letter from uploaded image file.
    """
    try:
        logger.info(f"Received prediction request for file: {file.filename}")

        
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")

        
        image_bytes = await file.read()

        
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit.")

       
        result = model_helper.predict_from_bytes(image_bytes)

        if result["success"]:
            logger.info(f"Prediction successful: {result['letter']} ({result['confidence']}%)")
            return PredictionResponse(success=True, letter=result["letter"], confidence=result["confidence"])
        else:
            logger.error(f"Prediction failed: {result['error']}")
            return PredictionResponse(success=False, error=result["error"])

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error during prediction from file")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@SLC_Router.post("/predict/url", response_model=PredictionResponse)
async def predict_from_url(request: ImageUrlRequest):
    """
    Predict sign language letter from an image URL.
    """
    try:
        logger.info(f"Received prediction request for URL: {request.image_url}")
        result = model_helper.predict_from_url(str(request.image_url))

        if result["success"]:
            logger.info(f"Prediction successful: {result['letter']} ({result['confidence']}%)")
            return PredictionResponse(success=True, letter=result["letter"], confidence=result["confidence"])
        else:
            logger.error(f"Prediction failed: {result['error']}")
            return PredictionResponse(success=False, error=result["error"])

    except Exception as e:
        logger.exception("Error during prediction from URL")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@SLC_Router.post("/predict/base64", response_model=PredictionResponse)
async def predict_from_base64(image_data: str = Form(...)):
    """
    Predict sign language letter from base64 encoded image data.
    """
    try:
        logger.info("Received prediction request for base64 image")

        
        if "," in image_data:
            image_data = image_data.split(",")[1]
 
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid base64 image data.")
     
        result = model_helper.predict_from_bytes(image_bytes)

        if result["success"]:
            logger.info(f"Prediction successful: {result['letter']} ({result['confidence']}%)")
            return PredictionResponse(success=True, letter=result["letter"], confidence=result["confidence"])
        else:
            logger.error(f"Prediction failed: {result['error']}")
            return PredictionResponse(success=False, error=result["error"])

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error during prediction from base64")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@SLC_Router.get("/model/info")
async def get_model_info():
    """
    Get information about the loaded model.
    """
    try:
        info = model_helper.get_model_info()
        return JSONResponse(content=info)
    except Exception as e:
        logger.exception("Error getting model info")
        raise HTTPException(status_code=500, detail=f"Error retrieving model information: {str(e)}")
