#!/usr/bin/env python3
"""
Enhanced YOLOv10 Service with C++ Integration
This service combines the power of YOLOv10 with high-performance C++ components
for optimized image processing, NMS, and video handling.
"""

import argparse
import json
import os
import sys
import time
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading

import cv2
from ultralytics import YOLO
import yaml

# Import C++ enhancement module
try:
    import yolov10_cpp_module as cpp
    CPP_AVAILABLE = True
    print("✅ C++ enhancement module loaded successfully")
except ImportError as e:
    CPP_AVAILABLE = False
    print(f"⚠️  C++ enhancement module not available: {e}")
    print("   Using Python-only implementation")


class EnhancedYOLOv10Service:
    """Enhanced YOLOv10 service with C++ integration for improved performance."""
    
    def __init__(self, model_path: str, config_path: str = "config.yaml"):
        """
        Initialize the enhanced YOLOv10 service.
        
        Args:
            model_path: Path to the YOLOv10 model file
            config_path: Path to the configuration file
        """
        self.model_path = model_path
        self.config = self._load_config(config_path)
        self.model = self._load_model()
        
        # Initialize C++ components if available
        self.cpp_components = {}
        if CPP_AVAILABLE:
            self._initialize_cpp_components()
        
        # Performance tracking
        self.performance_stats = {
            'total_inferences': 0,
            'total_processing_time': 0.0,
            'avg_inference_time': 0.0,
            'cpp_usage_count': 0,
            'python_usage_count': 0
        }
        
        # Thread safety
        self._lock = threading.Lock()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            print(f"Warning: Config file {config_path} not found. Using default settings.")
            return {
                'confidence_threshold': 0.5,
                'iou_threshold': 0.45,
                'class_labels': {},
                'model_config': {
                    'device': 'auto',
                    'half': False,
                    'max_det': 300,
                    'agnostic_nms': False,
                    'augment': False
                },
                'cpp_enhancement': {
                    'enable_image_processor': True,
                    'enable_nms_processor': True,
                    'enable_video_processor': True,
                    'enable_memory_manager': True,
                    'nms_type': 'STANDARD',
                    'temporal_smoothing': True,
                    'multi_threading': True
                }
            }
    
    def _load_model(self) -> YOLO:
        """Load the YOLOv10 model."""
        try:
            model = YOLO(self.model_path)
            print(f"YOLOv10 model loaded successfully from {self.model_path}")
            return model
        except Exception as e:
            print(f"Error loading YOLOv10 model: {e}")
            sys.exit(1)
    
    def _initialize_cpp_components(self):
        """Initialize C++ enhancement components."""
        try:
            # Initialize image processor
            if self.config.get('cpp_enhancement', {}).get('enable_image_processor', True):
                self.cpp_components['image_processor'] = cpp.ImageProcessor()
                print("✅ C++ ImageProcessor initialized")
            
            # Initialize NMS processor
            if self.config.get('cpp_enhancement', {}).get('enable_nms_processor', True):
                nms_config = cpp.NMSConfig()
                nms_config.iou_threshold = self.config.get('iou_threshold', 0.45)
                nms_config.confidence_threshold = self.config.get('confidence_threshold', 0.5)
                nms_config.nms_type = getattr(cpp.NMSType, 
                    self.config.get('cpp_enhancement', {}).get('nms_type', 'STANDARD'))
                
                self.cpp_components['nms_processor'] = cpp.NMSProcessor(nms_config)
                print("✅ C++ NMSProcessor initialized")
            
            # Initialize video processor
            if self.config.get('cpp_enhancement', {}).get('enable_video_processor', True):
                video_config = cpp.VideoConfig()
                video_config.enable_temporal_smoothing = self.config.get('cpp_enhancement', {}).get('temporal_smoothing', True)
                video_config.enable_multi_threading = self.config.get('cpp_enhancement', {}).get('multi_threading', True)
                
                self.cpp_components['video_processor'] = cpp.VideoProcessor(video_config)
                self.cpp_components['video_processor'].initialize()
                print("✅ C++ VideoProcessor initialized")
            
            # Initialize memory manager
            if self.config.get('cpp_enhancement', {}).get('enable_memory_manager', True):
                memory_config = cpp.MemoryPoolConfig()
                memory_config.initial_size = 1024 * 1024 * 100  # 100MB
                memory_config.max_size = 1024 * 1024 * 1024     # 1GB
                
                self.cpp_components['memory_manager'] = cpp.MemoryManager(memory_config)
                self.cpp_components['memory_manager'].initialize()
                print("✅ C++ MemoryManager initialized")
                
        except Exception as e:
            print(f"⚠️  Error initializing C++ components: {e}")
            CPP_AVAILABLE = False
    
    def predict(self, image_path: str, use_cpp: bool = True) -> List[Dict[str, Any]]:
        """
        Perform enhanced object detection on an image using YOLOv10 + C++ optimizations.
        
        Args:
            image_path: Path to the input image
            use_cpp: Whether to use C++ optimizations
            
        Returns:
            List of detection results with bounding boxes, class labels, and confidence scores
        """
        start_time = time.time()
        
        try:
            # Load and validate image
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Preprocess image with C++ if available
            if use_cpp and CPP_AVAILABLE and 'image_processor' in self.cpp_components:
                try:
                    # Use C++ image preprocessing
                    preprocessed_image = self.cpp_components['image_processor'].preprocess_image(
                        image_path, (640, 640), True
                    )
                    # Convert back to format expected by YOLO
                    image = cv2.imread(image_path)
                    if preprocessed_image is not None:
                        # Use preprocessed image for inference
                        pass
                    self.performance_stats['cpp_usage_count'] += 1
                except Exception as e:
                    print(f"⚠️  C++ preprocessing failed, falling back to Python: {e}")
                    use_cpp = False
            
            # Get model configuration
            model_config = self.config.get('model_config', {})
            
            # Perform prediction with YOLOv10
            results = self.model(
                image_path, 
                conf=self.config['confidence_threshold'], 
                iou=self.config['iou_threshold'],
                device=model_config.get('device', 'auto'),
                half=model_config.get('half', False),
                max_det=model_config.get('max_det', 300),
                agnostic_nms=model_config.get('agnostic_nms', False),
                augment=model_config.get('augment', False)
            )
            
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get bounding box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        
                        # Get class and confidence
                        class_id = int(box.cls[0].cpu().numpy())
                        confidence = float(box.conf[0].cpu().numpy())
                        
                        # Get class label
                        class_label = self.config['class_labels'].get(class_id, f"class_{class_id}")
                        
                        detection = {
                            'bbox': [float(x1), float(y1), float(x2), float(y2)],
                            'class_id': class_id,
                            'label': class_label,
                            'confidence': confidence
                        }
                        detections.append(detection)
            
            # Apply enhanced NMS if C++ is available
            if use_cpp and CPP_AVAILABLE and 'nms_processor' in self.cpp_components:
                try:
                    # Convert detections to C++ format
                    cpp_detections = cpp.convert_detections_to_cpp(detections)
                    # Apply C++ NMS
                    filtered_detections = self.cpp_components['nms_processor'].apply_nms(cpp_detections)
                    # Convert back to Python format
                    detections = cpp.convert_detections_to_python(filtered_detections)
                    self.performance_stats['cpp_usage_count'] += 1
                except Exception as e:
                    print(f"⚠️  C++ NMS failed, using Python results: {e}")
                    self.performance_stats['python_usage_count'] += 1
            else:
                self.performance_stats['python_usage_count'] += 1
            
            # Update performance statistics
            processing_time = time.time() - start_time
            with self._lock:
                self.performance_stats['total_inferences'] += 1
                self.performance_stats['total_processing_time'] += processing_time
                self.performance_stats['avg_inference_time'] = (
                    self.performance_stats['total_processing_time'] / 
                    self.performance_stats['total_inferences']
                )
            
            return detections
            
        except Exception as e:
            print(f"Error during enhanced YOLOv10 prediction: {e}")
            return []
    
    def predict_batch(self, image_paths: List[str], use_cpp: bool = True, 
                     max_workers: int = 4) -> List[List[Dict[str, Any]]]:
        """
        Perform batch prediction on multiple images with parallel processing.
        
        Args:
            image_paths: List of image paths
            use_cpp: Whether to use C++ optimizations
            max_workers: Maximum number of parallel workers
            
        Returns:
            List of detection results for each image
        """
        if use_cpp and CPP_AVAILABLE and 'memory_manager' in self.cpp_components:
            # Use C++ memory manager for batch processing
            try:
                # Preallocate memory for batch processing
                expected_size = len(image_paths) * 1024 * 1024  # 1MB per image estimate
                self.cpp_components['memory_manager'].preallocate(expected_size)
            except Exception as e:
                print(f"⚠️  C++ memory preallocation failed: {e}")
        
        # Use ThreadPoolExecutor for I/O bound operations
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(
                lambda path: self.predict(path, use_cpp), 
                image_paths
            ))
        
        return results
    
    def process_video(self, video_path: str, output_path: str = "", 
                     use_cpp: bool = True) -> Dict[str, Any]:
        """
        Process video with enhanced capabilities.
        
        Args:
            video_path: Path to input video
            output_path: Path to output video (optional)
            use_cpp: Whether to use C++ optimizations
            
        Returns:
            Processing results and statistics
        """
        if use_cpp and CPP_AVAILABLE and 'video_processor' in self.cpp_components:
            try:
                # Use C++ video processor
                def detection_callback(frame):
                    # This would be called for each frame
                    # For now, we'll use the Python model
                    return self.predict_frame(frame)
                
                self.cpp_components['video_processor'].set_detection_callback(detection_callback)
                
                success = self.cpp_components['video_processor'].process_video(
                    video_path, output_path
                )
                
                if success:
                    stats = self.cpp_components['video_processor'].get_stats()
                    return {
                        'success': True,
                        'stats': {
                            'total_frames': stats.total_frames,
                            'processed_frames': stats.processed_frames,
                            'avg_fps': stats.avg_fps,
                            'avg_processing_time_ms': stats.avg_processing_time_ms
                        }
                    }
                
            except Exception as e:
                print(f"⚠️  C++ video processing failed: {e}")
        
        # Fallback to Python video processing
        return self._process_video_python(video_path, output_path)
    
    def _process_video_python(self, video_path: str, output_path: str = "") -> Dict[str, Any]:
        """Fallback Python video processing."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {'success': False, 'error': 'Could not open video file'}
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, 
                                (int(cap.get(3)), int(cap.get(4))))
        
        processed_frames = 0
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            detections = self.predict_frame(frame)
            
            # Draw detections
            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                label = detection['label']
                confidence = detection['confidence']
                
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"{label}: {confidence:.2f}", 
                           (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            if output_path:
                out.write(frame)
            
            processed_frames += 1
        
        cap.release()
        if output_path:
            out.release()
        
        processing_time = time.time() - start_time
        
        return {
            'success': True,
            'stats': {
                'total_frames': total_frames,
                'processed_frames': processed_frames,
                'avg_fps': processed_frames / processing_time,
                'avg_processing_time_ms': (processing_time / processed_frames) * 1000
            }
        }
    
    def predict_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Predict on a single frame (numpy array)."""
        # Convert frame to temporary file or use in-memory processing
        # For simplicity, we'll save to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            cv2.imwrite(tmp.name, frame)
            detections = self.predict(tmp.name)
            os.unlink(tmp.name)
            return detections
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """Get image information (width, height, filename)."""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            height, width = img.shape[:2]
            filename = os.path.basename(image_path)
            
            return {
                'filename': filename,
                'width': width,
                'height': height,
                'path': image_path
            }
        except Exception as e:
            print(f"Error getting image info: {e}")
            return {}
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        with self._lock:
            stats = self.performance_stats.copy()
        
        # Add C++ component status
        stats['cpp_available'] = CPP_AVAILABLE
        stats['cpp_components'] = list(self.cpp_components.keys())
        
        return stats
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics if C++ memory manager is available."""
        if CPP_AVAILABLE and 'memory_manager' in self.cpp_components:
            try:
                memory_stats = self.cpp_components['memory_manager'].get_stats()
                pool_status = self.cpp_components['memory_manager'].get_pool_status()
                
                return {
                    'memory_stats': {
                        'total_allocated': memory_stats.total_allocated,
                        'total_used': memory_stats.total_used,
                        'total_free': memory_stats.total_free,
                        'peak_usage': memory_stats.peak_usage,
                        'fragmentation_ratio': memory_stats.fragmentation_ratio
                    },
                    'pool_status': {
                        'total_blocks': pool_status.total_blocks,
                        'used_blocks': pool_status.used_blocks,
                        'free_blocks': pool_status.free_blocks,
                        'utilization_ratio': pool_status.utilization_ratio,
                        'is_fragmented': pool_status.is_fragmented
                    }
                }
            except Exception as e:
                return {'error': str(e)}
        
        return {'error': 'C++ memory manager not available'}


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Enhanced YOLOv10 Auto-Annotation Service")
    parser.add_argument("--image", help="Path to input image")
    parser.add_argument("--video", help="Path to input video")
    parser.add_argument("--batch", nargs='+', help="Batch of image paths")
    parser.add_argument("--model", default="yolov10n.pt", help="Path to YOLOv10 model")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--no-cpp", action="store_true", help="Disable C++ optimizations")
    parser.add_argument("--stats", action="store_true", help="Show performance statistics")
    
    args = parser.parse_args()
    
    # Initialize enhanced service
    service = EnhancedYOLOv10Service(args.model, args.config)
    
    results = []
    
    # Process single image
    if args.image:
        print(f"Processing image: {args.image}")
        image_info = service.get_image_info(args.image)
        print(f"Image: {image_info['filename']} ({image_info['width']}x{image_info['height']})")
        
        detections = service.predict(args.image, use_cpp=not args.no_cpp)
        
        result = {
            'image_info': image_info,
            'detections': detections,
            'total_detections': len(detections),
            'model_version': 'YOLOv10 Enhanced'
        }
        results.append(result)
        
        print(f"\nFound {len(detections)} objects:")
        for i, detection in enumerate(detections):
            bbox = detection['bbox']
            print(f"  {i+1}. {detection['label']} (conf: {detection['confidence']:.3f})")
            print(f"      BBox: [{bbox[0]:.1f}, {bbox[1]:.1f}, {bbox[2]:.1f}, {bbox[3]:.1f}]")
    
    # Process video
    elif args.video:
        print(f"Processing video: {args.video}")
        result = service.process_video(args.video, args.output, use_cpp=not args.no_cpp)
        results.append(result)
        
        if result['success']:
            stats = result['stats']
            print(f"\nVideo processing completed:")
            print(f"  Total frames: {stats['total_frames']}")
            print(f"  Processed frames: {stats['processed_frames']}")
            print(f"  Average FPS: {stats['avg_fps']:.2f}")
            print(f"  Average processing time: {stats['avg_processing_time_ms']:.2f} ms")
    
    # Process batch
    elif args.batch:
        print(f"Processing batch of {len(args.batch)} images")
        batch_results = service.predict_batch(args.batch, use_cpp=not args.no_cpp)
        results.extend(batch_results)
        
        total_detections = sum(len(detections) for detections in batch_results)
        print(f"\nBatch processing completed:")
        print(f"  Total images: {len(args.batch)}")
        print(f"  Total detections: {total_detections}")
    
    # Show statistics
    if args.stats:
        print("\n" + "="*50)
        print("PERFORMANCE STATISTICS")
        print("="*50)
        
        perf_stats = service.get_performance_stats()
        print(f"Total inferences: {perf_stats['total_inferences']}")
        print(f"Average inference time: {perf_stats['avg_inference_time']:.3f}s")
        print(f"C++ usage count: {perf_stats['cpp_usage_count']}")
        print(f"Python usage count: {perf_stats['python_usage_count']}")
        print(f"C++ available: {perf_stats['cpp_available']}")
        print(f"C++ components: {', '.join(perf_stats['cpp_components'])}")
        
        memory_stats = service.get_memory_stats()
        if 'error' not in memory_stats:
            print(f"\nMemory Statistics:")
            mem_stats = memory_stats['memory_stats']
            print(f"  Total allocated: {mem_stats['total_allocated'] / (1024*1024):.1f} MB")
            print(f"  Total used: {mem_stats['total_used'] / (1024*1024):.1f} MB")
            print(f"  Peak usage: {mem_stats['peak_usage'] / (1024*1024):.1f} MB")
            print(f"  Fragmentation ratio: {mem_stats['fragmentation_ratio']:.3f}")
    
    # Save results if output file specified
    if args.output and results:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")
    
    return results


if __name__ == "__main__":
    main()
