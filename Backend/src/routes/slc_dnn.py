from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import numpy as np
import tensorflow as tf
from src.helper.slc import load_interpreter
from src import logger


SLC_Realtime_Router = APIRouter(prefix="/slc-realtime", tags=["Realtime Model"])


interpreter, labels = load_interpreter("REALTIME")


class LandmarksRequest(BaseModel):
    landmarks: List[float] 


@SLC_Realtime_Router.post("/predict")
async def predict_realtime(request: LandmarksRequest):
    """
    Accepts normalized hand landmarks (42 values: x1, y1, x2, y2, ... x21, y21)
    and runs the real-time .tflite model.
    """
    try:
        landmarks = request.landmarks
        
        
        if len(landmarks) != 42:
            raise HTTPException(
                status_code=400, 
                detail=f"Expected 42 landmark values, got {len(landmarks)}"
            )
        
       
        data = np.array([landmarks], dtype=np.float32)
        
       
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        interpreter.set_tensor(input_details[0]["index"], data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]["index"])
        
        pred_index = int(np.argmax(output_data))
        confidence = float(np.max(output_data))
        label = str(labels[pred_index])
        
        logger.info(f"Predicted {label} ({confidence:.3f})")
        
        return {"label": label, "confidence": round(confidence, 3)}
    
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Realtime prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@SLC_Realtime_Router.post("/predict-image")
async def predict_realtime_image(request: Request):
    """
    LEGACY ENDPOINT: Accepts base64-encoded webcam image.
    This keeps your original functionality intact.
    """
    import base64
    import cv2
    import mediapipe as mp
    
    try:
        data = await request.json()
        image_base64 = data.get("image")

        if not image_base64:
            raise HTTPException(status_code=400, detail="Missing 'image' in request body")

        
        image_bytes = base64.b64decode(image_base64.split(",")[1])
        npimg = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image data")

        
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if not results.multi_hand_landmarks:
            return JSONResponse({"label": "-", "confidence": 0.0})

        
        hand_landmarks = results.multi_hand_landmarks[0]
        
        x = np.array([lm.x for lm in hand_landmarks.landmark])
        y = np.array([lm.y for lm in hand_landmarks.landmark])
        cx, cy = np.mean(x), np.mean(y)
        x, y = x - cx, y - cy
        max_val = max(np.ptp(x), np.ptp(y))
        x, y = x / max_val, y / max_val
        flattened = np.array([[v for pair in zip(x, y) for v in pair]], dtype=np.float32)

       
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]["index"], flattened)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]["index"])

        pred_index = int(np.argmax(output_data))
        confidence = float(np.max(output_data))
        label = str(labels[pred_index])

        logger.info(f"Predicted {label} ({confidence:.3f})")

        return {"label": label, "confidence": round(confidence, 3)}

    except Exception as e:
        logger.error(f"Realtime prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))