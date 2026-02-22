import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# ==========================================
# 1. PAGE SETUP & BRANDING
# ==========================================
st.set_page_config(page_title="The Safal Trader Scanner", page_icon="📈", layout="centered")

# ==========================================
# 2. LOGIN SYSTEM (SECURITY WALL)
# ==========================================
# Yahan aap apne clients ke ID aur Password set kar sakte hain
VALID_USERS = {
    "gursewak": "safal123",  # Aapki Admin ID
    "client1": "trade2026",  # Demo Client ID
}

# Session state check karna
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Agar Login NAHI hai, toh sirf Login Form dikhao
if not st.session_state['logged_in']:
    st.title("🔒 Login - The Safal Trader")
    st.markdown("Kripya Premium Scanner use karne ke liye apna **User ID** aur **Password** darj karein.")
    
    with st.form("login_form"):
        username = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state['logged_in'] = True
                st.success("✅ Login Successful! Loading dashboard...")
                time.sleep(1)
                st.rerun() # Page refresh karke main dashboard layega
            else:
                st.error("❌ Galat User ID ya Password. Kripya dobara try karein.")
                
    st.stop() # Yahan code ruk jayega agar login nahi hai toh

# ==========================================
# 3. MAIN DASHBOARD (Sirf Login walo ke liye)
# ==========================================
col1, col2 = st.columns([4, 1])
with col1:
    st.title("📈 The Safal Trader")
with col2:
    # Logout Button
    if st.button("Logout", key="logout_btn"):
        st.session_state['logged_in'] = False
        st.rerun()

st.subheader("Live Breakout & Breakdown Scanner")
st.markdown("Yeh premium tool live market data ko analyze karke high-probability setups dhoondhta hai. **Trade with logic, not magic.**")
st.divider()

# ==========================================
# 4. WATCHLIST
# ==========================================
WATCHLIST = [
    "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS", 
    "SBIN.NS", "ITC.NS", "TATAMOTORS.NS", "AXISBANK.NS", "ZOMATO.NS"
]

# ==========================================
# 5. SCANNER ENGINE
# ==========================================
if st.button("🚀 Start Live Scan", use_container_width=True):
    
    st.write(f"**Scan Started at:** {datetime.now().strftime('%H:%M:%S')}")
    progress_bar = st.progress(0)
    status_text = st.empty()
    results = []
    
    for i, symbol in enumerate(WATCHLIST):
        stock_name = symbol.replace(".NS", "")
        status_text.text(f"Scanning {stock_name}...")
        
        try:
            df = yf.download(symbol, period="5d", interval="5m", progress=False)
            if df.empty: continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            df['Vol_SMA'] = df['Volume'].rolling(20).mean()
            
            curr = df.iloc[-2]
            prev_high = df['High'].iloc[:-20].max()
            prev_low = df['Low'].iloc[:-20].min()
            
            if (curr['Close'] > prev_high) and (curr['Volume'] > curr['Vol_SMA']):
                results.append({"Stock": stock_name, "Signal": "🚀 BREAKOUT", "Price (₹)": round(curr['Close'], 2), "RSI": round(curr['RSI'], 2), "Volume Spike": f"{curr['Volume']/curr['Vol_SMA']:.1f}x"})
            elif (curr['Close'] < prev_low) and (curr['Volume'] > curr['Vol_SMA']):
                results.append({"Stock": stock_name, "Signal": "🔻 BREAKDOWN", "Price (₹)": round(curr['Close'], 2), "RSI": round(curr['RSI'], 2), "Volume Spike": f"{curr['Volume']/curr['Vol_SMA']:.1f}x"})
                
        except Exception as e:
            pass 
            
        progress_bar.progress((i + 1) / len(WATCHLIST))
        
    status_text.text("✅ Scan Complete!")
    
    st.divider()
    if len(results) > 0:
        st.success(f"{len(results)} Strong Signals Found!")
        result_df = pd.DataFrame(results)
        st.dataframe(result_df, use_container_width=True, hide_index=True)
    else:
        st.info("Abhi koi clear breakout ya breakdown nahi mila. Market sideways ho sakti hai. Thodi der baad dubara try karein.")

st.markdown("---")
st.caption("© 2026 The Safal Trader. All rights reserved. (For Educational Purposes Only)")