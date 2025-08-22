import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FiEye, FiEyeOff, FiTarget, FiTrendingUp, FiClock } from 'react-icons/fi';

const DetectionResults = ({ results }) => {
  const [showAnnotated, setShowAnnotated] = useState(true);

  const { detections = [], summary = {}, annotated_image, original_image } = results;

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-400';
    if (confidence >= 0.6) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getConfidenceBarColor = (confidence) => {
    if (confidence >= 0.8) return 'bg-green-500';
    if (confidence >= 0.6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="space-y-6">
      {/* Image Display */}
      <div className="relative">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">Detected Image</h3>
          <button
            onClick={() => setShowAnnotated(!showAnnotated)}
            className="flex items-center space-x-2 text-white/70 hover:text-white transition-colors"
          >
            {showAnnotated ? <FiEyeOff className="text-sm" /> : <FiEye className="text-sm" />}
            <span className="text-sm">
              {showAnnotated ? 'Show Original' : 'Show Annotated'}
            </span>
          </button>
        </div>
        
        <motion.div
          key={showAnnotated ? 'annotated' : 'original'}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
          className="rounded-lg overflow-hidden bg-white/5 border border-white/20"
        >
          <img
            src={showAnnotated && annotated_image 
              ? `data:image/jpeg;base64,${annotated_image}` 
              : `data:image/jpeg;base64,${original_image}`
            }
            alt="Detection Result"
            className="w-full h-auto max-h-96 object-contain"
          />
        </motion.div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white/10 rounded-lg p-4 text-center"
        >
          <FiTarget className="text-2xl text-white mx-auto mb-2" />
          <div className="text-2xl font-bold text-white">{detections.length}</div>
          <div className="text-sm text-white/60">Objects Found</div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white/10 rounded-lg p-4 text-center"
        >
          <FiTrendingUp className="text-2xl text-white mx-auto mb-2" />
          <div className="text-2xl font-bold text-white">
            {detections.length > 0 
              ? (detections.reduce((sum, det) => sum + det.confidence, 0) / detections.length * 100).toFixed(1)
              : '0'
            }%
          </div>
          <div className="text-sm text-white/60">Avg Confidence</div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white/10 rounded-lg p-4 text-center"
        >
          <FiClock className="text-2xl text-white mx-auto mb-2" />
          <div className="text-2xl font-bold text-white">
            {summary.processing_time || '~1-2s'}
          </div>
          <div className="text-sm text-white/60">Processing Time</div>
        </motion.div>
      </div>

      {/* Detections List */}
      {detections.length > 0 ? (
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Detected Objects</h3>
          <div className="space-y-3 max-h-64 overflow-y-auto">
            {detections.map((detection, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white/10 rounded-lg p-4 border border-white/20"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                    <div>
                      <div className="font-medium text-white capitalize">
                        {detection.label}
                      </div>
                      <div className="text-sm text-white/60">
                        Confidence: {detection.confidence.toFixed(3)}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <div className="w-20 bg-white/20 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${getConfidenceBarColor(detection.confidence)}`}
                        style={{ width: `${detection.confidence * 100}%` }}
                      ></div>
                    </div>
                    <span className={`text-sm font-medium ${getConfidenceColor(detection.confidence)}`}>
                      {(detection.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
                
                <div className="mt-2 text-xs text-white/40">
                  BBox: [{detection.bbox[0].toFixed(1)}, {detection.bbox[1].toFixed(1)}, {detection.bbox[2].toFixed(1)}, {detection.bbox[3].toFixed(1)}]
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-8"
        >
          <div className="text-6xl text-white/30 mb-4">🔍</div>
          <p className="text-white/60">No objects detected in this image</p>
          <p className="text-sm text-white/40 mt-2">
            Try uploading a different image with more prominent objects
          </p>
        </motion.div>
      )}
    </div>
  );
};

export default DetectionResults;
