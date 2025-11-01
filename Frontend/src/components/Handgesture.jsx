import React, { useRef, useEffect, useState } from 'react';
import { Camera, StopCircle, Activity, Zap } from 'lucide-react';
import '../App.css';

const GestureRecognitionApp = () => {
  const videoRef = useRef(null);
  const overlayCanvasRef = useRef(null);
  const [isRunning, setIsRunning] = useState(false);
  const [prediction, setPrediction] = useState({ label: '-', confidence: 0 });
  const [error, setError] = useState('');
  const [fps, setFps] = useState(0);
  const [mediapipeLoaded, setMediapipeLoaded] = useState(false);
  const handsRef = useRef(null);
  const cameraRef = useRef(null);
  const streamRef = useRef(null);
  const lastFrameTime = useRef(Date.now());

  // Read API base URL from Vite env variables.
  // Create a `.env` file at project root with:
  // VITE_API_BASE_URL=http://127.0.0.1:8000
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';


  useEffect(() => {
    const loadMediaPipe = async () => {
      try {
        const handsScript = document.createElement('script');
        handsScript.src = 'https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js';
        handsScript.async = true;

        handsScript.onload = () => {
          const drawingScript = document.createElement('script');
          drawingScript.src = 'https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js';
          drawingScript.async = true;

          drawingScript.onload = () => {
            const cameraUtilsScript = document.createElement('script');
            cameraUtilsScript.src = 'https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js';
            cameraUtilsScript.async = true;

            cameraUtilsScript.onload = () => {
              console.log('✅ MediaPipe loaded successfully');
              setMediapipeLoaded(true);
            };

            document.body.appendChild(cameraUtilsScript);
          };

          document.body.appendChild(drawingScript);
        };

        document.body.appendChild(handsScript);
      } catch (err) {
        console.error('MediaPipe loading error:', err);
        setError('Failed to load MediaPipe: ' + err.message);
      }
    };

    loadMediaPipe();
  }, []);


  const initializeMediaPipe = () => {
    if (!window.Hands) return null;

    const hands = new window.Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    return hands;
  };


  const normalizeLandmarks = (landmarks) => {
    const x = landmarks.map((lm) => lm.x);
    const y = landmarks.map((lm) => lm.y);
    const cx = x.reduce((a, b) => a + b) / x.length;
    const cy = y.reduce((a, b) => a + b) / y.length;

    const centeredX = x.map((val) => val - cx);
    const centeredY = y.map((val) => val - cy);

    const rangeX = Math.max(...centeredX) - Math.min(...centeredX);
    const rangeY = Math.max(...centeredY) - Math.min(...centeredY);
    const maxRange = Math.max(rangeX, rangeY);

    const normalizedX = centeredX.map((val) => val / maxRange);
    const normalizedY = centeredY.map((val) => val / maxRange);

    const flattened = [];
    for (let i = 0; i < normalizedX.length; i++) {
      flattened.push(normalizedX[i], normalizedY[i]);
    }

    return flattened;
  };


  const drawHandSkeleton = (landmarks, canvasCtx, width, height) => {
    if (!landmarks || !window.drawConnectors || !window.drawLandmarks) return;
    canvasCtx.clearRect(0, 0, width, height);
    window.drawConnectors(canvasCtx, landmarks, window.HAND_CONNECTIONS, {
      color: '#00FF00',
      lineWidth: 2,
    });
    window.drawLandmarks(canvasCtx, landmarks, {
      color: '#FF0000',
      lineWidth: 1,
      radius: 3,
    });
  };

  const predictGesture = async (landmarks) => {
    try {
      const response = await fetch(`${API_BASE_URL}/slc-realtime/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ landmarks }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const result = await response.json();
      setPrediction(result);
      setError('');
    } catch (err) {
      console.error('Prediction error:', err);
      setError('Prediction failed: ' + err.message);
    }
  };

  
  const startDetection = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
      }

      handsRef.current = initializeMediaPipe();
      if (!handsRef.current) {
        setError('Failed to initialize MediaPipe Hands');
        return;
      }

      const overlayCanvas = overlayCanvasRef.current;
      const overlayCtx = overlayCanvas.getContext('2d');

      handsRef.current.onResults((results) => {
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
          const landmarks = results.multiHandLandmarks[0];
          drawHandSkeleton(landmarks, overlayCtx, overlayCanvas.width, overlayCanvas.height);
          const normalized = normalizeLandmarks(landmarks);
          predictGesture(normalized);
        } else {
          overlayCtx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
          setPrediction({ label: '-', confidence: 0 });
        }

        const now = Date.now();
        const diff = now - lastFrameTime.current;
        if (diff > 0) setFps(Math.round(1000 / diff));
        lastFrameTime.current = now;
      });

      const camera = new window.Camera(videoRef.current, {
        onFrame: async () => {
          await handsRef.current.send({ image: videoRef.current });
        },
        width: 640,
        height: 480,
      });
      camera.start();
      cameraRef.current = camera;
      setIsRunning(true);
      setError('');
    } catch (err) {
      console.error('Webcam error:', err);
      setError('Failed to start webcam: ' + err.message);
    }
  };


  const stopDetection = () => {
    if (cameraRef.current) {
      cameraRef.current.stop();
      cameraRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    if (handsRef.current) {
      handsRef.current.close();
      handsRef.current = null;
    }
    setIsRunning(false);
    setPrediction({ label: '-', confidence: 0 });
    setFps(0);
  };

  
  useEffect(() => {
    return () => stopDetection();
  }, []);

  const toggleDetection = () => {
    if (!mediapipeLoaded) {
      setError('MediaPipe is still loading. Please wait...');
      return;
    }
    if (isRunning) stopDetection();
    else startDetection();
  };

  return (
    <div className="app-container">
      <div className="app-wrapper">
        {/* Header */}
        <div className="app-header">
          <h1 className="app-title">
            <Activity className="app-title-icon" />
            Hand Gesture Recognition
          </h1>
          <p className="app-subtitle">Real-time ASL detection using MediaPipe & TensorFlow</p>
        </div>

        <div className="main-grid">
          {/* Main Video Feed */}
          <div className="video-section">
            <div className="video-container">
              <video ref={videoRef} autoPlay playsInline muted className="video-feed" />
              <canvas
                ref={overlayCanvasRef}
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  pointerEvents: 'none',
                  transform: 'scaleX(-1)',
                }}
              />

              {isRunning && (
                <div className="video-overlay-top">
                  <div className="live-indicator">
                    <div className="live-dot" />
                    <span className="live-text">LIVE</span>
                  </div>
                  <div className="fps-indicator">{fps} FPS</div>
                </div>
              )}

              {isRunning && prediction.label !== '-' && (
                <div className="prediction-overlay">
                  <div className="prediction-card">
                    <div className="prediction-content">
                      <div className="prediction-label-section">
                        <div className="prediction-label-title">Detected Gesture</div>
                        <div className="prediction-label-value">{prediction.label}</div>
                      </div>
                      <div className="prediction-confidence-section">
                        <div className="prediction-confidence-title">Confidence</div>
                        <div className="prediction-confidence-value">
                          {(prediction.confidence * 100).toFixed(1)}%
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

              {!isRunning && (
                <div className="video-placeholder">
                  <div className="placeholder-content">
                    <Camera className="placeholder-icon" />
                    <p className="placeholder-text">
                      {mediapipeLoaded ? 'Click Start to begin detection' : 'Loading MediaPipe...'}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Control Panel */}
          <div className="control-panel">
            <div className="control-card">
              <h2 className="control-card-title">
                <Zap className="control-icon" />
                Controls
              </h2>

              <button
                onClick={toggleDetection}
                disabled={!mediapipeLoaded && !isRunning}
                className={`control-button ${isRunning ? 'stop' : 'start'}`}
              >
                {isRunning ? (
                  <>
                    <StopCircle className="control-button-icon" />
                    Stop Detection
                  </>
                ) : (
                  <>
                    <Camera className="control-button-icon" />
                    {mediapipeLoaded ? 'Start Detection' : 'Loading...'}
                  </>
                )}
              </button>

              {error && (
                <div className="error-message">
                  <p className="error-text">{error}</p>
                </div>
              )}
            </div>

            <div className="control-card">
              <h2 className="control-card-title">Statistics</h2>
              <div className="stats-list">
                <div className="stat-item">
                  <span className="stat-label">Status</span>
                  <span className={`stat-value ${isRunning ? 'running' : 'stopped'}`}>
                    {isRunning ? 'Running' : 'Stopped'}
                  </span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">FPS</span>
                  <span className="stat-value fps">{fps}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Current Gesture</span>
                  <span className="stat-value gesture">{prediction.label}</span>
                </div>
              </div>
            </div>

            <div className="control-card">
              <h2 className="control-card-title">Instructions</h2>
              <ul className="instructions-list">
                <li className="instruction-item">
                  <span className="instruction-number">1.</span>
                  <span>Wait for MediaPipe to load completely</span>
                </li>
                <li className="instruction-item">
                  <span className="instruction-number">2.</span>
                  <span>Click "Start Detection" to activate camera</span>
                </li>
                <li className="instruction-item">
                  <span className="instruction-number">3.</span>
                  <span>Show hand gestures - green skeleton will appear</span>
                </li>
                <li className="instruction-item">
                  <span className="instruction-number">4.</span>
                  <span>View real-time predictions on screen</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GestureRecognitionApp;
