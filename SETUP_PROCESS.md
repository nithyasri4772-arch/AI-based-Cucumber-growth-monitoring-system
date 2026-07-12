# 🚀 Complete Project Setup & Process Guide

Follow these exact steps to move your project from Simulation to Reality.

---

## **Step 1: ThingSpeak Setup (IoT Cloud)**
1.  **Website**: Go to [ThingSpeak.com](https://thingspeak.com).
2.  **Channel**: Create a **New Channel**.
3.  **Fields**: Enable **Field 1** (Temperature), **Field 2** (Humidity), and **Field 3** (Cucumber Size).
4.  **Keys**: Go to the **API Keys** tab and copy your **Write API Key**.
5.  **Config**: Open `configs/settings.yaml` and paste the key into `thingspeak_write_api_key`. Also, put your **Channel ID** into the `dashboard` section to see live charts.

---

## **Step 2: Firebase Setup (Growth History)**
1.  **Website**: Go to [Firebase Console](https://console.firebase.google.com).
2.  **Project**: Create a project and enable **Realtime Database**.
3.  **Rules**: Set rules to `true` (Test Mode) so the Python script can write data.
4.  **Key**: Go to **Project Settings** > **Service Accounts** > **Generate New Private Key**.
5.  **Placement**: Rename the downloaded `.json` file to **`firebase_key.json`** and place it in the project root folder.

---

## **Step 3: Hardware Connection (ESP32)**
1.  **WiFi**: Ensure your ESP32 is on the same WiFi as your computer.
2.  **Endpoint**: Once the ESP32 is running, get its IP address (e.g., `192.168.1.50`).
3.  **Config**: Update `esp32_endpoint` in `settings.yaml`.
4.  **Mode**: Change `project.mode` from `simulation` to `hardware`.

---

## **Step 4: AI Model Training (YOLOv8)**
1.  **Photos**: Take 30-50 photos of your cucumbers.
2.  **Training**: Use the `TRAIN_MY_MODEL.bat` file in this folder. It will guide you through training your own `cucumber.pt` model.
3.  **Deployment**: Once training finishes, the script will tell you where to find the model. Move it to `models/yolo/cucumber.pt`.

---

## **Step 5: Daily Monitoring Process**
1.  **Start Dashboard**:
    *   Open PowerShell and run: `streamlit run src/dashboard.py`
    *   This will open your Master Hub in the browser.
2.  **Run detection**:
    *   Every morning (or automatically), run the detection pipeline: `python -m src.main`
    *   The results will instantly appear on your dashboard!

---

## **File Checklist**
Check that you have these files in your folder:
- [ ] `configs/settings.yaml` (Updated with your keys)
- [ ] `firebase_key.json` (Your secret database key)
- [ ] `models/yolo/cucumber.pt` (Your trained AI model)
