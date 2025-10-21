import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import requests

from typing import Dict, Any, Optional
from keras.models import load_model
from libs.utils.config import MODEL_PATH
from src import logger

class ModelHelper:
    """Helper class for loading model and processing predictions"""
    
    
    LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
    
    def __init__(self, model_path: Optional[str] = MODEL_PATH):
        """
        Initialize the ModelHelper with a trained model
        
        Args:
            model_path: Path to the saved Keras model
        """
        if model_path is None:
            raise ValueError("MODEL_PATH is not configured. Please provide a valid model path.")
        self.model_path = model_path
        self.model: Any = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model"""
        try:
            logger.info(f"Loading model from: {self.model_path}")
            self.model = load_model(self.model_path)
            if self.model is not None:
                logger.info("Model loaded successfully")
            else:
                raise RuntimeError("Model loaded but returned None")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise RuntimeError(f"Could not load model from {self.model_path}: {str(e)}")
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for model input
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image ready for prediction
        """
        try:
            
            if len(image.shape) == 3:
                if image.shape[2] == 4:  
                    image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
                elif image.shape[2] == 3:  
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            
            image_resized = cv2.resize(image, (28, 28))
            
            
            image_normalized = image_resized.astype('float32') / 255.0
            
           
            image_input = image_normalized.reshape(1, 28, 28, 1)
            
            logger.debug(f"Image preprocessed - shape: {image_input.shape}, range: [{image_input.min():.4f}, {image_input.max():.4f}]")
            
            return image_input
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise ValueError(f"Image preprocessing failed: {str(e)}")
    
    def _predict(self, image_input: np.ndarray) -> Dict[str, Any]:
        """
        Make prediction on preprocessed image
        
        Args:
            image_input: Preprocessed image array
            
        Returns:
            Dictionary with prediction results
        """
        try:
            
            model = self.model
            if model is None or not hasattr(model, "predict"):
                raise RuntimeError("Model is not loaded or does not support prediction.")
            
            prediction = model.predict(image_input, verbose=0)
            
            
            predicted_class = np.argmax(prediction[0])
            confidence = float(np.max(prediction[0]) * 100)  
            predicted_letter = self.LABELS[predicted_class]
            
            
            top3_idx = np.argsort(prediction[0])[-3:][::-1]
            top3_predictions = [
                {
                    "letter": self.LABELS[idx],
                    "confidence": float(prediction[0][idx] * 100)
                }
                for idx in top3_idx
            ]
            
            logger.info(f"Prediction: {predicted_letter} ({confidence:.2f}%)")
            
            return {
                "success": True,
                "letter": predicted_letter,
                "confidence": round(confidence, 2),
                "top3": top3_predictions,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return {
                "success": False,
                "letter": None,
                "confidence": None,
                "error": f"Prediction failed: {str(e)}"
            }
    
    def predict_from_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Predict sign language letter from image bytes
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Dictionary with prediction results
        """
        try:
            
            image_pil = Image.open(BytesIO(image_bytes))
            
            
            image_np = np.array(image_pil)
            
            
            image_input = self._preprocess_image(image_np)
            
            
            result = self._predict(image_input)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing image bytes: {str(e)}")
            return {
                "success": False,
                "letter": None,
                "confidence": None,
                "error": f"Failed to process image: {str(e)}"
            }
    
    def predict_from_url(self, image_url: str) -> Dict[str, Any]:
        """
        Predict sign language letter from image URL
        
        Args:
            image_url: URL of the image
            
        Returns:
            Dictionary with prediction results
        """
        try:
            
            logger.info(f"Downloading image from: {image_url}")
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            
            image_bytes = response.content
            
            
            result = self.predict_from_bytes(image_bytes)
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading image from URL: {str(e)}")
            return {
                "success": False,
                "letter": None,
                "confidence": None,
                "error": f"Failed to download image: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Error processing image from URL: {str(e)}")
            return {
                "success": False,
                "letter": None,
                "confidence": None,
                "error": f"Failed to process image: {str(e)}"
            }
    
    def predict_from_path(self, image_path: str) -> Dict[str, Any]:
        """
        Predict sign language letter from local image path
        
        Args:
            image_path: Path to the local image file
            
        Returns:
            Dictionary with prediction results
        """
        try:
            
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            if image is None:
                raise ValueError(f"Could not load image from: {image_path}")
            
           
            image_input = self._preprocess_image(image)
            
            
            result = self._predict(image_input)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing image from path: {str(e)}")
            return {
                "success": False,
                "letter": None,
                "confidence": None,
                "error": f"Failed to process image: {str(e)}"
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model
        
        Returns:
            Dictionary with model information
        """
        if self.model is None:
            return {
                "loaded": False,
                "error": "Model not loaded"
            }
        
        return {
            "loaded": True,
            "model_path": self.model_path,
            "input_shape": str(self.model.input_shape),
            "output_shape": str(self.model.output_shape),
            "num_classes": len(self.LABELS),
            "labels": self.LABELS,
            "total_parameters": int(self.model.count_params())
        }