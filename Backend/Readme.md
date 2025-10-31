# 🧠 Sign Language Classifier – FastAPI Backend

A **FastAPI backend service** for **American Sign Language (ASL)** alphabet recognition.
It supports both **static image (CNN)** and **real-time hand landmark (DNN)** classification models trained with TensorFlow.

---

## 🛠️ Tech Stack

| Category              | Technology                    |
| --------------------- | ----------------------------- |
| **Backend Framework** | FastAPI 0.104+                |
| **Server**            | Uvicorn                       |
| **Machine Learning**  | TensorFlow 2.15 / Keras       |
| **Image Processing**  | OpenCV, MediaPipe, Pillow     |
| **Data Handling**     | NumPy, Pandas                 |
| **Validation**        | Pydantic                      |
| **Testing**           | Pytest, Monkeypatch, Mocking  |
| **CORS**              | Configured for React frontend |

---

## ✨ Features

* 🖼️ **Static Gesture Classification (CNN)**
  Upload or provide a URL of a hand image to predict its ASL letter.

* ✋ **Real-Time Gesture Recognition (DNN)**
  Receives 42 normalized MediaPipe landmarks via API for continuous gesture recognition.

* 🧠 **Dual-Model Inference**
  Supports both TensorFlow and TensorFlow Lite models.

* ⚙️ **Error-Handled APIs**
  Built-in validation, detailed error messages, and structured logging.

* 🧩 **Fully Tested**
  Includes unit tests with **mocking** and **monkeypatching** using **pytest**.

* 🧱 **Extensible Design**
  Modular route structure (`slc_cnn.py`, `slc_dnn.py`) for easy model updates.

* 📘 **Interactive Docs**
  Swagger UI and ReDoc available by default.

---

## 📂 Project Structure

```
Backend/
├── src/
│   ├── app.py                         # FastAPI app entry point
│   ├── routes/
│   │   ├── slc_cnn.py                 # Static CNN model route (/slc-static)
│   │   └── slc_dnn.py                 # Real-time DNN model route (/slc-realtime)
│   └── helper/
│       └── slc.py                     # Shared logic for loading & predicting models
├── libs/
│   └── utils/
│       ├── config/__init__.py         # Configuration & model paths
│       ├── logger/__init__.py         # Logging setup
│       ├── middleware/service.py      # Custom middleware
│       └── model/                     # TFLite & label files
├── tests/                             # Unit tests (pytest + mocking)
│   ├── test_slc_cnn.py
│   └── test_slc_dnn.py
├── logs/                              # Generated logs
├── requirements.txt                   # Dependencies
└── example.env                        # Environment variables template
```

---

## 🚀 Installation & Setup

### Prerequisites

* Python 3.8+
* pip

### Steps

#### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd Sign_Language_Classifier/Backend
```

#### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# or
source .venv/bin/activate # macOS/Linux
```

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure Environment Variables

```bash
cp example.env .env
```

Edit `.env` with your custom HOST, PORT, and model paths.

#### 5️⃣ Start the Server

```bash
python -m src.app
```

Server will run at:

* API: [http://localhost:3000](http://localhost:3000)
* Swagger UI: [http://localhost:3000/docs](http://localhost:3000/docs)
* ReDoc: [http://localhost:3000/redoc](http://localhost:3000/redoc)

---

## 📡 API Endpoints

### 🧩 Root Endpoint

```http
GET /
```

Health check for the server.

---

### 🖼️ Static Gesture Prediction (CNN)

```http
POST /slc-static/predict
```

**Input:** Image file (PNG, JPG)

```bash
multipart/form-data
file: hand.png
```

**Response:**

```json
{
  "label": "A",
  "confidence": 0.982
}
```

---

### 🌐 Static Gesture via URL

```http
POST /slc-static/predict-url
```

**Body:**

```json
{ "url": "https://example.com/hand.png" }
```

**Response:**

```json
{ "label": "B", "confidence": 0.955 }
```

---

### ✋ Real-Time Gesture Prediction (DNN)

```http
POST /slc-realtime/predict
```

**Input:** Normalized landmarks from MediaPipe

```json
{
  "landmarks": [x1, y1, x2, y2, ..., x21, y21]
}
```

**Response:**

```json
{ "label": "F", "confidence": 0.967 }
```

---

## 🧠 Model Summary

| Model | Type     | Input           | Output               | File                                |
| ----- | -------- | --------------- | -------------------- | ----------------------------------- |
| CNN   | Image    | 28×28 grayscale | 24 ASL letters (A–Y) | static_keypoint_classifier.tflite   |
| DNN   | Landmark | 42 float points | 24 ASL letters (A–Y) | realtime_keypoint_classifier.tflite |

⚠️ Letters **J** and **Z** are excluded as they require motion.

---

## 🧪 Testing

Unit tests ensure backend stability using **pytest**, **monkeypatch**, and **mocking**.

Run all tests:

```bash
python -m pytest -v
```

Output example:

```
4 passed, 2 warnings in 3.95s
```

Tests cover:

* ✅ Static model predictions (`/slc-static/predict`)
* ✅ Realtime DNN predictions (`/slc-realtime/predict`)
* ✅ Error handling & invalid inputs

---

## ⚙️ Environment Variables

| Variable               | Description                 | Example                                                                             |
| ---------------------- | --------------------------- | ----------------------------------------------------------------------------------- |
| `HOST`                 | Server host                 | `0.0.0.0`                                                                           |
| `PORT`                 | Port number                 | `3000`                                                                              |
| `STATIC_MODEL_PATH`    | Path to CNN `.tflite` model | `libs/utils/model/keypoint_classifier_static/static_keypoint_classifier.tflite`     |
| `STATIC_LABELS_PATH`   | Path to CNN labels          | `libs/utils/model/keypoint_classifier_static/static_label_classes.npy`              |
| `REALTIME_MODEL_PATH`  | Path to DNN `.tflite` model | `libs/utils/model/keypoint_classifier_realtime/realtime_keypoint_classifier.tflite` |
| `REALTIME_LABELS_PATH` | Path to DNN labels          | `libs/utils/model/keypoint_classifier_realtime/realtime_label_classes.npy`          |

---

## 🧾 Developer Notes

* 🧠 **FastAPI modular routing** allows independent model updates.
* 🔁 **CORS Middleware** enables frontend integration.
* ⚙️ **Pytest mocking** simulates predictions without running heavy ML models.
* 🧱 **Custom middleware** logs every API call for observability.
* 🧩 Compatible with **Windows**, **Linux**, and **macOS**.

---

## 🧰 Example Frontend Integration

```javascript
const response = await fetch(`${API_BASE_URL}/slc-realtime/predict`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ landmarks }),
});
const result = await response.json();
console.log(result.label, result.confidence);
```

---

## 🧩 Future Improvements

* Integrate LSTM-based temporal models for motion gestures (J, Z)
* Add multilingual gesture dataset expansion
* Deploy to Docker with CI/CD integration
* Optimize TensorFlow Lite models for mobile inference

---

## 🔒 Security Guidelines

* Do not commit `.env` or model weights to public repos
* Restrict CORS origins in production
* Use HTTPS for webcam-based data transfers
* Regularly update dependencies and scan vulnerabilities

---

**Built with ❤️ using FastAPI, TensorFlow, and MediaPipe**
*Empowering accessibility through AI-driven Sign Language Recognition.*
