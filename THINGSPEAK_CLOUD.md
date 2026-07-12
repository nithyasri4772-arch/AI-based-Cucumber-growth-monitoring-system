# ThingSpeak-Style Cloud (Sensor + AI Results)

[ThingSpeak](https://thingspeak.com/) is a MathWorks IoT cloud: you create a **Channel**, get a **Write API Key**, then send numeric **fields** (`field1` … `field8`) with HTTP POST. Charts and MATLAB/React apps read the same channel.

This project can push **one update per pipeline run** (same idea as ESP32 → ThingSpeak, but from your PC or cloud VM).

---

## 1) Create a ThingSpeak account and channel

1. Go to [https://thingspeak.com](https://thingspeak.com) and sign up (free tier is enough to start).
2. **Channels → New Channel**.
3. Name it (e.g. `Cucumber IoT`).
4. Enable and name fields (optional but clearer on graphs):

   | ThingSpeak field | Meaning (this project)        |
   |------------------|-------------------------------|
   | Field 1          | Temperature (°C)              |
   | Field 2          | Humidity (%)                  |
   | Field 3          | Average cucumber size (cm)    |
   | Field 4          | Minimum days to harvest       |
   | Field 5          | Number of detections this run |

5. **Save Channel**.
6. Open **API Keys** tab → copy **Write API Key** (keep it secret).

---

## 2) Configure this project

Edit `configs/settings.yaml` under `cloud:`:

```yaml
cloud:
  log_file: "data/logs/daily_growth_log.csv"
  thingspeak_enabled: true
  thingspeak_write_api_key: "PASTE_YOUR_WRITE_API_KEY_HERE"
  # Optional: EU server if your account uses it
  # thingspeak_base_url: "https://api.thingspeak.com/update.json"
```

**Security:** Do not commit real API keys to public Git. Use env var in production (see below).

### Use environment variable (recommended)

Set before running:

**Windows PowerShell:**

```powershell
$env:THINGSPEAK_WRITE_API_KEY = "your_key_here"
```

**Linux / cloud / Codespaces:**

```bash
export THINGSPEAK_WRITE_API_KEY="your_key_here"
```

In `settings.yaml` you can leave:

```yaml
thingspeak_write_api_key: ""
```

If the key in YAML is empty, the code uses `THINGSPEAK_WRITE_API_KEY` from the environment when `thingspeak_enabled: true`.

---

## 3) Run the pipeline

Same as always:

```powershell
python scripts/setup_and_run.py
```

or:

```bash
python scripts/setup_and_run.py
```

On success you may see `[ThingSpeak] Update OK (entry_id=...)`.  
On failure: `[ThingSpeak] Upload failed: ...` (check key, internet, firewall).

---

## 4) View data in ThingSpeak

1. Open your channel on ThingSpeak.
2. **Private View** → charts update after each run (free tier has rate limits: **max ~1 update per 15 seconds** per channel).
3. If you run the script in a tight loop, space runs by **15+ seconds** or ThingSpeak will reject updates.

---

## 5) “ThingSpeak-like” alternatives (same pattern)

Same idea: **HTTP POST** with API key + fields.

| Service        | Idea |
|----------------|------|
| ThingSpeak     | Fields + charts + MATLAB |
| [Ubidots](https://ubidots.com) | Variables via REST |
| [Adafruit IO](https://io.adafruit.com) | Feeds + dashboards |
| InfluxDB Cloud | Time-series + Grafana |
| Custom Flask/FastAPI | Your own `POST /ingest` |

You can copy the pattern in `src/utils/cloud_logger.py` (`_push_thingspeak`) and change URL + JSON shape for another provider.

---

## 6) ESP32 → ThingSpeak (field reference)

If the **microcontroller** sends data directly to ThingSpeak, your PC pipeline can stay **CSV-only** (`thingspeak_enabled: false`) and only ThingSpeak stores the cloud history. If **both** send to the same channel, use different channels or merge logic carefully to avoid confusion.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| 403 / invalid key | Write API Key correct, channel not deleted |
| No new points | Free tier 15 s between updates; wait and run again |
| Timeout | Firewall / proxy blocking `api.thingspeak.com` |
| Empty charts | `thingspeak_enabled: true` and non-empty key or env var |

Official update docs: [ThingSpeak Write Data](https://www.mathworks.com/help/thingspeak/write-data-to-channel.html).
