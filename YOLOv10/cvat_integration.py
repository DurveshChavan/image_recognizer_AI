#!/usr/bin/env python3
"""
CVAT Integration for YOLOv8 Auto-Annotation
This script converts YOLOv8 predictions to CVAT-compatible XML format.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import yaml
from yolov10_service import YOLOv10Service


class CVATIntegration:
    """CVAT integration for converting YOLOv10 predictions to CVAT XML format."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize CVAT integration.
        
        Args:
            config_path: Path to the configuration file
        """
        self._config_path = config_path
        self.config = self._load_config(config_path)
        self.yolo_service = None
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            print(f"Error: Config file {config_path} not found.")
            sys.exit(1)
    
    def initialize_yolo_service(self, model_path: str = None):
        """Initialize the YOLOv10 service."""
        if model_path is None:
            model_path = self.config.get('yolov10_model_path', 'yolov10n.pt')
        
        # Use the same config path that was passed to this class
        config_path = getattr(self, '_config_path', 'config.yaml')
        self.yolo_service = YOLOv10Service(model_path, config_path)
    
    def predict_and_convert(self, image_path: str) -> Dict[str, Any]:
        """
        Perform prediction and convert to CVAT format.
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Dictionary with CVAT-compatible annotation data
        """
        if self.yolo_service is None:
            self.initialize_yolo_service()
        
        # Get image info
        image_info = self.yolo_service.get_image_info(image_path)
        
        # Perform prediction
        detections = self.yolo_service.predict(image_path)
        
        # Convert to CVAT format
        cvat_annotations = self._convert_to_cvat_format(image_info, detections)
        
        return cvat_annotations
    
    def _convert_to_cvat_format(self, image_info: Dict[str, Any], 
                               detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Convert YOLOv10 detections to CVAT format.
        
        Args:
            image_info: Image information dictionary
            detections: List of YOLOv10 detection results
            
        Returns:
            CVAT-compatible annotation data
        """
        cvat_data = {
            'version': '1.1',
            'meta': {
                'task': {
                    'id': 1,
                    'name': 'YOLOv10 Auto-Annotation',
                    'size': 1,
                    'mode': 'annotation',
                    'overlap': 0,
                    'bugtracker': '',
                    'created': datetime.now().isoformat(),
                    'updated': datetime.now().isoformat(),
                    'start_frame': 0,
                    'stop_frame': 0,
                    'frame_filter': '',
                    'z_order': False,
                    'image_quality': 95,
                    'labels': []
                },
                'dumped': datetime.now().isoformat()
            },
            'annotations': []
        }
        
        # Add labels to meta
        for class_id, class_label in self.config['class_labels'].items():
            cvat_data['meta']['task']['labels'].append({
                'name': class_label,
                'color': '#000000',
                'attributes': []
            })
        
        # Create annotation for the image
        annotation = {
            'id': 1,
            'job_id': 1,
            'frame': 0,
            'filename': image_info['filename'],
            'width': image_info['width'],
            'height': image_info['height'],
            'shapes': []
        }
        
        # Convert detections to CVAT shapes
        for i, detection in enumerate(detections):
            bbox = detection['bbox']
            x1, y1, x2, y2 = bbox
            
            # Convert to CVAT format (x, y coordinates for rectangle)
            shape = {
                'id': i + 1,
                'type': 'rectangle',
                'label': detection['label'],
                'points': [
                    [x1, y1],  # Top-left
                    [x2, y2]   # Bottom-right
                ],
                'group_id': 0,
                'frame': 0,
                'occluded': False,
                'outside': False,
                'keyframe': True,
                'attributes': [
                    {
                        'name': 'confidence',
                        'value': f"{detection['confidence']:.3f}"
                    }
                ]
            }
            annotation['shapes'].append(shape)
        
        cvat_data['annotations'].append(annotation)
        
        return cvat_data
    
    def save_cvat_xml(self, cvat_data: Dict[str, Any], output_path: str):
        """
        Save CVAT data to XML file.
        
        Args:
            cvat_data: CVAT annotation data
            output_path: Path to save the XML file
        """
        xml_content = self._generate_cvat_xml(cvat_data)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"CVAT annotations saved to: {output_path}")
    
    def _generate_cvat_xml(self, cvat_data: Dict[str, Any]) -> str:
        """
        Generate CVAT XML content.
        
        Args:
            cvat_data: CVAT annotation data
            
        Returns:
            XML string content
        """
        xml_lines = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<annotations>',
            f'  <version>{cvat_data["version"]}</version>',
            '  <meta>',
            '    <task>',
            f'      <id>{cvat_data["meta"]["task"]["id"]}</id>',
            f'      <name>{cvat_data["meta"]["task"]["name"]}</name>',
            f'      <size>{cvat_data["meta"]["task"]["size"]}</size>',
            f'      <mode>{cvat_data["meta"]["task"]["mode"]}</mode>',
            f'      <overlap>{cvat_data["meta"]["task"]["overlap"]}</overlap>',
            f'      <bugtracker>{cvat_data["meta"]["task"]["bugtracker"]}</bugtracker>',
            f'      <created>{cvat_data["meta"]["task"]["created"]}</created>',
            f'      <updated>{cvat_data["meta"]["task"]["updated"]}</updated>',
            f'      <start_frame>{cvat_data["meta"]["task"]["start_frame"]}</start_frame>',
            f'      <stop_frame>{cvat_data["meta"]["task"]["stop_frame"]}</stop_frame>',
            f'      <frame_filter>{cvat_data["meta"]["task"]["frame_filter"]}</frame_filter>',
            f'      <z_order>{str(cvat_data["meta"]["task"]["z_order"]).lower()}</z_order>',
            f'      <image_quality>{cvat_data["meta"]["task"]["image_quality"]}</image_quality>',
            '      <labels>'
        ]
        
        # Add labels
        for label in cvat_data['meta']['task']['labels']:
            xml_lines.extend([
                '        <label>',
                f'          <name>{label["name"]}</name>',
                f'          <color>{label["color"]}</color>',
                '          <attributes>',
                '          </attributes>',
                '        </label>'
            ])
        
        xml_lines.extend([
            '      </labels>',
            '    </task>',
            f'    <dumped>{cvat_data["meta"]["dumped"]}</dumped>',
            '  </meta>',
            '  <annotations>'
        ])
        
        # Add annotations
        for annotation in cvat_data['annotations']:
            xml_lines.extend([
                '    <annotation>',
                f'      <id>{annotation["id"]}</id>',
                f'      <job_id>{annotation["job_id"]}</job_id>',
                f'      <frame>{annotation["frame"]}</frame>',
                f'      <filename>{annotation["filename"]}</filename>',
                f'      <width>{annotation["width"]}</width>',
                f'      <height>{annotation["height"]}</height>',
                '      <shapes>'
            ])
            
            # Add shapes
            for shape in annotation['shapes']:
                xml_lines.extend([
                    '        <shape>',
                    f'          <id>{shape["id"]}</id>',
                    f'          <type>{shape["type"]}</type>',
                    f'          <label>{shape["label"]}</label>',
                    '          <points>'
                ])
                
                # Add points
                for point in shape['points']:
                    xml_lines.append(f'            <point>{point[0]:.2f},{point[1]:.2f}</point>')
                
                xml_lines.extend([
                    '          </points>',
                    f'          <group_id>{shape["group_id"]}</group_id>',
                    f'          <frame>{shape["frame"]}</frame>',
                    f'          <occluded>{str(shape["occluded"]).lower()}</occluded>',
                    f'          <outside>{str(shape["outside"]).lower()}</outside>',
                    f'          <keyframe>{str(shape["keyframe"]).lower()}</keyframe>',
                    '          <attributes>'
                ])
                
                # Add attributes
                for attr in shape['attributes']:
                    xml_lines.extend([
                        '            <attribute>',
                        f'              <name>{attr["name"]}</name>',
                        f'              <value>{attr["value"]}</value>',
                        '            </attribute>'
                    ])
                
                xml_lines.extend([
                    '          </attributes>',
                    '        </shape>'
                ])
            
            xml_lines.extend([
                '      </shapes>',
                '    </annotation>'
            ])
        
        xml_lines.extend([
            '  </annotations>',
            '</annotations>'
        ])
        
        return '\n'.join(xml_lines)


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="CVAT Integration for YOLOv10 Auto-Annotation")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--model", help="Path to YOLOv10 model (overrides config)")
    parser.add_argument("--output", help="Output XML file path")
    
    args = parser.parse_args()
    
    # Initialize CVAT integration
    cvat_integration = CVATIntegration(args.config)
    
    # Initialize YOLO service
    model_path = args.model if args.model else None
    cvat_integration.initialize_yolo_service(model_path)
    
    # Process image
    print(f"Processing image: {args.image}")
    cvat_data = cvat_integration.predict_and_convert(args.image)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        # Create default output path
        image_name = os.path.splitext(os.path.basename(args.image))[0]
        output_dir = cvat_integration.config.get('output_dir', 'annotations')
        output_path = os.path.join(output_dir, f"{image_name}_annotations.xml")
    
    # Save CVAT XML
    cvat_integration.save_cvat_xml(cvat_data, output_path)
    
    # Print summary
    annotation = cvat_data['annotations'][0]
    print(f"\nAnnotation Summary:")
    print(f"  Image: {annotation['filename']} ({annotation['width']}x{annotation['height']})")
    print(f"  Objects detected: {len(annotation['shapes'])}")
    
    for shape in annotation['shapes']:
        print(f"    - {shape['label']} (confidence: {shape['attributes'][0]['value']})")
    
    return cvat_data


if __name__ == "__main__":
    main()
