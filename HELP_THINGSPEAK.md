# 📊 HELP: Optimal ThingSpeak Cloud Model

Setup your IoT cloud to capture every data point from your cucumber farm.

### 📜 Channel Configuration Strategy
1.  **Channel Name**: `Cucumber AI Farm Monitor`
2.  **Field Mapping** (Must follow this order for the Dashboard charts):
    - **Field 1**: `Temp (Celsius)` - Real-time temperature.
    - **Field 2**: `Humidity (%)` - Air moisture levels.
    - **Field 3**: `Cucumber Growth (cm)` - Size detected by AI.
    - **Field 4**: `Harvest Readiness` - Days remaining (0 = Ready).
    - **Field 5**: `Detection Count` - Total fruits found.

### 🚀 Integration Steps
1.  **API Keys**: Go to the **API Keys** tab.
2.  **Write Key**: Copy the `Write API Key`. 
3.  **Config**: Paste it into your `configs/settings.yaml` under `cloud: > thingspeak_write_api_key`.

### 💎 Dashboard Setup
To see the graphs inside your Streamlit Dashboard:
1.  Find your **Channel ID** (on the main page of your channel).
2.  Paste it into `configs/settings.yaml` under `dashboard: > thingspeak_channel_id`.
3.  Ensure your channel is set to **Public** (Sharing tab) so the dashboard can load the iframe.

### ⏱️ Data Rate Limit
- **Free Account**: ThingSpeak allows 1 update every **15 seconds**.
- **Setting**: In your `settings.yaml`, keep the `refresh_interval_sec` above 15 for cloud sync stability.
