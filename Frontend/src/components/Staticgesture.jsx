import React, { useState } from 'react';
import { Upload, Image, RefreshCw, AlertCircle } from 'lucide-react';
import '../App.css';

// Read API base URL from Vite environment variables.
// Create a `.env` file at project root with a line like:
// VITE_API_BASE_URL=http://127.0.0.1:8000
// Vite exposes env vars prefixed with VITE_ via `import.meta.env`.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export default function StaticGesture() {
  const [imagePreview, setImagePreview] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
      setError('Invalid file type. Please upload PNG or JPG images.');
      return;
    }

    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
      setImageFile(file);
      setError('');
      setPrediction(null);
    };
    reader.readAsDataURL(file);
  };

 
  const handleUrlChange = (e) => {
    setImageUrl(e.target.value);
    setPrediction(null);
  };

  const handleLoadUrlImage = () => {
    if (!imageUrl.trim()) {
      setError('Please enter a valid image URL.');
      return;
    }
    setImagePreview(imageUrl);
    setImageFile(null);
    setError('');
  };

  
  const handlePredict = async () => {
    if (!imagePreview) {
      setError('Please upload or load an image first.');
      return;
    }

    setIsLoading(true);
    setError('');
    setPrediction(null);

    try {
      let response;

      if (imageFile) {
        // Upload file for prediction
        const formData = new FormData();
        formData.append('file', imageFile);

        response = await fetch(`${API_BASE_URL}/slc-static/predict`, {
          method: 'POST',
          body: formData,
        });
      } else if (imageUrl) {
        // URL-based prediction is not yet supported by the backend
        setError('URL-based prediction is currently not supported. Please upload an image file instead.');
        setIsLoading(false);
        return;
      }

      if (!response.ok) throw new Error(`HTTP error! Status ${response.status}`);

      const result = await response.json();
      setPrediction(result);
    } catch (err) {
      setError('Prediction failed: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

 
  const handleClear = () => {
    setImagePreview('');
    setImageFile(null);
    setImageUrl('');
    setPrediction(null);
    setError('');
  };

  return (
    <div className="app-container">
      <div className="app-wrapper">
        <div className="app-header">
          <h1 className="app-title">
            <Image className="app-title-icon" />
            Static Hand Gesture Recognition
          </h1>
          <p className="app-subtitle">
            Upload an image or provide a URL to detect the sign language gesture
          </p>
        </div>

        <div className="main-grid">
          <div className="video-section">
            <div className="video-container upload-box">
              {!imagePreview ? (
                <label className="upload-placeholder">
                  <Upload className="placeholder-icon" />
                  <p className="placeholder-text">Click or drag to upload an image</p>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileUpload}
                    className="hidden-file-input"
                  />
                </label>
              ) : (
                <div className="uploaded-image-container">
                  <img src={imagePreview} alt="Uploaded preview" className="uploaded-image" />
                </div>
              )}

              {prediction && (
                <div className="prediction-overlay static">
                  <div className="prediction-card">
                    <div className="prediction-content">
                      <div className="prediction-label-section">
                        <div className="prediction-label-title">Predicted Gesture</div>
                        <div className="prediction-label-value">{prediction.label}</div>
                      </div>
                      <div className="prediction-confidence-section">
                        <div className="prediction-confidence-title">Confidence</div>
                        <div className="prediction-confidence-value">
                          {(prediction.confidence * 100).toFixed(2)}%
                        </div>
                      </div>
                    </div>
                    <div className="confidence-bar-container">
                      <div
                        className="confidence-bar-fill"
                        style={{ width: `${prediction.confidence * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="control-panel">
            <div className="control-card">
              <h2 className="control-card-title">Image Input</h2>
              <input
                type="text"
                placeholder="Enter image URL..."
                value={imageUrl}
                onChange={handleUrlChange}
                className="url-input"
              />
              <button onClick={handleLoadUrlImage} className="control-button start">
                Load Image
              </button>

              <div className="button-row">
                <button
                  onClick={handlePredict}
                  disabled={isLoading || !imagePreview}
                  className={`control-button ${isLoading ? 'disabled' : 'start'}`}
                >
                  {isLoading ? 'Predicting...' : 'Predict'}
                </button>
                <button onClick={handleClear} className="control-button stop">
                  <RefreshCw className="control-button-icon" />
                  Clear
                </button>
              </div>

              {error && (
                <div className="error-message">
                  <AlertCircle className="error-icon" />
                  <p className="error-text">{error}</p>
                </div>
              )}
            </div>

            <div className="control-card">
              <h2 className="control-card-title">Instructions</h2>
              <ul className="instructions-list">
                <li className="instruction-item">
                  <span className="instruction-number">1.</span>
                  <span>Upload an image or paste a valid URL.</span>
                </li>
                <li className="instruction-item">
                  <span className="instruction-number">2.</span>
                  <span>Click “Predict” to analyze the gesture.</span>
                </li>
                <li className="instruction-item">
                  <span className="instruction-number">3.</span>
                  <span>View the predicted sign and confidence below.</span>
                </li>
                <li className="instruction-item">
                  <span className="instruction-number">4.</span>
                  <span>Use “Clear” to reset and upload again.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
