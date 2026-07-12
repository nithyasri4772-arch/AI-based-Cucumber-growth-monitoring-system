from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PredictionConfig:
    ideal_harvest_cm: float
    min_growth_cm_per_day: float
    max_growth_cm_per_day: float
    baseline_growth_cm_per_day: float


class HarvestPredictor:
    def __init__(self, cfg: PredictionConfig) -> None:
        self.cfg = cfg

    def predict_days_remaining(self, size_cm: float, temperature_c: float, humidity_percent: float) -> int:
        # Implementation of the optimized growth logic from the project specification
        # Growth factors based on Section 5.6 of the methodology
        
        if temperature_c > 32:
            avg_growth = self.cfg.max_growth_cm_per_day # 2.5cm/day
        elif temperature_c < 25:
            avg_growth = self.cfg.min_growth_cm_per_day # 1.0cm/day
        else:
            avg_growth = self.cfg.baseline_growth_cm_per_day # 1.8cm/day

        # Humidity adjustment (Subtle boost for high humidity)
        if humidity_percent > 70:
            avg_growth *= 1.05

        remaining = max(self.cfg.ideal_harvest_cm - size_cm, 0.0)
        
        if remaining <= 0:
            return 0
            
        return int(round(remaining / avg_growth))

    def add_predictions(self, sized_detections: List[Dict[str, float]], sensor_data: Dict[str, float]) -> List[Dict[str, float]]:
        out: List[Dict[str, float]] = []
        for item in sized_detections:
            days = self.predict_days_remaining(
                size_cm=item["size_cm"],
                temperature_c=sensor_data["temperature_c"],
                humidity_percent=sensor_data["humidity_percent"],
            )
            new_item = dict(item)
            new_item["days_to_harvest"] = days
            new_item["harvest_ready"] = days <= 0
            out.append(new_item)
        return out

