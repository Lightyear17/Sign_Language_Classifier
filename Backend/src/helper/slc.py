import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf

from libs.utils.config import MODEL_PATHS, MODEL_LABELS


mp_hands = mp.solutions.hands


def load_interpreter(model_type: str):
    """Load TensorFlow Lite model and corresponding labels."""
    try:
        if model_type.upper() == "STATIC":
            model_path = MODEL_PATHS["STATIC_MODEL"]
            labels_path = MODEL_LABELS["STATIC_LABELS"]
        elif model_type.upper() == "REALTIME":
            model_path = MODEL_PATHS["REALTIME_MODEL"]
            labels_path = MODEL_LABELS["REALTIME_LABELS"]
        else:
            raise ValueError(f"Invalid model type: {model_type}")

        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        labels = np.load(labels_path, allow_pickle=True)
        print(f"Loaded {model_type} model from {model_path}")
        return interpreter, labels

    except Exception as e:
        raise RuntimeError(f"Error loading {model_type} model: {e}")


def preprocess_image(img_bytes: bytes):
    """Convert raw bytes to OpenCV BGR image."""
    npimg = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image data.")
    return img


def preprocess_landmarks(landmarks):
    """Normalize landmarks like in training."""
    x = np.array([lm.x for lm in landmarks])
    y = np.array([lm.y for lm in landmarks])
    cx, cy = np.mean(x), np.mean(y)
    x, y = x - cx, y - cy
    max_val = max(np.ptp(x), np.ptp(y))
    x, y = x / max_val, y / max_val
    return np.array([[v for pair in zip(x, y) for v in pair]], dtype=np.float32)


def predict_gesture(img, interpreter, labels):
    """Auto-detect model input shape → run correct preprocessing."""
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_shape = input_details[0]["shape"]

   
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

   
    if len(input_shape) == 4:
       
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (input_shape[1], input_shape[2]))
        gray = gray.astype("float32") / 255.0

       
        gray = np.expand_dims(gray, axis=(0, -1))
        interpreter.set_tensor(input_details[0]["index"], gray)
        interpreter.invoke()

   
    else:
        hands = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        results = hands.process(img_rgb)

        if not results.multi_hand_landmarks:
            return {"label": "-", "confidence": 0.0}

        data = preprocess_landmarks(results.multi_hand_landmarks[0].landmark)
        interpreter.set_tensor(input_details[0]["index"], data)
        interpreter.invoke()

  
    output_data = interpreter.get_tensor(output_details[0]["index"])
    pred_index = int(np.argmax(output_data))
    confidence = float(np.max(output_data))

    return {
        "label": str(labels[pred_index]),
        "confidence": round(confidence, 3)
    }



def real_time_prediction():
    
    interpreter_static, labels_static = load_interpreter("STATIC")
    interpreter_realtime, labels_realtime = load_interpreter("REALTIME")

    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        
        frame = cv2.flip(frame, 1)
       
        prediction_static = predict_gesture(frame, interpreter_static, labels_static)
       
        prediction_realtime = predict_gesture(frame, interpreter_realtime, labels_realtime)

        cv2.putText(frame, f"Static: {prediction_static['label']} ({prediction_static['confidence']}%)", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(frame, f"Realtime: {prediction_realtime['label']} ({prediction_realtime['confidence']}%)", 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        
        cv2.imshow("Hand Gesture Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    real_time_prediction()
