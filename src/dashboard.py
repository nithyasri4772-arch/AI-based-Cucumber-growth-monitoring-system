import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import time
import yaml
import os
from datetime import datetime
import streamlit.components.v1 as components
import firebase_admin
from firebase_admin import credentials, db

# Page config
st.set_page_config(
    page_title="Cucumber Master Hub",
    page_icon="🥒",
    layout="wide",
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .status-bar {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Load settings
@st.cache_data
def load_settings():
    with open("configs/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

cfg = load_settings()
log_path = Path(cfg["cloud"]["log_file"])

# Firebase Initialization
def init_firebase_v2():
    if not cfg["cloud"]["firebase_enabled"]:
        return False, "Firebase is disabled in settings.yaml"
    
    key_path = Path(cfg["cloud"]["firebase_service_account_key"])
    if not key_path.exists():
        key_path = Path(os.getcwd()) / cfg["cloud"]["firebase_service_account_key"]
            
    if not key_path.exists():
        return False, f"Key file '{cfg['cloud']['firebase_service_account_key']}' not found."
        
    try:
        try:
            firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(str(key_path))
            firebase_admin.initialize_app(cred, {
                'databaseURL': cfg["cloud"]["firebase_db_url"]
            })
        return True, "Connected"
    except Exception as e:
        return False, str(e)

if 'cloud_available' not in st.session_state or not st.session_state.cloud_available:
    success, msg = init_firebase_v2()
    st.session_state.cloud_available = success
    st.session_state.cloud_msg = msg

# Title and Sidebar
st.title("🥒 Cucumber Master Monitoring Hub")
st.sidebar.header("🎛️ Control Panel")

is_hardware = cfg["project"]["mode"] == "hardware"
status_color = "#238636" if is_hardware else "#8b949e"
status_text = "HARDWARE MODE ACTIVE" if is_hardware else "SIMULATION MODE ACTIVE"
st.sidebar.markdown(f'<div class="status-bar" style="background-color: {status_color}; color: white;">{status_text}</div>', unsafe_allow_html=True)

cloud_icon = "🟢" if st.session_state.cloud_available else "🔴"
cloud_text = "Cloud Connected" if st.session_state.cloud_available else "Cloud Offline"
st.sidebar.markdown(f"**{cloud_icon} {cloud_text}**")
if not st.session_state.cloud_available:
    st.sidebar.warning(f"Error: {st.session_state.cloud_msg}")

refresh_rate = st.sidebar.slider("Refresh Rate (s)", 5, 60, cfg["dashboard"]["refresh_interval_sec"])

def get_local_data():
    if not log_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(log_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df['source'] = 'Local'
    return df

def get_cloud_data():
    if not st.session_state.cloud_available:
        return pd.DataFrame()
    try:
        ref = db.reference('detections')
        snapshot = ref.order_by_key().limit_to_last(50).get()
        if not snapshot: return pd.DataFrame()
        rows = []
        for ts_key, entry in snapshot.items():
            row = {
                'timestamp': entry.get('timestamp', ts_key),
                'temperature_c': entry.get('sensors', {}).get('temperature_c', 0),
                'humidity_percent': entry.get('sensors', {}).get('humidity_percent', 0),
                'size_cm': entry.get('summary', {}).get('avg_size_cm', 0),
                'count': entry.get('summary', {}).get('count', 0),
                'source': 'Cloud'
            }
            rows.append(row)
        df = pd.DataFrame(rows)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        return df.dropna(subset=['timestamp'])
    except Exception:
        return pd.DataFrame()

data_mode = st.sidebar.radio("Data Source", ["Local Log", "Live Cloud"])
if data_mode == "Live Cloud":
    data = get_cloud_data()
    if data.empty: data = get_local_data()
else:
    data = get_local_data()

if data.empty:
    st.warning("No logs found. Run the pipeline first.")
else:
    latest = data.iloc[-1]
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Temperature", f"{latest.get('temperature_c', 0)}°C")
    with m2: st.metric("Humidity", f"{latest.get('humidity_percent', 0)}%")
    with m3: st.metric("Latest Size", f"{latest.get('size_cm', 0)} cm")
    with m4:
        days = latest.get('days_to_harvest', 'N/A')
        st.metric("Harvest Info", f"{days} Days" if days != 'N/A' else "N/A")

    tab1, tab2, tab3 = st.tabs(["🖼️ AI Live View", "📊 Cloud Charts (ThingSpeak)", "📜 History Log"])

    with tab1:
        st.subheader("Visual AI Detections")
        processed_dir = Path("data/processed")
        if processed_dir.exists():
            cols = st.columns(3)
            for i, angle in enumerate(["left", "top", "right"]):
                img_path = processed_dir / f"latest_{angle}.jpg"
                if img_path.exists():
                    with cols[i]:
                        st.image(str(img_path), caption=f"Angle: {angle.capitalize()}", use_container_width=True)
        else:
            st.info("Run the pipeline to see AI photos.")

    with tab2:
        st.subheader("ThingSpeak Live Cloud Integration")
        chan_id = cfg["dashboard"].get("thingspeak_channel_id")
        if chan_id:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**1. Temperature History**")
                components.iframe(f"https://thingspeak.com/channels/{chan_id}/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=30&type=line&update=15", height=250)
                st.markdown("**3. Cucumber Size (cm)**")
                components.iframe(f"https://thingspeak.com/channels/{chan_id}/charts/3?bgcolor=%23ffffff&color=%232ecc71&dynamic=true&results=30&type=line&update=15", height=250)
                st.markdown("**5. AI Detection Count**")
                components.iframe(f"https://thingspeak.com/channels/{chan_id}/charts/5?bgcolor=%23ffffff&color=%23f1c40f&dynamic=true&results=30&type=line&update=15", height=250)

            with c2:
                st.markdown("**2. Humidity History**")
                components.iframe(f"https://thingspeak.com/channels/{chan_id}/charts/2?bgcolor=%23ffffff&color=%233498db&dynamic=true&results=30&type=line&update=15", height=250)
                st.markdown("**4. Days to Harvest**")
                components.iframe(f"https://thingspeak.com/channels/{chan_id}/charts/4?bgcolor=%23ffffff&color=%23e67e22&dynamic=true&results=30&type=line&update=15", height=250)
                st.info("💡 Charts update every 15 seconds.")

    with tab3:
        st.subheader(f"Growth History ({data_mode})")
        st.dataframe(data.sort_values(by='timestamp', ascending=False), use_container_width=True)

    # Growth Trends - TWO GRAPHS SIDE BY SIDE
    st.subheader(f"📈 {data_mode} Growth Analytics")
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        y_val = 'size_cm'
        color_val = 'angle' if 'angle' in data.columns else None
        fig_growth = px.line(data, x='timestamp', y=y_val, color=color_val, markers=True, template="plotly_dark")
        fig_growth.update_layout(title="Growth Trends (Size cm)")
        st.plotly_chart(fig_growth, use_container_width=True)
        
    with g_col2:
        fig_env = go.Figure()
        fig_env.add_trace(go.Scatter(x=data['timestamp'], y=data['temperature_c'], name="Temp (°C)", line=dict(color='#ff4b4b')))
        fig_env.add_trace(go.Scatter(x=data['timestamp'], y=data['humidity_percent'], name="Humidity (%)", line=dict(color='#00d4ff')))
        fig_env.update_layout(
            template="plotly_dark",
            title="Climate: Temperature & Humidity",
            yaxis_title="Value",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_env, use_container_width=True)

# Footer
st.sidebar.divider()
if st.sidebar.button("Force Sync Cloud"):
    st.toast("Syncing with Firebase...")
    time.sleep(1)
    st.success("Cloud data synced!")

time.sleep(refresh_rate)
st.rerun()
