from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Any
import numpy as np
import time
import requests

logger = logging.getLogger(__name__)

@dataclass
class CaptureConfig:
    angles: List[str]
    output_dir: str
    image_width: int
    image_height: int
    hardware_trigger_enabled: bool = False
    esp32_control_url: str = ""
    servo_angles: Dict[str, int] = field(default_factory=dict)
    fan_delay_sec: float = 2.0

class MultiAngleCapture:
    def __init__(self, cfg: CaptureConfig) -> None:
        self.cfg = cfg
        Path(self.cfg.output_dir).mkdir(parents=True, exist_ok=True)

    def _send_command(self, endpoint: str) -> bool:
        if not self.cfg.hardware_trigger_enabled or not self.cfg.esp32_control_url:
            return True
        
        url = f"{self.cfg.esp32_control_url}{endpoint}"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                logger.info(f"[Hardware] Command Success: {endpoint}")
                return True
            else:
                logger.warning(f"[Hardware] Command Failed ({resp.status_code}): {endpoint}")
        except Exception as e:
            logger.error(f"[Hardware] Connection Error: {e}")
        return False

    def capture(self) -> Dict[str, np.ndarray]:
        images: Dict[str, np.ndarray] = {}
        
        for idx, angle in enumerate(self.cfg.angles):
            logger.info(f"Processing angle: {angle}")
            
            # 1. Move Servo to Angle
            target_angle = self.cfg.servo_angles.get(angle, 90)
            self._send_command(f"/move?angle={target_angle}")
            
            # 2. Turn on Fan to blow leaves
            self._send_command("/fan?state=on")
            
            # 3. Wait for environment to stabilize
            if self.cfg.hardware_trigger_enabled:
                time.sleep(self.cfg.fan_delay_sec)
            
            # 4. Capture Image
            # Mock image generation for now. 
            # In hardware mode, this would trigger a Camera API or open a WebCam.
            img = np.zeros((self.cfg.image_height, self.cfg.image_width, 3), dtype=np.uint8)
            # Create a "Cucumber-colored" block (Green)
            cv2_color = (0, 200, 0)
            import cv2
            cv2.rectangle(img, (100, 100), (300, 400), cv2_color, -1)
            
            images[angle] = img
            
            # 5. Turn off Fan
            self._send_command("/fan?state=off")
            
        return images
