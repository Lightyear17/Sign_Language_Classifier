# Sign Language Classifier - Frontend

A modern React frontend application for classifying American Sign Language (ASL) alphabet letters from images using a trained CNN model.

## 🛠 Tech Stack

- **Framework**: React 19.1.1
- **Build Tool**: Vite 7.1.7
- **UI Icons**: Lucide React 0.546.0
- **Styling**: Custom CSS
- **HTTP Client**: Fetch API

## ✨ Features

- **Multiple Upload Methods**: 
  - Direct file upload (drag & drop interface)
  - Load images from URL
- **Real-time Predictions**: Instant ASL letter recognition
- **Visual Feedback**: 
  - Image preview
  - Confidence score visualization
  - Loading states and error handling
- **Responsive Design**: Clean and intuitive user interface
- **Error Handling**: Comprehensive validation and user-friendly error messages

## 📁 Project Structure

```
Frontend/
├── src/
│   ├── App.jsx                     # Main application component
│   ├── App.css                     # Application styles
│   ├── main.jsx                    # Application entry point
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
   ```bash
   # Copy example.env to .env
   cp .env.example .env
   
   # Edit .env with your API URL
   # Example:
   VITE_API_BASE_URL=http://localhost:8000
   ```

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

- **File Upload**: `POST /slc/predict`
- **URL Upload**: `POST /slc/predict/url`

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |

⚠️ **Important**: The `VITE_` prefix is required for Vite to expose the variable to your client-side code.

## 🎨 Features Overview

### Image Upload
- Supports PNG, JPG, JPEG formats
- Maximum file size: 10MB
- Real-time file validation
- Image preview before prediction

### URL Loading
- Paste any valid image URL
- Automatic image validation
- Error handling for invalid/unreachable URLs

### Prediction Results
- Displays detected ASL letter
- Shows confidence percentage
- Visual confidence bar
- Option to analyze another image

## 🔒 Security Considerations

- Never commit `.env` files to version control
- Validate all user inputs before sending to backend
- Implement rate limiting for production
- Use HTTPS in production environments
- Sanitize image URLs to prevent XSS attacks

## 🐛 Troubleshooting

### Development server won't start
- Ensure Node.js version is 18.x or higher
- Delete `node_modules` and `package-lock.json`, then run `npm install`
- Check if port 5173 is already in use

### API connection errors
- Verify backend server is running
- Check `VITE_API_BASE_URL` in `.env` file
- Ensure CORS is properly configured in backend
- Restart dev server after changing `.env`

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
