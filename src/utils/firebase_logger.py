from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List
import firebase_admin
from firebase_admin import credentials, db
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class FirebaseConfig:
    enabled: bool
    service_account_key: str
    db_url: str

class FirebaseLogger:
    def __init__(self, cfg: FirebaseConfig) -> None:
        self.cfg = cfg
        self.app = None
        if not cfg.enabled:
            return

        key_path = Path(cfg.service_account_key)
        if not key_path.exists():
            logger.warning(f"[Firebase] Key file not found at {key_path}. Firebase disabled.") 
            self.cfg.enabled = False
            return

        try:
            # Check if app already initialized
            try:
                self.app = firebase_admin.get_app()
            except ValueError:
                cred = credentials.Certificate(str(key_path))
                self.app = firebase_admin.initialize_app(cred, {
                    'databaseURL': cfg.db_url
                })
            logger.info("[Firebase] Initialized successfully.")
        except Exception as e:
            logger.error(f"[Firebase] Initialization failed: {e}")
            self.cfg.enabled = False

    def push_data(self, sensor_data: Dict[str, float], predictions: List[Dict[str, Any]]) -> None:
        if not self.cfg.enabled:
            return

        try:
            from datetime import datetime
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            ref = db.reference(f'detections/{ts}')
            
            n = len(predictions)
            avg_size = round(sum(item["size_cm"] for item in predictions) / n, 2) if n else 0.0
            
            data_to_push = {
                "timestamp": datetime.now().isoformat(),
                "sensors": sensor_data,
                "summary": {
                    "count": n,
                    "avg_size_cm": avg_size,
                    "harvest_ready_count": sum(1 for item in predictions if item.get("harvest_ready"))
                },
                "details": predictions
            }
            
            ref.set(data_to_push)
            db.reference('latest').set(data_to_push)
            
            logger.info(f"[Firebase] Data synced successfully to detections/{ts}")
        except Exception as e:
            logger.error(f"[Firebase] Push failed: {e}")
