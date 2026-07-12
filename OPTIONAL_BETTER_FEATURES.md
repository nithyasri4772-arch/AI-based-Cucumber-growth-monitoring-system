# Optional Improvements — Full List (Use What You Need)

This project already runs end-to-end in **simulation**. Below is a **complete optional menu** to make it **better for real use**: safer, more accurate, easier to operate, and closer to deployment.

Pick items in order: **stability → data → model → hardware → cloud → polish**.

---

## Tier A — Before you change code (high value, zero risk)

| Optional | Why it helps | What to do |
|----------|----------------|-------------|
| **Never commit API keys** | Avoid leaking ThingSpeak / Blynk tokens | Use env vars only; see `THINGSPEAK_CLOUD.md` |
| **Keep `configs/settings.yaml` in Git without secrets** | Same repo, safe sharing | Empty strings in YAML + env for real keys |
| **Version your own `settings.local.yaml`** (optional pattern) | Personal overrides without editing shared defaults | Copy `settings.yaml` → `settings.local.yaml`, load that in code later if you add it |
| **Run on a schedule** | Greenhouse / farm needs periodic readings | Windows **Task Scheduler** every 15+ min (ThingSpeak free tier: ≥15 s between posts) |
| **Backup `data/logs/`** | Long-term growth analytics | Copy CSV weekly to OneDrive / Google Drive |
| **Document your field setup** | Future you remembers wiring | One page: sensor type, camera URL, WiFi SSID (not password in repo) |

---

## Tier B — Configuration and cloud (optional, already partly supported)

| Optional | Why it helps | What to do |
|----------|----------------|-------------|
| **ThingSpeak dashboards** | See temperature, humidity, AI summary over time | `THINGSPEAK_CLOUD.md` + `cloud.thingspeak_enabled: true` |
| **Disable mock vision when model exists** | Forces real detections only | `vision.use_mock_when_missing: false` after `models/yolo/cucumber.pt` works |
| **Tune harvest prediction** | Match your cucumber variety / climate | Edit `prediction.ideal_harvest_cm`, `min/max_growth_cm_per_day` in `settings.yaml` |
| **Tune size scale** | More accurate cm from pixels | Calibrate `measurement.marker_real_cm` and `marker_pixel_size` with a real 5 cm reference in image |
| **Alerts** | Know when harvest_ready | Toggle `alerts.*` in `settings.yaml`; extend `notifier.py` for email/SMS later |

---

## Tier C — Dataset and model (biggest accuracy win)

| Optional | Why it helps | What to do |
|----------|----------------|-------------|
| **Your own photos** | Model learns your greenhouse, lighting, variety | Follow `DATASET_AND_TRAINING_GUIDE.md` |
| **Balanced dataset** | Fewer false positives | Many angles, day/night, occluded fruit, empty plant scenes |
| **Train YOLO (Ultralytics)** | Real bounding boxes instead of mock | `pip install ultralytics`, train, copy `best.pt` → `models/yolo/cucumber.pt` |
| **Implement real inference** | Template has a `pass` when model file exists | Fill `FruitDetector.detect()` in `src/vision/detector.py` with Ultralytics predict loop |
| **Retrain loop** | Model stays good as season changes | Monthly: add bad cases → label → retrain → replace `.pt` |

---

## Tier D — Hardware path (optional, for real IoT)

| Optional | Why it helps | What to do |
|----------|----------------|-------------|
| **ESP32 + DHT22** | Real temperature / humidity | Implement HTTP/MQTT in `sensor_reader.py` when `source: esp32` |
| **ESP32-CAM or USB camera** | Real images instead of numpy mocks | Replace `MultiAngleCapture.capture()` with camera + optional servo angles |
| **Marker in frame** | Stable cm measurement | Fixed color/size reference visible in every shot |
| **Local edge run** | Works if internet drops | Run pipeline on Raspberry Pi / mini PC near the farm |

---

## Tier E — Software engineering (optional, “production feel”)

| Optional | Why it helps | What to do |
|----------|----------------|-------------|
| **`.gitignore` for `.venv` and secrets** | Clean repo | Root `.gitignore` (included in project) |
| **Logging module** | Easier debugging than `print` only | Add `logging` in `main.py` and key modules |
| **CLI arguments** | One-off runs with different config | `argparse`: `--config path/to.yaml` |
| **Docker** | Same environment on PC and server | `Dockerfile` + mount `configs/`, `data/` |
| **Unit tests** | Safe refactors | `pytest` for `size_estimator`, `harvest_predictor` math |
| **Simple dashboard** | Non-technical users | Optional `streamlit` app reading latest CSV or ThingSpeak |

---

## Tier F — Security and reliability (optional, important if public)

| Optional | Why it helps | What to do |
|----------|----------------|-------------|
| **HTTPS only for ESP32 endpoints** | Avoid cleartext credentials | Reverse proxy (nginx) or device TLS where possible |
| **Rate limit cloud posts** | Respect ThingSpeak / API limits | Sleep ≥15 s between ThingSpeak updates on free tier |
| **Validate sensor range** | Reject bad readings | Clamp or drop if temp/humidity out of physical limits |
| **Secrets in CI** | Automated runs without leaking keys | GitHub Actions secrets for `THINGSPEAK_WRITE_API_KEY` |

---

## Suggested order (practical roadmap)

1. Use simulation until CSV + ThingSpeak (optional) look correct.  
2. Collect dataset + train YOLO + wire real `detect()`.  
3. Connect ESP32 sensors + real camera capture.  
4. Add scheduling + backups + logging.  
5. Add tests/Docker if you collaborate or deploy long-term.

---

## Quick “minimum better” pack (if you only do five things)

1. Enable ThingSpeak with **env var** key, not YAML in Git.  
2. Train one **cucumber.pt** and set `use_mock_when_missing: false`.  
3. Calibrate **marker** sizes in `settings.yaml`.  
4. **Schedule** one run every hour (or every 15+ minutes if pushing ThingSpeak each run).  
5. **Backup** `daily_growth_log.csv` weekly.

---

## Files in this repo that match optional areas

| Topic | File |
|-------|------|
| Run / setup | `README.md`, `CLOUD_SETUP.md` |
| Dataset + train | `DATASET_AND_TRAINING_GUIDE.md` |
| ThingSpeak | `THINGSPEAK_CLOUD.md` |
| Main pipeline | `src/main.py` |
| Vision hook | `src/vision/detector.py` |
| Sensors / camera | `src/sensors/sensor_reader.py`, `src/capture/multi_angle_capture.py` |
| Config | `configs/settings.yaml` |
| Logs + cloud push | `src/utils/cloud_logger.py` |

If you tell me your priority (**accuracy**, **hardware**, or **cloud dashboard**), I can turn one tier into a **short ordered checklist** only for that path.
