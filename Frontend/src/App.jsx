import React, { useState } from 'react';
import GestureRecognitionApp from './components/Handgesture';
import StaticGesture from './components/Staticgesture';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('realtime');

  return (
    <div className="main-app">
      {/* Top Navigation Tabs */}
      <div className="tab-bar">
        <button
          className={`tab-button ${activeTab === 'realtime' ? 'active' : ''}`}
          onClick={() => setActiveTab('realtime')}
        >
          🎥 Realtime Detection
        </button>
        <button
          className={`tab-button ${activeTab === 'static' ? 'active' : ''}`}
          onClick={() => setActiveTab('static')}
        >
          🖼️ Static Image Detection
        </button>
     
      </div>

      {/* Active Component */}
      <div className="tab-content">
        {activeTab === 'realtime' && <GestureRecognitionApp />}
        {activeTab === 'static' && <StaticGesture />}
       
      </div>
    </div>
  );
}