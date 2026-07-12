from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import random
import cv2
import numpy as np
try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None


@dataclass
class VisionConfig:
    yolo_model_path: str
    confidence_threshold: float
    use_mock_when_missing: bool
    use_opencv_filter: bool = True


class FruitDetector:
    def __init__(self, cfg: VisionConfig) -> None:
        self.cfg = cfg
        self.model = None
        if YOLO and Path(cfg.yolo_model_path).exists():
            try:
                self.model = YOLO(cfg.yolo_model_path)
            except Exception as e:
                print(f"[Vision] Failed to load YOLO model: {e}")

    def _opencv_detect(self, image: np.ndarray) -> List[Dict[str, float]]:
        # 0. Contrast Enhancement (CLAHE) - Essential for greenhouse lighting
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        
        # 1. RGB to HSV color space conversion
        hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
        
        # 2. Color segmentation (Green range)
        lower_green = np.array([35, 50, 40])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # 3. Gaussian blur noise removal
        blurred = cv2.GaussianBlur(mask, (7, 7), 0)
        
        # 4. Morphological operations (Closing holes)
        kernel = np.ones((5, 5), np.uint8)
        morphed = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
        
        # 5. Contour detection
        contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1200: # Slightly larger threshold for better quality
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = float(max(w, h)) / (min(w, h) + 1e-6)
                
                # Cucumbers are elongated (high aspect ratio)
                if aspect_ratio > 1.8:
                    detections.append({
                        "confidence": 0.88,
                        "pixel_length": float(max(w, h)),
                        "bbox": [x, y, w, h],
                        "detection_type": "opencv_robust"
                    })
        return detections

    def detect(self, images: Dict[str, np.ndarray]) -> List[Dict[str, float]]:
        all_detections: List[Dict[str, float]] = []

        for angle, img in images.items():
            angle_detections = []
            
            # Try YOLO first
            if self.model:
                results = self.model.predict(img, conf=self.cfg.confidence_threshold, verbose=False)
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        b = box.xywh[0].tolist() # x, y, w, h
                        angle_detections.append({
                            "angle": angle,
                            "confidence": float(box.conf),
                            "pixel_length": float(max(b[2], b[3])),
                            "bbox": b
                        })
            
            # Try OpenCV fallback/overlay if requested or if YOLO found nothing
            if self.cfg.use_opencv_filter and not angle_detections:
                cv_results = self._opencv_detect(img)
                for d in cv_results:
                    d["angle"] = angle
                    angle_detections.append(d)

            # Mock fallback if still empty and configured
            if not angle_detections and self.cfg.use_mock_when_missing:
                if random.random() > 0.4:
                    px = round(random.uniform(180.0, 420.0), 2)
                    angle_detections.append({
                        "angle": angle,
                        "confidence": round(random.uniform(0.70, 0.95), 2),
                        "pixel_length": px,
                        "bbox": [100, 100, px, 50]
                    })
            
            all_detections.extend(angle_detections)

        return all_detections

    def draw_detections(self, images: Dict[str, np.ndarray], detections: List[Dict[str, float]]) -> Dict[str, np.ndarray]:
        annotated: Dict[str, np.ndarray] = {}
        
        for angle, img in images.items():
            canvas = img.copy()
            angle_data = [d for d in detections if d["angle"] == angle]
            
            for d in angle_data:
                bbox = d.get("bbox")
                if bbox:
                    # Draw Bounding Box
                    x, y, w, h = [int(v) for v in bbox]
                    # If YOLO xywh, convert to x1y1x2y2 logic for opencv drawing if needed
                    # Our current logic gives x,y as top-left (OpenCV) or center (YOLO). 
                    # For simplicity, we assume top-left here or adjust.
                    cv2.rectangle(canvas, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    # Draw Label
                    label = f"Size: {d.get('size_cm', '??')}cm"
                    cv2.putText(canvas, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            annotated[angle] = canvas
            
        return annotated

