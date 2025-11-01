# Sign Language Classifier

A full-stack web application for classifying American Sign Language (ASL) alphabet letters from images using a trained CNN model. The system provides real-time predictions through an intuitive web interface.

## 🎯 Overview

This project consists of two main components:
- **Backend**: FastAPI server with TensorFlow/Keras model for ASL letter classification
- **Frontend**: React application with modern UI for image upload and prediction visualization

## 🌟 Key Features

- 📸 **Static Gesture Recognition**: Upload images or provide URLs for ASL letter classification
- ✋ **Real-Time Hand Detection**: Live camera feed with MediaPipe hand tracking for continuous recognition
- 🤖 **Dual-Model System**: 
  - CNN model for static image classification
  - DNN model for real-time hand landmark recognition
- 📊 **Confidence Scores**: Visual representation of prediction confidence
- ⚡ **Fast Processing**: Optimized with TensorFlow and TensorFlow Lite
- 🎨 **Responsive UI**: Clean, intuitive interface for all devices
- 🧪 **Fully Tested**: Comprehensive unit tests with pytest and mocking

## 📁 Project Structure

```
Sign_Language_Classifier/
├── Backend/                    # FastAPI backend application
│   ├── src/                   # Source code
│   ├── libs/                  # Utilities and middleware
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend documentation
├── Frontend/                   # React frontend application
│   ├── src/                   # Source code
│   ├── public/               # Static assets
│   ├── package.json          # Node.js dependencies
│   └── README.md             # Frontend documentation
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Backend**: Python 3.8+, pip
- **Frontend**: Node.js 18+, npm/yarn
- Git

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Lightyear17/Sign_Language_Classifier.git
   cd Sign_Language_Classifier
   ```

2. **Set Up Backend**
   ```bash
   cd Backend
   # See Backend/README.md for detailed setup instructions
   ```

3. **Set Up Frontend**
   ```bash
   cd Frontend
   # See Frontend/README.md for detailed setup instructions
   ```

## 📚 Documentation

For detailed setup, configuration, and usage instructions, please refer to:

- **[Backend Documentation](./Backend/readme.md)** - API endpoints, environment setup, dependencies
- **[Frontend Documentation](./Frontend/README.md)** - UI features, build process, configuration

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **ML/AI**: TensorFlow 2.15+, Keras
- **Image Processing**: OpenCV, MediaPipe, Pillow
- **Data Processing**: NumPy, Pandas
- **Server**: Uvicorn
- **Testing**: Pytest with mocking

### Frontend
- **Framework**: React 19.1.1
- **Build Tool**: Vite 7.1.7
- **Hand Detection**: MediaPipe
- **Icons**: Lucide React
- **Styling**: Custom CSS
- **HTTP Client**: Fetch API

## 🔧 Configuration

Both applications require environment configuration:

- **Backend**: Copy `Backend/example.env` to `Backend/.env`
- **Frontend**: Copy `Frontend/.env.example` to `Frontend/.env`

Refer to respective README files for detailed configuration options.

## 🏗 Architecture

```
┌─────────────┐      HTTP/REST      ┌─────────────┐
│   Frontend  │ ──────────────────> │   Backend   │
│  (React +   │                     │  (FastAPI)  │
│    Vite)    │ <────────────────── │             │
└─────────────┘      JSON Response  └──────┬──────┘
                                            │
                                            ▼
                                    ┌───────────────┐
                                    │  CNN Model    │
                                    │  (TensorFlow) │
                                    └───────────────┘
```

## 🔒 Security

- Environment variables for sensitive configuration
- CORS configuration for API access control
- Input validation on both client and server
- File type and size restrictions

⚠️ **Important**: Never commit `.env` files to version control.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes following conventional commits
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Message Format
```
<type>: <description>

Changes Made:
- Change 1
- Change 2

Checklist:
- [x] Does it change the .env file?
- [ ] Does it depend on a previous commit?
- [x] Does the code follow conventional commit standards?
- [x] Has the code been tested manually or automatically?
- [x] Is the change less than 300 lines of code?
```

## 📝 License

This project is maintained by [Lightyear17](https://github.com/Lightyear17).

## 🐛 Issues & Support

If you encounter any issues or have questions:
- Check the specific README files for Backend and Frontend
- Review troubleshooting sections in component documentation
- Open an issue on GitHub with detailed information

## 🙏 Acknowledgments

- Sign Language MNIST dataset for model training
- FastAPI and React communities
- TensorFlow team for ML framework

---

**Built with ❤️ for accessible communication**
