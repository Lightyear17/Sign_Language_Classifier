# Sign Language Classifier - FastAPI Backend

A FastAPI backend service for predicting American Sign Language (ASL) alphabet letters from images using a trained CNN model.

## 🛠 Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **ML Framework**: TensorFlow 2.15.0 / Keras 2.15.0
- **Image Processing**: OpenCV, Pillow
- **Data Processing**: NumPy
- **HTTP Client**: Requests
- **Validation**: Pydantic

## ✨ Features

- **Multiple Input Methods**: Upload files, provide URLs, or send base64 encoded images
- **CNN Model**: Trained on Sign Language MNIST dataset
- **24 ASL Letters**: Recognizes A-Y (excluding J and Z which require motion)
- **RESTful API**: Clean and well-documented endpoints
- **CORS Enabled**: Ready for frontend integration
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Robust error handling with meaningful messages
- **Type Safety**: Pydantic models for request/response validation
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc

## 📁 Project Structure

```
Backend/
├── src/
│   ├── __init__.py
│   ├── app.py                      # FastAPI application entry point
│   ├── routes/
│   │   └── slc.py                  # API route handlers
│   └── helper/
│       └── slc.py                  # Model loading and prediction logic
├── libs/
│   └── utils/
│       ├── config/                 # Configuration management
│       ├── logger/                 # Logging utilities
│       ├── middleware/             # Custom middleware
│       └── model/                  # Trained models
├── logs/                           # Application logs (auto-generated)
├── requirements.txt                # Python dependencies
└── example.env                     # Environment variables template
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Lightyear17/Sign_Language_Classifier.git
   cd Sign_Language_Classifier/Backend
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   # Copy example.env to .env and configure your settings
   cp example.env .env
   # Edit .env with your specific configuration
   ```

5. **Run the Application**
   ```bash
   # From the Backend directory
   python -m src.app
   ```

   The API will be available at:
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs

## 📡 API Endpoints

### Health Check
```http
GET /
```
Returns a simple health check response.

### Sign Language Classification
```http
POST /api/slc/*
```
Various endpoints for sign language classification. See interactive documentation at `/docs` for detailed API specifications.

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔒 Security Considerations

- Never commit `.env` files to version control
- Keep your model files secure and version controlled separately if they contain sensitive training data
- In production, configure CORS to allow only specific origins instead of `*`
- Use environment variables for all sensitive configuration
- Regularly update dependencies to patch security vulnerabilities

## 📝 Environment Variables

See `example.env` for required environment variables. Create a `.env` file based on this template with your specific configuration.

---

**Built with FastAPI and TensorFlow**