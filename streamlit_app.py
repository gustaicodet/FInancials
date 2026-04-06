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
    h1 { font-weight: 600; letter-spacing: -1px; color: #ffffff; text-align: center; }
    .price-text { font-size: 56px; font-weight: 600; color: #ffffff; margin: 0; text-align: center; }
    .change-text { font-size: 24px; font-weight: 400; margin-top: -5px; text-align: center; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- ROBUST DATA FETCHING ---
@st.cache_data(ttl=600)
def get_gold_data():
    try:
        gold = yf.Ticker("GC=F")
        df = gold.history(period="1y")
        if df.empty:
            return None
        return df
    except Exception:
        return None

df = get_gold_data()

if df is not None:
    # Get the most recent valid prices
    current_price = float(df['Close'].iloc[-1])
    prev_price = float(df['Close'].iloc[-2])
    change = current_price - prev_price
    pct_change = (change / prev_price) * 100
    
    color = "#32d74b" if change >= 0 else "#ff453a"

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1>Gold</h1>", unsafe_allow_html=True)

    # Price & Change Display
    st.markdown(f"""
        <div style="margin-bottom: 40px;">
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
    
    st.markdown(f"<p style='text-align: center; color: #48484a; font-size: 12px; margin-top: 40px;'>Data: Yahoo Finance | Updated {datetime.now().strftime('%H:%M')}</p>", unsafe_allow_html=True)

else:
    st.markdown("<br><br><h2 style='text-align: center; color: #ff453a;'>System Offline</h2>", unsafe_allow_html=True)
    st.info("The market data provider is currently unresponsive. This usually resolves in a few minutes.")
