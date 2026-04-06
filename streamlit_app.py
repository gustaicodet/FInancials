import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="Sovereign HUD", layout="centered")

# --- MINIMALIST DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #000000; font-family: 'Inter', sans-serif; color: white; }
    .price-text { font-size: 48px; font-weight: 600; text-align: center; margin: 0; }
    .sub-text { font-size: 14px; color: #8e8e93; text-align: center; text-transform: uppercase; letter-spacing: 1px; }
    .runway-box { background-color: #1c1c1e; border-radius: 15px; padding: 25px; margin: 20px 0; border: 1px solid #2c2c2e; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUT ---
st.sidebar.title("Settings")
current_wealth = st.sidebar.number_input("Your Current Portfolio (€)", value=15000, step=1000)
monthly_goal = 1500 # Your target rent/lifestyle

# --- DATA FETCHING ---
@st.cache_data(ttl=600)
def get_gold():
    return yf.Ticker("GC=F").history(period="1y")

df = get_gold()

# --- DASHBOARD ---
st.markdown("<br><p class='sub-text'>Global Value Proxy</p>", unsafe_allow_html=True)

if not df.empty:
    curr = df['Close'].iloc[-1]
    st.markdown(f"<p class='price-text'>${curr:,.2f}</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>Gold / Ounce</p>", unsafe_allow_html=True)

    # --- THE RUNWAY CALCULATOR ---
    # Math: (Portfolio * 4%) / 12 = Monthly Passive. 
    # (Monthly Passive / Monthly Goal) * 30 = Days secured.
    annual_passive = current_wealth * 0.04
    monthly_passive = annual_passive / 12
    days_secured = (monthly_passive / monthly_goal) * 30
    
    st.markdown("<div class='runway-box'>", unsafe_allow_html=True)
    st.write(f"### 🔓 Freedom Runway")
    st.write(f"Your current portfolio secures **{days_secured:.1f} days** of your 1,500€ dream lifestyle every month.")
    st.progress(min(days_secured / 30, 1.0))
    st.write(f"Passive Income: **{monthly_passive:.2f}€ / {monthly_goal}€**")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- MINIMALIST CHART ---
    fig = go.Figure(go.Scatter(x=df.index, y=df['Close'], line=dict(color='#ffffff', width=2), fill='tozeroy', fillcolor='rgba(255,255,255,0.05)'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0), height=250, 
                      xaxis=dict(showgrid=False, color="#48484a"), yaxis=dict(showgrid=False, showticklabels=False))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
