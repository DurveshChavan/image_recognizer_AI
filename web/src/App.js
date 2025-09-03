import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiUpload, FiEye, FiZap, FiCheckCircle, FiAlertCircle, FiLoader } from 'react-icons/fi';
import ImageUpload from './components/ImageUpload';
import DetectionResults from './components/DetectionResults';
import Header from './components/Header';
import Stats from './components/Stats';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    totalDetections: 0,
    averageConfidence: 0,
    processingTime: 0
  });

  const handleImageUpload = async (file) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const startTime = Date.now();
      // Call deployed Flask backend
              const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://your-app-name.onrender.com';
      const response = await fetch(`${backendUrl}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      const endTime = Date.now();

      if (response.ok) {
        setResults(data);
        setStats({
          totalDetections: data.detections?.length || 0,
          averageConfidence: data.detections?.length > 0 
            ? data.detections.reduce((sum, det) => sum + det.confidence, 0) / data.detections.length 
            : 0,
          processingTime: endTime - startTime
        });
      } else {
        setError(data.error || 'Failed to process image');
      }
    } catch (err) {
      setError('Network error. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        <Header />
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
          {/* Left Panel - Upload */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20"
          >
            <div className="flex items-center mb-6">
              <FiUpload className="text-2xl text-white mr-3" />
              <h2 className="text-2xl font-semibold text-white">Upload Image</h2>
            </div>
            
            <ImageUpload 
              onUpload={handleImageUpload}
              isLoading={isLoading}
            />
          </motion.div>

          {/* Right Panel - Results */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20"
          >
            <div className="flex items-center mb-6">
              <FiEye className="text-2xl text-white mr-3" />
              <h2 className="text-2xl font-semibold text-white">Detection Results</h2>
            </div>
            
            <AnimatePresence mode="wait">
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex flex-col items-center justify-center py-12"
                >
                  <FiLoader className="text-4xl text-white animate-spin mb-4" />
                  <p className="text-white text-lg">Processing image with YOLOv10...</p>
                </motion.div>
              )}

              {error && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="bg-red-500/20 border border-red-400/30 rounded-lg p-4"
                >
                  <div className="flex items-center">
                    <FiAlertCircle className="text-red-400 text-xl mr-3" />
                    <p className="text-red-200">{error}</p>
                  </div>
                </motion.div>
              )}

              {results && !isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                >
                  <DetectionResults results={results} />
                </motion.div>
              )}

              {!results && !isLoading && !error && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-12"
                >
                  <FiEye className="text-6xl text-white/50 mx-auto mb-4" />
                  <p className="text-white/70 text-lg">
                    Upload an image to see detection results
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>

        {/* Stats Section */}
        {results && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="mt-8"
          >
            <Stats stats={stats} />
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default App;
