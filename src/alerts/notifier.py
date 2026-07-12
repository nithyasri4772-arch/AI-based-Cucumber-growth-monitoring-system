from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AlertConfig:
    blynk_enabled: bool
    blynk_token: str
    mobile_notify: bool
    led_enabled: bool
    buzzer_enabled: bool


class Notifier:
    def __init__(self, cfg: AlertConfig) -> None:
        self.cfg = cfg

    def send(self, predictions: List[Dict[str, float]]) -> None:
        ready = [p for p in predictions if p.get("harvest_ready")]
        if not ready:
            print("[ALERT] No fruits are harvest-ready today.")
            return

        print(f"[ALERT] {len(ready)} fruit(s) are ready to harvest.")
        if self.cfg.mobile_notify:
            print("[ALERT] Mobile notification: sent (mock).")
        if self.cfg.led_enabled:
            print("[ALERT] LED indicator: ON (mock).")
        if self.cfg.buzzer_enabled:
            print("[ALERT] Buzzer: BEEP (mock).")
        if self.cfg.blynk_enabled:
            print("[ALERT] Blynk push: enabled (implement API call).")

