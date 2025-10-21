import React, { useState } from 'react';
import { Upload, RefreshCw, AlertCircle, ArrowLeft } from 'lucide-react';
import './App.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function SignLanguageClassifier() {
  const [imageUrl, setImageUrl] = useState('');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [predictionError, setPredictionError] = useState('');
  const [showResults, setShowResults] = useState(false);


  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
      if (!validTypes.includes(file.type)) {
        setUploadError('Invalid file type. Please upload PNG, JPG, or JPEG images only.');
        setUploadedImage(null);
        setUploadedFile(null);
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        setUploadError('File size exceeds 10MB. Please upload a smaller image.');
        setUploadedImage(null);
        setUploadedFile(null);
        return;
      }

      setUploadError('');
      setUploadedFile(file);

      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result);
        setPrediction(null);
        setPredictionError('');
      };
      reader.onerror = () => {
        setUploadError('Failed to read file. Please try again.');
      };
      reader.readAsDataURL(file);
    }
  };


  const handleUrlLoad = () => {
    if (!imageUrl.trim()) {
      setUploadError('Please enter a valid image URL.');
      return;
    }

    try {
      new URL(imageUrl);
    } catch {
      setUploadError('Invalid URL format. Please enter a valid image URL.');
      return;
    }

    setUploadError('');
    const img = new Image();

    img.onload = () => {
      setUploadedImage(imageUrl);
      setUploadedFile(null);
      setPrediction(null);
      setPredictionError('');
    };

    img.onerror = () => {
      setUploadError('Failed to load image from URL. Please check the URL and try again.');
      setUploadedImage(null);
    };

    img.src = imageUrl;
  };

  const handlePredict = async () => {
    if (!uploadedImage) return;

    setIsLoading(true);
    setPredictionError('');
    setShowResults(true);

    try {
      let response;

      if (uploadedFile) {
       
        const formData = new FormData();
        formData.append('file', uploadedFile);

        response = await fetch(`${API_BASE_URL}/slc/predict`, {
          method: 'POST',
          body: formData,
        });
      } else if (imageUrl) {
        
        response = await fetch(`${API_BASE_URL}/slc/predict/url`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image_url: imageUrl }),
        });
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        setPrediction({
          letter: data.letter,
          confidence: data.confidence,
        });
        setPredictionError('');
      } else {
        setPredictionError(data.error || 'Prediction failed. Please try again.');
        setPrediction(null);
      }
    } catch (error) {
      console.error('Prediction error:', error);
      setPredictionError(
        'Failed to connect to the prediction service. Please ensure the backend is running and try again.'
      );
      setPrediction(null);
    } finally {
      setIsLoading(false);
    }
  };

 
  const handleReset = () => {
    setUploadedImage(null);
    setUploadedFile(null);
    setPrediction(null);
    setImageUrl('');
    setIsLoading(false);
    setUploadError('');
    setPredictionError('');
    setShowResults(false);
  };

  const handleBackToUpload = () => {
    setShowResults(false);
    setPrediction(null);
    setPredictionError('');
  };

 
  return (
    <div className="slc-container">
      <div className="slc-wrapper">
        <div className="slc-header">
          <h1 className="slc-title">Sign Language Classifier</h1>
          <p className="slc-subtitle">Upload an image and detect the sign language letter</p>
        </div>

        <div className="slc-card">
      
          {!showResults && (
            <>
              <h2 className="slc-section-title">Upload Image</h2>

              <div className="slc-upload-section">
                <div className={`slc-upload-area ${uploadedImage ? 'slc-upload-success' : ''}`}>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileUpload}
                    className="slc-file-input"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="slc-upload-label">
                    {uploadedImage ? (
                      <div>
                        <img src={uploadedImage} alt="Uploaded preview" className="slc-preview-image" />
                        <p className="slc-upload-success-text">Image uploaded successfully!</p>
                        <p className="slc-upload-change-text">Click to change image</p>
                      </div>
                    ) : (
                      <>
                        <Upload className="slc-upload-icon" />
                        <p className="slc-upload-title">Click to upload an image</p>
                        <p className="slc-upload-subtitle">PNG, JPG, JPEG up to 10MB</p>
                      </>
                    )}
                  </label>
                </div>
              </div>

              <div className="slc-divider">
                <div className="slc-divider-line"></div>
                <span className="slc-divider-text">OR</span>
              </div>

              <div className="slc-url-section">
                <input
                  type="text"
                  value={imageUrl}
                  onChange={(e) => setImageUrl(e.target.value)}
                  placeholder="Enter image URL"
                  className="slc-url-input"
                />
                <button onClick={handleUrlLoad} className="slc-url-button">
                  Load from URL
                </button>
              </div>

              {uploadError && (
                <div className="slc-error-box">
                  <div className="slc-error-content">
                    <AlertCircle className="slc-error-icon" />
                    <p className="slc-error-text">{uploadError}</p>
                  </div>
                </div>
              )}

              <div className="slc-button-group">
                <button
                  onClick={handlePredict}
                  disabled={!uploadedImage || isLoading}
                  className={`slc-predict-button ${
                    !uploadedImage || isLoading ? 'slc-button-disabled' : ''
                  }`}
                >
                  Predict Letter
                </button>
                <button onClick={handleReset} className="slc-reset-button">
                  <RefreshCw className="slc-reset-icon" />
                </button>
              </div>
            </>
          )}

      
          {showResults && (
            <>
              <button onClick={handleBackToUpload} className="slc-back-button">
                <ArrowLeft className="slc-back-icon" />
                Back to Upload
              </button>

              <h2 className="slc-section-title">Prediction Result</h2>

              {uploadedImage && (
                <div className="slc-result-image-section">
                  <h3 className="slc-result-image-title">Analyzed Image</h3>
                  <div className="slc-result-image-container">
                    <img src={uploadedImage} alt="Analyzed" className="slc-result-image" />
                  </div>
                </div>
              )}

              {isLoading && (
                <div className="slc-loading-container">
                  <div className="slc-spinner"></div>
                  <p className="slc-loading-text">Analyzing image...</p>
                </div>
              )}

              {predictionError && !isLoading && (
                <div className="slc-prediction-error">
                  <div className="slc-prediction-error-header">
                    <AlertCircle className="slc-prediction-error-icon" />
                    <div>
                      <h3 className="slc-prediction-error-title">Prediction Error</h3>
                      <p className="slc-prediction-error-text">{predictionError}</p>
                    </div>
                  </div>
                  <button onClick={handlePredict} className="slc-retry-button">
                    Try Again
                  </button>
                </div>
              )}

              {prediction && !isLoading && (
                <div className="slc-prediction-success">
                  <div className="slc-prediction-letter-section">
                    <p className="slc-prediction-label">Detected Letter</p>
                    <div className="slc-prediction-letter">{prediction.letter}</div>
                  </div>
                  <div className="slc-confidence-box">
                    <div className="slc-confidence-header">
                      <span className="slc-confidence-label">Confidence</span>
                      <span className="slc-confidence-value">{prediction.confidence}%</span>
                    </div>
                    <div className="slc-confidence-bar-bg">
                      <div
                        className="slc-confidence-bar"
                        style={{ width: `${prediction.confidence}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="slc-prediction-footer">
                    <p className="slc-prediction-footer-text">
                      American Sign Language (ASL) alphabet detected
                    </p>
                  </div>
                </div>
              )}

              <div className="slc-button-group">
                <button onClick={handleBackToUpload} className="slc-upload-another-button">
                  Upload Another Image
                </button>
                <button onClick={handleReset} className="slc-reset-button">
                  <RefreshCw className="slc-reset-icon" />
                </button>
              </div>
            </>
          )}
        </div>

        <div className="slc-footer">
          <p>Supports American Sign Language (ASL) alphabet recognition</p>
        </div>
      </div>
    </div>
  );
}
