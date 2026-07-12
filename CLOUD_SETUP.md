# Cloud Environment Setup (Step by Step)

Use this guide when you run the project **in the cloud** (browser IDE, Colab, or a Linux VM).  
Local Windows steps stay in `README.md`.

**Important:** In the cloud you usually have **no local ESP32/USB camera**. Keep `configs/settings.yaml` in **simulation** mode unless you connect real hardware over the network.

---

## What you need in any cloud

- Python **3.10+**
- Project folder as your **working directory** (clone or upload zip and unzip)
- Terminal access (bash)

---

## Option A — GitHub Codespaces (recommended for “cloud IDE”)

### Step 1: Put project on GitHub

Push this folder to a GitHub repository (or use an existing repo that contains it).

### Step 2: Open Codespaces

On GitHub: **Code → Codespaces → Create codespace** on the default branch.

### Step 3: Open terminal in Codespace

Bottom panel → **Terminal**. Shell is usually **bash**.

### Step 4: Go to project root

If the repo root *is* the project:

```bash
cd /workspaces/<your-repo-name>
```

If the project is in a subfolder:

```bash
cd /workspaces/<your-repo-name>/iot_ai_cucumber_project
```

### Step 5: Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 6: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 7: Run the pipeline

```bash
python scripts/setup_and_run.py
```

Same as:

```bash
python -m src.main
```

### Step 8: Check output

- Console: `=== PIPELINE RESULT ===`
- Log file: `data/logs/daily_growth_log.csv` (download from file explorer in Codespace if needed)

---

## Option B — Google Colab

Colab is good for **quick runs**; the session is **temporary** unless you save outputs to Drive.

### Step 1: Upload the project

- Zip `iot_ai_cucumber_project` on your PC.
- In Colab: **Files** (left) → upload the zip.

### Step 2: Unzip in a cell

```python
!unzip -q iot_ai_cucumber_project.zip -d /content/
```

If the zip contains a single top folder, `cd` into it (name may vary):

```python
%cd /content/iot_ai_cucumber_project
```

### Step 3: Install dependencies

```python
!pip install -q -r requirements.txt
```

### Step 4: Run

```python
!python scripts/setup_and_run.py
```

Or:

```python
!python -m src.main
```

**Note:** Colab’s current directory must be the project root so `configs/settings.yaml` resolves correctly. Use `%cd` to that folder before running.

---

## Option C — Linux cloud VM (AWS EC2, Azure VM, GCP Compute Engine, etc.)

### Step 1: SSH into the VM

Use your provider’s SSH instructions.

### Step 2: Install Python (if missing)

Ubuntu/Debian example:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

### Step 3: Get the project

Either **git clone**:

```bash
git clone <your-repo-url>
cd <repo>/iot_ai_cucumber_project
```

Or upload with `scp`/SFTP and unzip, then `cd` into the project folder.

### Step 4: venv + install + run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/setup_and_run.py
```

---

## Training (Ultralytics) in the cloud

After the base pipeline runs, you can train YOLO in the same environment:

```bash
source .venv/bin/activate   # if not already active
pip install ultralytics
```

Then follow `DATASET_AND_TRAINING_GUIDE.md` (use Linux paths like `runs/cucumber/...`).

GPU instances (Colab Pro, cloud GPU VM) speed training a lot.

---

## Config reminders in the cloud

| Setting | Typical cloud value |
|--------|----------------------|
| `project.mode` | `simulation` |
| `sensors.source` | `simulated` |
| `vision.use_mock_when_missing` | `true` until `models/yolo/cucumber.pt` exists |

If later your ESP32 exposes HTTP/MQTT on a **public or VPN URL**, you can point `esp32_endpoint` there from the cloud (security: use auth/VPN, not open internet without protection).

---

## Quick reference (bash)

```bash
cd /path/to/iot_ai_cucumber_project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/setup_and_run.py
```
