import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import feedparser
import requests
from datetime import datetime

# --- CONFIG & THEME ---
st.set_page_config(page_title="ENGINEER_TERMINAL_V1", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&display=swap');
    html, body, [class*="css"]  { font-family: 'IBM Plex Mono', monospace; background-color: #000000; color: #0dff00; }
    .stMetric { border: 1px solid #333; padding: 10px; border-radius: 0px; background-color: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA FETCHING ---
@st.cache_data(ttl=3600)
def get_fin_data():
    tickers = {"Gold": "GC=F", "Silver": "SI=F", "Copper": "HG=F", "Oil": "BZ=F"}
    data = yf.download(list(tickers.values()), period="1mo")['Close']
    data.columns = tickers.keys()
    return data

@st.cache_data(ttl=1800)
def get_kiel_tide():
    # Kiel Coordinates: 54.32, 10.13
    url = "https://marine-api.open-meteo.com/v1/marine?latitude=54.32&longitude=10.13&current=wave_height"
    try:
        r = requests.get(url).json()
        return f"{r['current']['wave_height']}m"
    except: return "N/A"

# --- SIDEBAR (INPUTS) ---
st.sidebar.title("🕹️ COMMAND_CENTER")
portfolio_val = st.sidebar.number_input("Current Portfolio (€)", value=10000, step=1000)
rent_goal = 1500
target_fire = (rent_goal * 12) / 0.04  # 4% Rule

# --- MAIN DASHBOARD ---
st.title("⚡ SOVEREIGN_ENGINEER_TERMINAL")
st.write(f"SYSTEM_TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | LOCATION: KIEL_GER")

col1, col2, col3 = st.columns(3)

# Row 1: Financial Metrics
data = get_fin_data()
gsr = data['Gold'].iloc[-1] / data['Silver'].iloc[-1]
gsr_prev = data['Gold'].iloc[-2] / data['Silver'].iloc[-2]

with col1:
    st.metric("GOLD/SILVER_RATIO", f"{gsr:.2f}", f"{gsr-gsr_prev:.2f}")
with col2:
    st.metric("COPPER_HG", f"{data['Copper'].iloc[-1]:.2f}", f"{(data['Copper'].iloc[-1]/data['Copper'].iloc[-2]-1)*100:.2f}%")
with col3:
    st.metric("KIEL_WAVE_HEIGHT", get_kiel_tide())

st.divider()

# Row 2: Charts & Freedom Tracker
c_left, c_right = st.columns([2, 1])

with c_left:
    st.subheader("📊 COMMODITY_DYNAMICS")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Gold']/data['Silver'], name="GSR", line=dict(color='#0dff00')))
    fig.update_layout(template="plotly_dark", height=300, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.subheader("🔓 FREEDOM_TRACKER")
    progress = min(portfolio_val / target_fire, 1.0)
    st.progress(progress)
    st.write(f"Goal: {target_fire:,.0f}€ (at 4% SWR)")
    st.write(f"Monthly Passive Est: {(portfolio_val * 0.04 / 12):.2f}€ / {rent_goal}€")

st.divider()

# Row 3: Engineering News
st.subheader("📰 INFRASTRUCTURE_WIRE")
feed = feedparser.parse("https://www.energy-storage.news/feed/")
for entry in feed.entries[:4]:
    st.markdown(f"**[{entry.title}]({entry.link})**")
    st.caption(f"Source: Energy Storage News | {entry.published[:16]}")
