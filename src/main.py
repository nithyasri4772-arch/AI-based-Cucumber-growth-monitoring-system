from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import yaml

from src.capture.multi_angle_capture import CaptureConfig, MultiAngleCapture
from src.sensors.sensor_reader import SensorConfig, SensorReader
from src.vision.detector import FruitDetector, VisionConfig
from src.measurement.size_estimator import MeasurementConfig, SizeEstimator
from src.prediction.harvest_predictor import HarvestPredictor, PredictionConfig
from src.alerts.notifier import AlertConfig, Notifier
from src.utils.cloud_logger import CloudLogConfig, CloudLogger
from src.utils.firebase_logger import FirebaseConfig


import argparse
import logging
import cv2
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("data/logs/pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_settings(path: str = "configs/settings.yaml") -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config from {path}: {e}")
        raise


def run_pipeline(config_path: str) -> None:
    logger.info("Starting Cucumber Detection Pipeline...")
    
    try:
        settings = load_settings(config_path)
        
        # Initialize Configs
        capture_cfg = CaptureConfig(**settings["capture"])
        sensor_cfg = SensorConfig(**settings["sensors"])
        vision_cfg = VisionConfig(**settings["vision"])
        measure_cfg = MeasurementConfig(**settings["measurement"])
        predict_cfg = PredictionConfig(**settings["prediction"])
        alert_cfg = AlertConfig(**settings["alerts"])
        cloud_cfg = CloudLogConfig(**settings["cloud"])
        # Handle Firebase sub-config from cloud section
        f_cfg_raw = settings["cloud"].copy()
        # Filter for FirebaseConfig fields
        f_cfg = FirebaseConfig(
            enabled=f_cfg_raw.get("firebase_enabled", False),
            service_account_key=f_cfg_raw.get("firebase_service_account_key", "firebase_key.json"),
            db_url=f_cfg_raw.get("firebase_db_url", "")
        )

        # Initialize Modules
        capturer = MultiAngleCapture(capture_cfg)
        sensor_reader = SensorReader(sensor_cfg)
        detector = FruitDetector(vision_cfg)
        estimator = SizeEstimator(measure_cfg)
        predictor = HarvestPredictor(predict_cfg)
        notifier = Notifier(alert_cfg)
        cloud_logger = CloudLogger(cloud_cfg, f_cfg)

        # 1. Capture Images
        logger.info(f"Capturing images for angles: {capture_cfg.angles}")
        images = capturer.capture()
        
        # 2. Read Sensors
        sensor_data = sensor_reader.read()
        logger.info(f"Sensor Data: {sensor_data}")
        
        # 3. Detect Fruits (YOLO + OpenCV Fallback)
        detections = detector.detect(images)
        logger.info(f"Detected {len(detections)} fruit(s) across all angles.")
        
        # 4. Measure Size
        sized = estimator.estimate(detections)
        
        # 5. Draw Visual Proof
        annotated = detector.draw_detections(images, sized)
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        for angle, ani_img in annotated.items():
            cv2.imwrite(str(processed_dir / f"latest_{angle}.jpg"), ani_img)
        logger.info(f"Visual proof saved to {processed_dir}")

        # 6. Predict Harvest
        predicted = predictor.add_predictions(sized, sensor_data)
        
        # 7. Log and Notify
        cloud_logger.write_daily_log(sensor_data, predicted)
        notifier.send(predicted)

        # Print Summary
        print("\n" + "="*40)
        print(f" CUCUMBER MONITORING SUMMARY ({datetime.now().strftime('%H:%M:%S')})")
        print("="*40)
        if not predicted:
            print(" No cucumbers detected in this run.")
        for item in predicted:
            status = "READY" if item['harvest_ready'] else f"{item['days_to_harvest']} days left"
            print(f" Angle: {item['angle']:<6} | Size: {item['size_cm']:>5} cm | Status: {status}")
        print("="*40 + "\n")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IoT & AI Cucumber Detection Pipeline")
    parser.add_argument("--config", type=str, default="configs/settings.yaml", help="Path to config file")
    args = parser.parse_args()
    
    run_pipeline(args.config)
