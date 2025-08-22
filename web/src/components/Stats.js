import React from 'react';
import { motion } from 'framer-motion';
import { FiZap, FiTrendingUp, FiClock, FiTarget } from 'react-icons/fi';

const Stats = ({ stats }) => {
  const { totalDetections, averageConfidence, processingTime } = stats;

  const statItems = [
    {
      icon: FiTarget,
      label: 'Total Detections',
      value: totalDetections,
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: FiTrendingUp,
      label: 'Average Confidence',
      value: `${(averageConfidence * 100).toFixed(1)}%`,
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: FiClock,
      label: 'Processing Time',
      value: `${processingTime}ms`,
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: FiZap,
      label: 'Model Performance',
      value: 'YOLOv10 Nano',
      color: 'from-orange-500 to-red-500'
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20"
    >
      <h3 className="text-xl font-semibold text-white mb-6 text-center">
        Performance Statistics
      </h3>
      
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statItems.map((item, index) => (
          <motion.div
            key={item.label}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            className="text-center"
          >
            <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-r ${item.color} mb-3`}>
              <item.icon className="text-white text-xl" />
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {item.value}
            </div>
            <div className="text-sm text-white/60">
              {item.label}
            </div>
          </motion.div>
        ))}
      </div>
      
      <div className="mt-6 pt-6 border-t border-white/20">
        <div className="text-center">
          <p className="text-white/60 text-sm">
            Powered by YOLOv10 - State of the art object detection
          </p>
          <p className="text-white/40 text-xs mt-1">
            Real-time AI processing with high accuracy
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default Stats;
