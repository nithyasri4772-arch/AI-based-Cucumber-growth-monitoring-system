# 📂 Child-Level Project Structure Guide

This guide explains what every folder and file in your project does.

### 🌟 The Main Folders
| Folder Name | What is inside? | Why do we need it? |
| :--- | :--- | :--- |
| **`src/`** | The "Brain" of the project. | Contains all the Python code that runs the detection. |
| **`configs/`** | The "Memory" / Settings. | Where you put your API keys and WiFi IP address. |
| **`data/`** | The "Shed" (Storage). | Where the photos and logs (CSV) are saved. |
| **`models/`** | The "Teacher". | Where the YOLO AI model (`cucumber.pt`) lives. |
| **`dataset/`** | The "Study Notes". | Where you put photos to train the AI. |

---

### 🧠 Important Files in `src/`
- **`main.py`**: The "Start Button". Run this to start the whole system.
- **`dashboard.py`**: The "Monitoring Screen". Run this to see the charts and live view.
- **`capture/multi_angle_capture.py`**: Controls the Servo and Fan.
- **`utils/firebase_logger.py`**: Sends your data to the Google Database.

---

### ⚙️ The One File You Must Change
- **`configs/settings.yaml`**: This is the most important file. 
  - Change `firebase_enabled: true` to start the database.
  - Put your **ThingSpeak Key** here.
  - Put your **ESP32 IP address** here.

---

### 🏠 How to Move Around (The Paths)
- The project is in **`C:\Users\Asus\iot_ai_cucumber_project`**.
- To run the pipeline: Open PowerShell in this folder and type `python -m src.main`.
- To see your photos: Look in **`data/processed/`**.
- To see your sensor history: Look in **`data/logs/daily_growth_log.csv`**.

---

### 🚀 Starting your System
1. Open PowerShell.
2. Type `streamlit run src/dashboard.py`.
3. Open a second PowerShell window.
4. Type `python -m src.main`.
5. **Watch your dashboard update!**
