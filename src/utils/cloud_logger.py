from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import csv
import json
import os
import urllib.error
import urllib.request
from src.utils.firebase_logger import FirebaseConfig, FirebaseLogger


@dataclass
class CloudLogConfig:
    log_file: str
    thingspeak_enabled: bool = False
    thingspeak_write_api_key: str = ""
    thingspeak_base_url: str = "https://api.thingspeak.com/update.json"
    firebase_enabled: bool = False
    firebase_service_account_key: str = "firebase_key.json"
    firebase_db_url: str = ""


class CloudLogger:
    def __init__(self, cfg: CloudLogConfig, firebase_cfg: FirebaseConfig = None) -> None:
        self.cfg = cfg
        self.firebase = None
        if firebase_cfg:
            self.firebase = FirebaseLogger(firebase_cfg)
            
        Path(self.cfg.log_file).parent.mkdir(parents=True, exist_ok=True)

    def _push_thingspeak(self, sensor_data: Dict[str, float], predictions: List[Dict[str, float]]) -> None:
        if not self.cfg.thingspeak_enabled:
            return
        api_key = (self.cfg.thingspeak_write_api_key or "").strip() or os.environ.get("THINGSPEAK_WRITE_API_KEY", "").strip()
        if not api_key:
            print("[ThingSpeak] Skipped: no write API key (YAML or THINGSPEAK_WRITE_API_KEY).")
            return

        n = len(predictions)
        avg_size = round(sum(p["size_cm"] for p in predictions) / n, 2) if n else 0.0
        min_days = min((int(p["days_to_harvest"]) for p in predictions), default=999)

        payload = {
            "api_key": api_key,
            "field1": float(sensor_data["temperature_c"]),
            "field2": float(sensor_data["humidity_percent"]),
            "field3": float(avg_size),
            "field4": float(min_days),
            "field5": float(n),
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.cfg.thingspeak_base_url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            data = json.loads(raw) if raw.strip().startswith("{") else {}
            entry_id = data.get("entry_id")
            if entry_id is not None:
                print(f"[ThingSpeak] Update OK (entry_id={entry_id}).")
            else:
                print(f"[ThingSpeak] Response: {raw[:200]}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            print(f"[ThingSpeak] HTTP {e.code}: {err_body[:300]}")
        except urllib.error.URLError as e:
            print(f"[ThingSpeak] Upload failed: {e.reason}")
        except Exception as e:
            print(f"[ThingSpeak] Upload failed: {e}")

    def write_daily_log(self, sensor_data: Dict[str, float], predictions: List[Dict[str, float]]) -> None:
        file_exists = Path(self.cfg.log_file).exists()
        with open(self.cfg.log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(
                    [
                        "timestamp",
                        "temperature_c",
                        "humidity_percent",
                        "angle",
                        "confidence",
                        "size_cm",
                        "days_to_harvest",
                        "harvest_ready",
                    ]
                )

            ts = datetime.now().isoformat(timespec="seconds")
            for row in predictions:
                writer.writerow(
                    [
                        ts,
                        sensor_data["temperature_c"],
                        sensor_data["humidity_percent"],
                        row["angle"],
                        row["confidence"],
                        row["size_cm"],
                        row["days_to_harvest"],
                        row["harvest_ready"],
                    ]
                )

        self._push_thingspeak(sensor_data, predictions)
        if self.firebase:
            self.firebase.push_data(sensor_data, predictions)

