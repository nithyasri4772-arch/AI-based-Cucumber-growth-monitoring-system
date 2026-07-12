from pathlib import Path
import subprocess
import sys


def ensure_dirs() -> None:
    required = [
        "data/raw",
        "data/processed",
        "data/logs",
        "models/yolo",
        "src/capture",
        "src/sensors",
        "src/vision",
        "src/measurement",
        "src/prediction",
        "src/alerts",
        "src/utils",
    ]
    for folder in required:
        Path(folder).mkdir(parents=True, exist_ok=True)


def run_pipeline() -> int:
    return subprocess.call([sys.executable, "-m", "src.main"])


if __name__ == "__main__":
    ensure_dirs()
    code = run_pipeline()
    raise SystemExit(code)

