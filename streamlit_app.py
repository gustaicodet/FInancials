import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="FIN_TERMINAL_V2", layout="wide")

# Extreme Minimalist CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&display=swap');
    html, body, [class*="css"]  { font-family: 'IBM Plex Mono', monospace; background-color: #000000; color: #0dff00; }
    .stMetric { border-bottom: 1px solid #333; padding: 15px 0px; border-radius: 0px; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data(ttl=300) # Updates every 5 minutes
def get_market_data():
    tickers = {
        "DAX": "^GDAXI", "DOW": "^DJI", "S&P500": "^GSPC",
        "NIKKEI": "^N225", "HANG_SENG": "^HSI",
        "GOLD": "GC=F", "SILVER": "SI=F", "COPPER": "HG=F", "BRENT": "BZ=F"
    }
    data = yf.download(list(tickers.values()), period="5d")['Close']
    return data, tickers

data, tickers = get_market_data()

# --- CALCULATIONS ---
def get_change(ticker_key):
    symbol = tickers[ticker_key]
    current = data[symbol].iloc[-1]
    prev = data[symbol].iloc[-2]
    diff = current - prev
    pct = (diff / prev) * 100
    return current, pct

# --- HEADER ---
st.title("📟 MARKET_PULSE_V2")
st.caption(f"LAST_SYNC: {datetime.now().strftime('%H:%M:%S')} | STATUS: ONLINE")
st.divider()

# --- ZONE 1: WESTERN INDICES ---
st.subheader("🌐 WESTERN_MARKETS")
col1, col2, col3 = st.columns(3)
with col1:
    val, pct = get_change("DAX")
    st.metric("GER_DAX", f"{val:,.2f}", f"{pct:.2f}%")
with col2:
    val, pct = get_change("S&P500")
    st.metric("US_S&P500", f"{val:,.2f}", f"{pct:.2f}%")
with col3:
    val, pct = get_change("DOW")
    st.metric("US_DOW_JONES", f"{val:,.2f}", f"{pct:.2f}%")

# --- ZONE 2: ASIAN INDICES ---
st.subheader("🌏 ASIAN_MARKETS")
col_a1, col_a2 = st.columns(2)
with col_a1:
    val, pct = get_change("NIKKEI")
    st.metric("JPN_NIKKEI_225", f"{val:,.2f}", f"{pct:.2f}%")
with col_a2:
    val, pct = get_change("HANG_SENG")
    st.metric("HK_HANG_SENG", f"{val:,.2f}", f"{pct:.2f}%")

st.divider()

# --- ZONE 3: COMMODITIES & RATIOS ---
st.subheader("🧱 HARD_ASSETS")
m1, m2, m3, m4 = st.columns(4)

gold_val, gold_pct = get_change("GOLD")
silv_val, silv_pct = get_change("SILVER")
gsr = gold_val / silv_val
gsr_prev = data[tickers["GOLD"]].iloc[-2] / data[tickers["SILVER"]].iloc[-2]

with m1:
    st.metric("GOLD_OZ", f"${gold_val:,.2f}", f"{gold_pct:.2f}%")
with m2:
    st.metric("SILVER_OZ", f"${silv_val:,.2f}", f"{silv_pct:.2f}%")
with m3:
    st.metric("G/S_RATIO", f"{gsr:.2f}", f"{gsr - gsr_prev:.2f}")
with m4:
    oil_val, oil_pct = get_change("BRENT")
    st.metric("BRENT_CRUDE", f"${oil_val:.2f}", f"{oil_pct:.2f}%")

st.metric("COPPER_LB", f"${data[tickers['COPPER']].iloc[-1]:.2f}", 
          f"{( (data[tickers['COPPER']].iloc[-1]/data[tickers['COPPER']].iloc[-2]) - 1)*100:.2f}%")

# --- VISUAL SIGNAL (GSR CHART) ---
st.subheader("📉 RATIO_TRACKER")
gsr_series = data[tickers["GOLD"]] / data[tickers["SILVER"]]
fig = go.Figure()
fig.add_trace(go.Scatter(x=gsr_series.index, y=gsr_series, line=dict(color='#0dff00', width=2)))
fig.update_layout(
    template="plotly_dark", height=250, margin=dict(l=0,r=0,t=0,b=0),
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=False), xaxis=dict(showgrid=False)
)
st.plotly_chart(fig, use_container_width=True)
