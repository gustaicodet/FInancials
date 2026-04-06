import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- APPLE DESIGN CONFIG ---
st.set_page_config(page_title="Gold Pro", layout="centered")

# Custom CSS for Apple Aesthetic (Clean, Rounded, Subtle Shadows)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    /* Main Background */
    .stApp {
        background-color: #000000;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Card Styling */
    .metric-card {
        background: #1c1c1e;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #2c2c2e;
        margin-bottom: 20px;
    }

    /* Clean Typography */
    h1 {
        font-weight: 600;
        letter-spacing: -1px;
        color: #ffffff;
    }
    
    .price-text {
        font-size: 48px;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
    }

    .change-text {
        font-size: 20px;
        font-weight: 400;
        margin-top: -5px;
    }

    /* Hide Streamlit elements for a "Clean App" feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DATA FETCHING ---
@st.cache_data(ttl=300)
def get_gold_data():
    df = yf.download("GC=F", period="1y", interval="1d")
    return df

try:
    df = get_gold_data()
    current_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    change = current_price - prev_price
    pct_change = (change / prev_price) * 100
    
    color = "#32d74b" if change >= 0 else "#ff453a" # Apple Green / Apple Red

    # --- UI LAYOUT ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Title
    st.markdown("<h1 style='text-align: center;'>Gold</h1>", unsafe_allow_html=True)

    # Price Card
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 40px;">
            <p class="price-text">${current_price:,.2f}</p>
            <p class="change-text" style="color: {color};">
                {"↑" if change >= 0 else "↓"} {abs(change):,.2f} ({abs(pct_change):.2f}%)
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Close'], 
        mode='lines',
        line=dict(color='#ffffff', width=3),
        fill='tozeroy',
        fillcolor='rgba(255, 255, 255, 0.05)' # Subtle gradient-like fill
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        xaxis=dict(showgrid=False, showticklabels=True, color="#8e8e93"),
        yaxis=dict(showgrid=False, showticklabels=False),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown(f"<p style='text-align: center; color: #8e8e93; font-size: 12px; margin-top: 50px;'>Last updated: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

except Exception as e:
    st.error("Market data currently unavailable.")
