import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- APPLE DESIGN SYSTEM CONFIG ---
st.set_page_config(page_title="Gold Pro", layout="centered")

# Advanced CSS for the "Apple" look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    .stApp {
        background-color: #000000;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Remove Streamlit Clutter */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; max-width: 500px;}

    /* Center Header */
    .title-text {
        text-align: center;
        font-weight: 500;
        font-size: 18px;
        color: #8e8e93;
        margin-bottom: 5px;
    }

    /* Price Styling */
    .price-large {
        text-align: center;
        font-size: 52px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -2px;
        margin: 0;
    }

    .delta-text {
        text-align: center;
        font-size: 19px;
        font-weight: 500;
        margin-top: -5px;
        margin-bottom: 30px;
    }

    /* Styling the Segmented Control (Pills) */
    div[data-testid="stSegmentedControl"] {
        display: flex;
        justify-content: center;
        background-color: #1c1c1e;
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 30px;
    }
    
    button[data-testid="stSegmentedControlItem"] {
        background-color: transparent !important;
        border: none !important;
        color: #ffffff !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    button[data-testid="stSegmentedControlItem"][aria-checked="true"] {
        background-color: #3a3a3c !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA FETCHING ---
@st.cache_data(ttl=600)
def fetch_gold(period):
    try:
        data = yf.Ticker("GC=F").history(period=period)
        return data if not data.empty else None
    except:
        return None

# --- UI LAYOUT ---
st.markdown('<p class="title-text">Gold</p>', unsafe_allow_html=True)

# 1. Timeframe Selection (Segmented Control / Pills)
timeframe_options = ["1M", "6M", "1Y", "5Y", "All"]
timeframe_map = {"1M": "1mo", "6M": "6mo", "1Y": "1y", "5Y": "5y", "All": "max"}

# Using the modern segmented_control (available in 2026)
selected_tf = st.segmented_control(
    "Timeframe", 
    options=timeframe_options, 
    default="1Y", 
    label_visibility="collapsed"
)

df = fetch_gold(timeframe_map[selected_tf])

if df is not None:
    current = float(df['Close'].iloc[-1])
    prev = float(df['Close'].iloc[-2])
    diff = current - prev
    pct = (diff / prev) * 100
    color = "#32d74b" if diff >= 0 else "#ff453a"

    # 2. Display Price & Change
    st.markdown(f'<p class="price-large">${current:,.2f}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="delta-text" style="color: {color};">{"↑" if diff >= 0 else "↓"} {abs(diff):.2f} ({abs(pct):.2f}%)</p>', unsafe_allow_html=True)

    # 3. The Apple-Style Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'],
        mode='lines',
        line=dict(color='#ffffff', width=2.5, shape='spline'), # Spline = Smooth Curve
        fill='tozeroy',
        fillcolor='rgba(255, 255, 255, 0.04)'
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=320,
        xaxis=dict(showgrid=False, showticklabels=True, color="#48484a", nticks=4, font=dict(size=10)),
        yaxis=dict(showgrid=False, showticklabels=False, fixedrange=True),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1c1c1e", font_size=12, font_family="Inter")
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown(f"<p style='text-align: center; color: #48484a; font-size: 11px; margin-top: 40px;'>Data: Yahoo Finance • {selected_tf} View</p>", unsafe_allow_html=True)

else:
    st.markdown("<h2 style='text-align: center; color: #ff453a; margin-top: 100px;'>Data Sync Error</h2>", unsafe_allow_html=True)
