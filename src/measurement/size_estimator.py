from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MeasurementConfig:
    marker_real_cm: float
    marker_pixel_size: float


class SizeEstimator:
    def __init__(self, cfg: MeasurementConfig) -> None:
        self.cfg = cfg

    def pixel_to_cm(self, pixel_value: float) -> float:
        # Formula: (fruit_px / marker_px) * marker_cm
        return (pixel_value / self.cfg.marker_pixel_size) * self.cfg.marker_real_cm

    def estimate(self, detections: List[Dict[str, float]]) -> List[Dict[str, float]]:
        enriched: List[Dict[str, float]] = []
        for item in detections:
            fruit_cm = round(self.pixel_to_cm(item["pixel_length"]), 2)
            new_item = dict(item)
            new_item["size_cm"] = fruit_cm
            enriched.append(new_item)
        return enriched

