# Sign Language Classifier - Frontend

A modern React frontend application for classifying American Sign Language (ASL) alphabet letters from images using a trained CNN model.

## 🛠 Tech Stack

- **Framework**: React 19.1.1
- **Build Tool**: Vite 7.1.7
- **UI Icons**: Lucide React 0.546.0
- **Styling**: Custom CSS
- **HTTP Client**: Fetch API

## ✨ Features

- **Static Gesture Recognition**: 
  - Upload image files (drag & drop interface)
  - Predict ASL letters from static images
- **Real-time Hand Gesture Detection**: 
  - Live camera feed with MediaPipe hand tracking
  - Real-time ASL gesture recognition
- **Visual Feedback**: 
  - Image/video preview
  - Confidence score visualization
  - Loading states and error handling
  - FPS counter for real-time mode
- **Responsive Design**: Clean and intuitive user interface
- **Error Handling**: Comprehensive validation and user-friendly error messages

## 📁 Project Structure

```
Frontend/
├── src/
│   ├── App.jsx                     # Main application component
│   ├── App.css                     # Application styles
│   ├── main.jsx                    # Application entry point
│   ├── components/
│   │   ├── Staticgesture.jsx       # Static image gesture recognition
│   │   ├── Handgesture.jsx         # Real-time hand gesture detection
│   │   └── mediapipe/              # MediaPipe utilities
│   └── index.css                   # Global styles
├── public/                         # Static assets
├── .env                           # Environment variables (not committed)
├── .env.example                   # Environment variables template
├── package.json                   # Dependencies and scripts
├── vite.config.js                 # Vite configuration
└── index.html                     # HTML template
```

## 🚀 Installation

### Prerequisites
- Node.js 18.x or higher
- npm or yarn package manager
- Backend API running (see Backend README)

### Steps

1. **Navigate to Frontend Directory**
   ```bash
   cd Sign_Language_Classifier/Frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Configure Environment Variables**

   Copy the example env file to a real `.env` in the project root and set your backend API URL. Vite only exposes variables that begin with `VITE_` to client-side code.

   - PowerShell (Windows):

   ```powershell
   Copy-Item .env.example .env
   # then edit .env and set your backend URL:
   # VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

   - macOS / Linux (bash):

   ```bash
   cp .env.example .env
   # then edit .env and set your backend URL:
   # VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

   After changing or creating `.env`, restart the Vite dev server so the new variables are picked up.

4. **Run Development Server**
   ```bash
   npm run dev
   ```

   The application will be available at:
   - Local: http://localhost:5173
   - Network: Check terminal output for network URL

5. **Build for Production**
   ```bash
   npm run build
   ```

   Production files will be in the `dist/` directory.

6. **Preview Production Build**
   ```bash
   npm run preview
   ```

## 📡 API Integration

The frontend communicates with the FastAPI backend through the following endpoints:

### Static Gesture Recognition
- **File Upload Prediction**: `POST /slc-static/predict`
  - Accepts: FormData with image file
  - Returns: `{ label: string, confidence: float }`

### Real-time Hand Gesture Detection
- **Hand Landmarks Prediction**: `POST /slc-realtime/predict`
  - Accepts: `{ landmarks: [x1, y1, x2, y2, ..., x21, y21] }` (42 values)
  - Returns: `{ label: string, confidence: float }`

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | `http://127.0.0.1:8000` |

⚠️ **Important**: 
- The `VITE_` prefix is required for Vite to expose the variable to your client-side code.
- Update `.env.example` with `VITE_API_BASE_URL=http://127.0.0.1:8000` for local development.

## 🎨 Features Overview

### Static Gesture Recognition (`Staticgesture.jsx`)
- Upload image files (PNG, JPG, JPEG)
- Real-time file validation
- Image preview before prediction
- Displays predicted sign letter and confidence score
- Visual confidence bar

### Real-time Hand Gesture Detection (`Handgesture.jsx`)
- Live video feed from webcam
- MediaPipe-based hand landmark detection
- Real-time ASL gesture recognition
- FPS counter and live indicator
- Hand skeleton visualization
- Instant gesture predictions

## 🔒 Security Considerations

- Never commit `.env` files to version control (use `.env.example` as template)
- Validate all user inputs before sending to backend
- Implement rate limiting in production
- Use HTTPS in production environments
- Configure proper CORS headers in backend to match frontend origin
- Restrict camera access permissions with user consent
- Never expose API keys or sensitive credentials in client-side code

## 🐛 Troubleshooting

### Development server won't start
- Ensure Node.js version is 18.x or higher
- Delete `node_modules` and `package-lock.json`, then run `npm install`
- Check if port 5173 is already in use

### API connection errors
- Verify backend server is running on the configured URL
- Check `VITE_API_BASE_URL` in `.env` file matches your backend
- Ensure CORS is properly configured in the FastAPI backend
- Restart dev server after changing `.env`
- Check browser console for detailed error messages
- Verify backend endpoints: `/slc-static/predict` and `/slc-realtime/predict`

### MediaPipe loading errors (real-time mode)
- Ensure internet connection (MediaPipe CDN scripts need to load)
- Check browser console for CDN loading issues
- Try clearing browser cache and hard refresh (Ctrl+Shift+R)
- Verify camera permissions are granted

### Build fails
- Clear Vite cache: `rm -rf node_modules/.vite`
- Check for ESLint errors: `npm run lint`

## 📝 Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📄 License

This project is part of the Sign Language Classifier application.

---

**Built with React + Vite**
