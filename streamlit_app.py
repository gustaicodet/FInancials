import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- STABLE APPLE DESIGN ---
st.set_page_config(page_title="Gold Pro", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #000000; font-family: 'Inter', sans-serif; }
    .price-text { font-size: 52px; font-weight: 600; color: #ffffff; text-align: center; margin: 0; }
    .delta-text { font-size: 20px; text-align: center; margin-bottom: 30px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- STABLE DATA FETCH ---
@st.cache_data(ttl=600)
def get_data(p):
    return yf.Ticker("GC=F").history(period=p)

st.markdown("<h3 style='text-align: center; color: #8e8e93; font-weight: 400;'>Gold</h3>", unsafe_allow_html=True)

# Simple, stable timeframe selector
tf = st.radio("Timeframe", ["1mo", "6mo", "1y", "5y"], index=2, horizontal=True, label_visibility="collapsed")

df = get_data(tf)

if not df.empty:
    curr, prev = df['Close'].iloc[-1], df['Close'].iloc[-2]
    diff = curr - prev
    color = "#32d74b" if diff >= 0 else "#ff453a"
    
    st.markdown(f'<p class="price-text">${curr:,.2f}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="delta-text" style="color: {color};">{"↑" if diff >= 0 else "↓"} {abs(diff):.2f} ({(diff/prev)*100:.2f}%)</p>', unsafe_allow_html=True)

    fig = go.Figure(go.Scatter(x=df.index, y=df['Close'], line=dict(color='#ffffff', width=2), fill='tozeroy', fillcolor='rgba(255,255,255,0.05)'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0), height=300, 
                      xaxis=dict(showgrid=False, color="#48484a"), yaxis=dict(showgrid=False, showticklabels=False))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
