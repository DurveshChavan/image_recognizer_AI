import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { FiUpload, FiImage, FiX } from 'react-icons/fi';

const ImageUpload = ({ onUpload, isLoading }) => {
  const [preview, setPreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      // Create preview
      const reader = new FileReader();
      reader.onload = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
      
      // Upload file
      onUpload(file);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff']
    },
    multiple: false,
    disabled: isLoading
  });

  const clearPreview = () => {
    setPreview(null);
  };

  return (
    <div className="space-y-6">
      {/* Drop Zone */}
      <motion.div
        {...getRootProps()}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300
          ${isDragActive || dragActive 
            ? 'border-white/60 bg-white/10' 
            : 'border-white/30 hover:border-white/50 hover:bg-white/5'
          }
          ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
        onDragEnter={() => setDragActive(true)}
        onDragLeave={() => setDragActive(false)}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          <motion.div
            animate={{ 
              scale: isDragActive ? 1.1 : 1,
              rotate: isDragActive ? 5 : 0
            }}
            transition={{ duration: 0.2 }}
            className="mx-auto w-16 h-16 bg-white/10 rounded-full flex items-center justify-center"
          >
            {isDragActive ? (
              <FiUpload className="text-2xl text-white" />
            ) : (
              <FiImage className="text-2xl text-white" />
            )}
          </motion.div>
          
          <div>
            <p className="text-lg font-medium text-white mb-2">
              {isDragActive ? 'Drop your image here' : 'Drag & drop your image here'}
            </p>
            <p className="text-white/60">
              or click to browse files
            </p>
          </div>
          
          <div className="text-sm text-white/40">
            Supports: JPG, PNG, GIF, BMP, TIFF
          </div>
        </div>
      </motion.div>

      {/* Preview */}
      {preview && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative"
        >
          <div className="relative rounded-lg overflow-hidden bg-white/5 border border-white/20">
            <img 
              src={preview} 
              alt="Preview" 
              className="w-full h-auto max-h-96 object-contain"
            />
            <button
              onClick={clearPreview}
              className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full transition-colors"
            >
              <FiX className="text-sm" />
            </button>
          </div>
        </motion.div>
      )}

      {/* Loading State */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-4"
        >
          <div className="inline-flex items-center space-x-2 text-white">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            <span>Processing image...</span>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default ImageUpload;
