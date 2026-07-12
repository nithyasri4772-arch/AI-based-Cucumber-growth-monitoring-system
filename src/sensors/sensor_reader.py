from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import random


@dataclass
class SensorConfig:
    source: str
    esp32_endpoint: str


class SensorReader:
    def __init__(self, cfg: SensorConfig) -> None:
        self.cfg = cfg

    def read(self) -> Dict[str, float]:
        # Simulation-first: ready to run even without hardware.
        if self.cfg.source == "simulated":
            return {
                "temperature_c": round(random.uniform(24.0, 34.0), 2),
                "humidity_percent": round(random.uniform(55.0, 90.0), 2),
            }
        # Placeholder for real ESP32 integration.
        return {
            "temperature_c": 28.0,
            "humidity_percent": 70.0,
        }

