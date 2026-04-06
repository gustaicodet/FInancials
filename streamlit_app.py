import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- SYSTEM CONFIG & APPLE-INSPIRED CSS ---
st.set_page_config(page_title="Gold Pro", layout="centered")

# Custom CSS for deep black background, modern fonts, pill buttons, and centered layout
st.markdown("""
    <style>
    /* 1. Deep OLED Black Background and Clean Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    .stApp {
        background-color: #000000;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 2. Centered Content Block with Breathing Room */
    .block-container {
        padding-top: 5rem;
        max-width: 450px;
        margin: auto;
    }

    /* 3. Style Header Section (Title & Price) */
    .title-text {
        text-align: center;
        font-weight: 500;
        font-size: 16px;
        color: #8e8e93; /* Apple Gray */
        margin-bottom: 5px;
    }

    .price-large {
        text-align: center;
        font-size: 56px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -2px;
        margin: 0;
        line-height: 1;
    }

    .delta-text {
        text-align: center;
        font-size: 20px;
        font-weight: 500;
        margin-top: 5px;
        margin-bottom: 40px;
    }

    /* 4. Style Timeframe Pills (Streamlit Segmented Control) */
    div[data-testid="stSegmentedControl"] {
        display: flex;
        justify-content: center;
        background-color: #1c1c1e; /* Deep Gray Card */
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
        background-color: #3a3a3c !important; /* Selected Pill */
        border-radius: 8px !important;
    }

    /* 5. Clean Chart and Footer */
    .stPlotlyChart { margin-top: 20px; }
    
    #MainMenu, footer, header { visibility: hidden; } /* Hide clutter */
    </style>
    """, unsafe_allow_html=True)

# --- ROBUST DATA FETCHING (yfinance) ---
@st.cache_data(ttl=600) # Updates every 10 minutes
def fetch_gold_data(period):
    try:
        gold = yf.Ticker("GC=F")
        df = gold.history(period=period)
        if df.empty:
            return None
        return df
    except Exception:
        return None

# --- UI LAYOUT ---
st.markdown('<p class="title-text">Gold (GC=F)</p>', unsafe_allow_html=True)

# 1. Timeframe Selection (Segmented Control / Pills)
timeframe_options = ["1M", "6M", "1Y", "5Y", "All"]
timeframe_map = {"1M": "1mo", "6M": "6mo", "1Y": "1y", "5Y": "5y", "All": "max"}

selected_tf = st.segmented_control(
    "Timeframe", 
    options=timeframe_options, 
    default="1Y", 
    label_visibility="collapsed"
)

df = fetch_gold_data(timeframe_map[selected_tf])

if df is not None:
    # --- METRICS CALCULATIONS ---
    current = float(df['Close'].iloc[-1])
    prev = float(df['Close'].iloc[-2])
    diff = current - prev
    pct = (diff / prev) * 100
    color = "#32d74b" if diff >= 0 else "#ff453a" # Apple Green / Apple Red

    # 2. Display Price & Change
    st.markdown(f'<p class="price-large">${current:,.2f}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="delta-text" style="color: {color};">{"↑" if diff >= 0 else "↓"} {abs(diff):.2f} ({abs(pct):.2f}%)</p>', unsafe_allow_html=True)

    # 3. Clean, High-End Plotly Chart
    fig = go.Figure()
    
    # Add the price line with a smooth curve (spline) and a white/transparent gradient fill
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'],
        mode='lines',
        line=dict(color='#ffffff', width=2.5, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(255, 255, 255, 0.04)' # Light-box gradient effect
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

    # Render the chart using st.plotly_chart
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # 4. Footer Section (Metadata)
    st.markdown(f"<p style='text-align: center; color: #48484a; font-size: 11px; margin-top: 50px;'>Source: Yahoo Finance | Updated: {datetime.now().strftime('%H:%M')}</p>", unsafe_allow_html=True)

else:
    st.markdown("<h2 style='text-align: center; color: #ff453a; margin-top: 100px;'>System Offline</h2>", unsafe_allow_html=True)
    st.info("The market data provider is currently unresponsive. This usually resolves in a few minutes.")
