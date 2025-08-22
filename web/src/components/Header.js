import React from 'react';
import { motion } from 'framer-motion';
import { FiZap, FiGithub, FiLinkedin } from 'react-icons/fi';

const Header = () => {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="text-center"
    >
      <div className="flex items-center justify-center mb-4">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="bg-gradient-to-r from-yellow-400 to-orange-500 p-3 rounded-full mr-4"
        >
          <FiZap className="text-2xl text-white" />
        </motion.div>
        <h1 className="text-5xl font-bold text-white">
          YOLOv10
        </h1>
      </div>
      
      <p className="text-xl text-white/80 mb-6 max-w-2xl mx-auto">
        Advanced AI-powered object detection using the latest YOLOv10 model. 
        Upload any image and let our AI identify objects with high accuracy.
      </p>
      
      <div className="flex items-center justify-center space-x-6 text-white/60">
        <motion.a
          href="https://github.com/DurveshChavan/image_recognizer_AI"
          target="_blank"
          rel="noopener noreferrer"
          whileHover={{ scale: 1.1, color: "white" }}
          className="flex items-center space-x-2 hover:text-white transition-colors"
        >
          <FiGithub className="text-xl" />
          <span>GitHub</span>
        </motion.a>
        <motion.a
          href="https://www.linkedin.com/in/durvesh-chavan/"
          target="_blank"
          rel="noopener noreferrer"
          whileHover={{ scale: 1.1, color: "white" }}
          className="flex items-center space-x-2 hover:text-white transition-colors"
        >
          <FiLinkedin className="text-xl" />
          <span>LinkedIn</span>
        </motion.a>
      </div>
    </motion.header>
  );
};

export default Header;
