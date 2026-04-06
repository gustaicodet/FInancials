import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- APPLE DESIGN CONFIG ---
st.set_page_config(page_title="Gold Pro", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    .stApp { background-color: #000000; font-family: 'Inter', -apple-system, sans-serif; }
    h1 { font-weight: 600; letter-spacing: -1px; color: #ffffff; text-align: center; margin-bottom: 0; }
    .price-text { font-size: 56px; font-weight: 600; color: #ffffff; margin: 0; text-align: center; }
    .change-text { font-size: 24px; font-weight: 400; margin-top: -5px; text-align: center; margin-bottom: 20px; }
    
    /* Minimalist Slider Styling */
    .stSelectSlider { padding-bottom: 20px; }
    div[data-baseweb="slider"] { background-color: transparent; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DATA FETCHING ---
@st.cache_data(ttl=600)
def get_gold_data(period):
    try:
        gold = yf.Ticker("GC=F")
        df = gold.history(period=period)
        if df.empty:
            return None
        return df
    except Exception:
        return None

# --- UI LAYOUT ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h1>Gold</h1>", unsafe_allow_html=True)

# 1. Timeframe Selection (The Spectrum Slider)
# We use a select_slider to mimic the "1M, 6M, 1Y" buttons in Apple Stocks
timeframe_map = {
    "1 Month": "1mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y",
    "Maximum": "max"
}

selected_label = st.select_slider(
    label="Select Spectrum",
    options=list(timeframe_map.keys()),
    value="1 Year",
    label_visibility="collapsed" # Keeps it minimalist
)

period = timeframe_map[selected_label]
df = get_gold_data(period)

if df is not None:
    # Get prices for the display
    current_price = float(df['Close'].iloc[-1])
    prev_price = float(df['Close'].iloc[-2])
    change = current_price - prev_price
    pct_change = (change / prev_price) * 100
    
    color = "#32d74b" if change >= 0 else "#ff453a"

    # Price & Change Display
    st.markdown(f"""
        <div>
            <p class="price-text">${current_price:,.2f}</p>
            <p class="change-text" style="color: {color};">
                {"↑" if change >= 0 else "↓"} {abs(change):,.2f} ({abs(pct_change):.2f}%)
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Minimalist Apple-Style Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'], 
        mode='lines',
        line=dict(color='#ffffff', width=3),
        fill='tozeroy',
        fillcolor='rgba(255, 255, 255, 0.03)'
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350,
        xaxis=dict(showgrid=False, showticklabels=True, color="#8e8e93", nticks=5),
        yaxis=dict(showgrid=False, showticklabels=False, fixedrange=True),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown(f"<p style='text-align: center; color: #48484a; font-size: 12px; margin-top: 20px;'>Data: Yahoo Finance | View: {selected_label}</p>", unsafe_allow_html=True)

else:
    st.markdown("<br><br><h2 style='text-align: center; color: #ff453a;'>System Offline</h2>", unsafe_allow_html=True)
