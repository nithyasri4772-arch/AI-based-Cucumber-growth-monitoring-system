@echo off
echo ===========================================
echo    Cucumber AI Model Training Launcher
echo ===========================================
echo.
echo [1/3] Activating Environment...
call .venv\Scripts\activate.bat

echo [2/3] Checking Dataset Folders...
if not exist dataset\images\train (
    echo.
    echo ERROR: Dataset not found in 'dataset/images/train'.
    echo Please follow DATASET_AND_TRAINING_GUIDE.md to set up folders.
    pause
    exit /b
)

echo [3/3] Starting YOLOv8 Training (100 Epochs)...
echo This may take a long time depending on your CPU/GPU.
yolo detect train data=dataset/data.yaml model=yolov8n.pt epochs=100 imgsz=640 batch=16 project=runs\cucumber name=exp

echo.
echo Training Finished!
echo Check your best model at: runs\cucumber\exp\weights\best.pt
echo Copy it to: models\yolo\cucumber.pt to use it in the dashboard.
pause
