#!/usr/bin/env python3
"""
YOLOv8 Service for Auto-Annotation
This script loads a YOLOv8 model and performs object detection on images.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Any

import cv2
import numpy as np
from ultralytics import YOLO
import yaml


class YOLOv8Service:
    """YOLOv8 service for object detection and annotation."""
    
    def __init__(self, model_path: str, config_path: str = "config.yaml"):
        """
        Initialize the YOLOv8 service.
        
        Args:
            model_path: Path to the YOLOv8 model file
            config_path: Path to the configuration file
        """
        self.model_path = model_path
        self.config = self._load_config(config_path)
        self.model = self._load_model()
        
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
                'class_labels': {}
            }
    
    def _load_model(self) -> YOLO:
        """Load the YOLOv8 model."""
        try:
            model = YOLO(self.model_path)
            print(f"Model loaded successfully from {self.model_path}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            sys.exit(1)
    
    def predict(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Perform object detection on an image.
        
        Args:
            image_path: Path to the input image
            
        Returns:
            List of detection results with bounding boxes, class labels, and confidence scores
        """
        try:
            # Load and validate image
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Perform prediction
            results = self.model(image_path, conf=self.config['confidence_threshold'], 
                               iou=self.config['iou_threshold'])
            
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
                            'class_label': class_label,
                            'confidence': confidence
                        }
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return []
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """
        Get image information (width, height, filename).
        
        Args:
            image_path: Path to the image
            
        Returns:
            Dictionary with image information
        """
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


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="YOLOv8 Auto-Annotation Service")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--model", default="yolov8n.pt", help="Path to YOLOv8 model")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--output", help="Output JSON file for results")
    
    args = parser.parse_args()
    
    # Initialize service
    service = YOLOv8Service(args.model, args.config)
    
    # Get image info
    image_info = service.get_image_info(args.image)
    print(f"Processing image: {image_info['filename']} ({image_info['width']}x{image_info['height']})")
    
    # Perform prediction
    detections = service.predict(args.image)
    
    # Prepare results
    results = {
        'image_info': image_info,
        'detections': detections,
        'total_detections': len(detections)
    }
    
    # Print results
    print(f"\nFound {len(detections)} objects:")
    for i, detection in enumerate(detections):
        bbox = detection['bbox']
        print(f"  {i+1}. {detection['class_label']} (conf: {detection['confidence']:.3f})")
        print(f"      BBox: [{bbox[0]:.1f}, {bbox[1]:.1f}, {bbox[2]:.1f}, {bbox[3]:.1f}]")
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")
    
    return results


if __name__ == "__main__":
    main()
