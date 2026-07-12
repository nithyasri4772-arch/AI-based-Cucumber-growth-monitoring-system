# IoT and AI Cucumber Detection Project

This project is a complete starter pipeline for:

- capturing multi-angle cucumber images (`top`, `left`, `right`)
- reading temperature and humidity (simulated now, ESP32-ready design)
- detecting cucumbers (YOLO-ready with mock fallback)
- estimating fruit size in centimeters using marker scale
- predicting days remaining to harvest
- generating alerts and writing daily logs

The current code runs fully in simulation mode, so you can run end-to-end without hardware.

## Tech Stack

- **Core Language**: Python 3.10+
- **AI & Computer Vision**: 
  - **Ultralytics YOLOv8**: For fruit detection and localization.
  - **OpenCV (opencv-python)**: For image capture, processing, and pixel-to-cm visual size estimation.
- **Web Dashboard**: 
  - **Streamlit**: Interactive UI to visualize detection history and statistics.
  - **Plotly & Pandas**: Data manipulation and high-fidelity charting.
- **Cloud & IoT Integration**:
  - **Firebase (firebase-admin)**: Cloud real-time database and data sync.
  - **ThingSpeak**: IoT analytics platform service (for remote sensor monitoring/charts).
- **Machine Learning**: 
  - **Scikit-learn**: For predictive modeling of days remaining to harvest.
- **Data & Configuration**:
  - **YAML (PyYAML)**: Configuration file management.
  - **CSV**: Local persistent logging.
- **Hardware Stack (Supported/ESP32 Ready)**:
  - **ESP32 Microcontroller**: Core controller for sensors and camera.
  - **DHT11 / DHT22 Sensor**: For ambient temperature & humidity tracking.

## 1) End-to-End Workflow (Start to Finish)

1. Load config from `configs/settings.yaml`
2. Capture images from multiple angles (`src/capture/multi_angle_capture.py`)
3. Read sensor values (`src/sensors/sensor_reader.py`)
4. Detect fruits (`src/vision/detector.py`)
5. Convert pixel length to cm (`src/measurement/size_estimator.py`)
6. Predict harvest days (`src/prediction/harvest_predictor.py`)
7. Trigger alerts (`src/alerts/notifier.py`)
8. Write CSV log (`src/utils/cloud_logger.py`)
9. Print final pipeline result on console (`src/main.py`)

## 2) Prerequisites

- **Local Windows:** Windows 10/11 + Python 3.10+ (recommended)
- **Cloud (Codespaces / Colab / Linux VM):** Python 3.10+ and a terminal — see **`CLOUD_SETUP.md`** for full step-by-step
- Internet (first-time dependency install)

Check Python:

```powershell
py --version
python --version
```

### Cloud environment (Codespaces, Colab, Linux VM)

Full bash/Colab steps are in **[`CLOUD_SETUP.md`](CLOUD_SETUP.md)** — same project, no Windows `run.ps1` required; use `venv` + `python scripts/setup_and_run.py`.

### ThingSpeak-style IoT cloud (charts + history)

Send temperature, humidity, and AI summary fields to **[ThingSpeak](https://thingspeak.com)** from each run: **[`THINGSPEAK_CLOUD.md`](THINGSPEAK_CLOUD.md)**. Configure under `cloud:` in `configs/settings.yaml`.

## 3) Project Setup (First Time)

Open PowerShell in project folder:

```powershell
cd C:\Users\Asus\iot_ai_cucumber_project
```

Create virtual environment:

```powershell
py -m venv .venv
```

Activate virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If script policy blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4) Run the Project

### Option A: Recommended (PowerShell, auto setup + run)

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

### Option B: Command Prompt

```bat
run.bat
```

### Option C: Manual run (when venv already active)

```powershell
python .\scripts\setup_and_run.py
```

or directly:

```powershell
python -m src.main
```

## 5) Expected Output

Typical run output:

- alert message (for ready or not-ready fruits)
- sensor values (temperature and humidity)
- number of detections
- per-angle confidence, size in cm, days to harvest
- CSV log save path

CSV log is appended to:

`data/logs/daily_growth_log.csv`

## 6) Configuration (`configs/settings.yaml`)

Important keys:

- `project.mode`: `simulation` or `hardware` (currently simulation behavior)
- `capture.angles`: image angles to process
- `sensors.source`: `simulated` or `esp32`
- `vision.yolo_model_path`: expected model path (`models/yolo/cucumber.pt`)
- `vision.use_mock_when_missing`: when `true`, still runs without YOLO model
- `measurement.marker_real_cm`, `measurement.marker_pixel_size`: pixel-to-cm scaling
- `prediction.*`: harvest prediction parameters
- `alerts.*`: notification toggles
- `cloud.log_file`: CSV path

## 7) Code Modules and Responsibilities

- `src/main.py`: pipeline orchestration
- `src/capture/multi_angle_capture.py`: image capture layer (mock image generation now)
- `src/sensors/sensor_reader.py`: sensor abstraction (simulated now, hardware placeholder)
- `src/vision/detector.py`: YOLO integration point + mock detections
- `src/measurement/size_estimator.py`: pixel-length to centimeter conversion
- `src/prediction/harvest_predictor.py`: days-to-harvest estimation logic
- `src/alerts/notifier.py`: alert channel handling
- `src/utils/cloud_logger.py`: CSV logging
- `scripts/setup_and_run.py`: ensures folders and runs pipeline

## 8) Move from Simulation to Real Hardware

1. Add trained model to `models/yolo/cucumber.pt`
2. Replace detection `pass` block in `src/vision/detector.py` with actual YOLO inference
3. Replace simulated capture in `src/capture/multi_angle_capture.py` with camera input
4. Replace sensor placeholder in `src/sensors/sensor_reader.py` with ESP32 API/MQTT calls
5. Set `sensors.source: "esp32"` and correct `esp32_endpoint` in config
6. If needed, replace alert mocks with real Blynk/IoT notification APIs

## 9) Troubleshooting

### Problem: Script window opens and closes quickly

Do not double-click `.bat`/`.ps1`. Run from terminal:

```powershell
cd C:\Users\Asus\iot_ai_cucumber_project
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

### Problem: `pip` or dependency error

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Problem: Reset environment cleanly

```powershell
deactivate
rmdir /s /q .venv
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\scripts\setup_and_run.py
```

## 10) Quick Command Cheat Sheet

```powershell
cd C:\Users\Asus\iot_ai_cucumber_project
.\.venv\Scripts\Activate.ps1
python .\scripts\setup_and_run.py
```

## 11) Current Dependency List

From `requirements.txt`:

- `numpy==2.1.3`
- `PyYAML==6.0.2`

## 12) Own Dataset and Training (Next Stage)

If you plan to create your own cucumber dataset and train a model, follow:

- `DATASET_AND_TRAINING_GUIDE.md`

After training, copy best model to:

- `models/yolo/cucumber.pt`

Then run the same pipeline again:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

## 13) Optional improvements (full menu)

To make the project **better step by step** as you use it (cloud, training, hardware, scheduling, security):

- **[`OPTIONAL_BETTER_FEATURES.md`](OPTIONAL_BETTER_FEATURES.md)** — complete optional checklist by tier

A root **`.gitignore`** is included so `.venv`, cache files, and optional local secret files are less likely to be committed by mistake.

