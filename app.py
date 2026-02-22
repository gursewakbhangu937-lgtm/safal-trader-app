import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# ==========================================
# 1. PAGE SETUP & BRANDING
# ==========================================
st.set_page_config(page_title="The Safal Trader Pro", page_icon="📈", layout="wide")

# ==========================================
# 2. LOGIN SYSTEM (SECURITY WALL)
# ==========================================
VALID_USERS = {
    "gursewak": "safal123",  # Admin
    "client1": "trade2026",  # Demo Client
}

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔒 Login - The Safal Trader Pro")
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
                st.rerun()
            else:
                st.error("❌ Galat User ID ya Password. Kripya dobara try karein.")
    st.stop()

# ==========================================
# 3. MAIN DASHBOARD
# ==========================================
col1, col2 = st.columns([8, 1])
with col1:
    st.title("📈 The Safal Trader Pro - Auto Scanner")
with col2:
    if st.button("Logout", key="logout_btn"):
        st.session_state['logged_in'] = False
        st.session_state['auto_scan'] = False
        st.rerun()

st.markdown("Yeh premium tool 200+ high-volume stocks ko real-time analyze karta hai. **Trade with logic, not magic.**")
st.divider()

# ==========================================
# 2. WATCHLIST (TOP 220 HIGH VOLUME STOCKS - YAHOO FORMAT)
# ==========================================
MY_WATCHLIST = [
    # Top 50 (Nifty 50 Giants)
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "SBIN.NS", "INFY.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS", 
    "LT.NS", "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "ADANIENT.NS", "KOTAKBANK.NS", "TITAN.NS", "ONGC.NS", "TATAMOTORS.NS", 
    "NTPC.NS", "AXISBANK.NS", "ADANIPORTS.NS", "ULTRACEMCO.NS", "ASIANPAINT.NS", "COALINDIA.NS", "BAJAJFINSV.NS", "BAJAJ-AUTO.NS", "POWERGRID.NS", "NESTLEIND.NS", 
    "WIPRO.NS", "M&M.NS", "HAL.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "GRASIM.NS", "SBILIFE.NS", "BEL.NS", "LTIM.NS", "TRENT.NS", "INDUSINDBK.NS",
    "HINDALCO.NS", "CIPLA.NS", "DRREDDY.NS", "BRITANNIA.NS", "APOLLOHOSP.NS", "EICHERMOT.NS", "DIVISLAB.NS", "TECHM.NS",

    # Super Active Midcaps & Breakout Stocks
    "ZOMATO.NS", "PAYTM.NS", "JIOFIN.NS", "IRFC.NS", "IREDA.NS", "RVNL.NS", "SUZLON.NS", "IDEA.NS", "YESBANK.NS", "PNB.NS", 
    "BANKBARODA.NS", "UNIONBANK.NS", "CANBK.NS", "IDFCFIRSTB.NS", "IOB.NS", "MAHABANK.NS", "CENTRALBK.NS", "UCOBANK.NS", "INDIANB.NS", "PSB.NS",
    "PFC.NS", "RECLTD.NS", "GAIL.NS", "BPCL.NS", "IOC.NS", "HINDPETRO.NS", "NHPC.NS", "SJVN.NS", "BHEL.NS", "CGPOWER.NS", 
    "DLF.NS", "LODHA.NS", "OBEROIRLTY.NS", "GODREJPROP.NS", "PRESTIGE.NS", "TVSMOTOR.NS", "ASHOKLEY.NS", "MOTHERSON.NS", "BOSCHLTD.NS", "MRF.NS",
    "SIEMENS.NS", "ABB.NS", "CUMMINSIND.NS", "POLYCAB.NS", "HAVELLS.NS", "DIXON.NS", "KAYNES.NS", "AMBER.NS", "SYRMA.NS", "OLECTRA.NS",

    # Finance, AMC & Brokers
    "CHOLAFIN.NS", "BAJAJHLDNG.NS", "MUTHOOTFIN.NS", "MANAPPURAM.NS", "SHRIRAMFIN.NS", "M&MFIN.NS", "L&TFH.NS", "ABCAPITAL.NS", "POONAWALLA.NS", "HDFCAMC.NS", 
    "NAM-INDIA.NS", "UTIAMC.NS", "BSE.NS", "MCX.NS", "CDSL.NS", "CAMS.NS", "KFINTECH.NS", "ANGELONE.NS", "MOTILALOFS.NS", "ICICIGI.NS", "ICICIPRULI.NS",

    # Pharma & Chemicals
    "LUPIN.NS", "AUROPHARMA.NS", "ZYDUSLIFE.NS", "BIOCON.NS", "GLENMARK.NS", "TORNTPHARM.NS", "ALKEM.NS", "IPCALAB.NS", "SYNGENE.NS", "LAURUSLABS.NS",
    "SRF.NS", "PIIND.NS", "DEEPAKNTR.NS", "TATACHEM.NS", "AARTIIND.NS", "ATUL.NS", "NAVINFLUOR.NS", "COROMANDEL.NS", "FACT.NS", "GNFC.NS",

    # Defense, Railways & Shipyards (High Momentum)
    "MAZDOCK.NS", "COCHINSHIP.NS", "GRSE.NS", "BDL.NS", "TITAGARH.NS", "TEXRAIL.NS", "IRCON.NS", "RITES.NS", "RAILTEL.NS", "MIDHANI.NS",

    # Metals & Mining
    "VEDL.NS", "NMDC.NS", "NATIONALUM.NS", "SAIL.NS", "JINDALSTEL.NS", "HINDZINC.NS", "HINDCOPPER.NS", "JSL.NS", "WELCORP.NS", "APLAPOLLO.NS",

    # Retail, FMCG & Consumer Durables
    "DMART.NS", "TATACONSUM.NS", "GODREJCP.NS", "DABUR.NS", "MARICO.NS", "COLPAL.NS", "UBL.NS", "MCDOWELL-N.NS", "RADICO.NS", "DEVYANI.NS", 
    "JUBLFOOD.NS", "WESTLIFE.NS", "BATAINDIA.NS", "METROBRAND.NS", "PAGEIND.NS", "VOLTAS.NS", "BLUESTARCO.NS", "WHIRLPOOL.NS", "CROMPTON.NS", "KALYANKJIL.NS",

    # IT & Tech (Mid/Small Cap)
    "PERSISTENT.NS", "COFORGE.NS", "MPHASIS.NS", "TATAELXSI.NS", "KPITTECH.NS", "CYIENT.NS", "SONACOMS.NS", "PBFINTECH.NS", "DELHIVERY.NS", "NYKAA.NS"
]

# ==========================================
# 5. CONTROL PANEL & AUTO-SCAN LOGIC
# ==========================================
if 'auto_scan' not in st.session_state:
    st.session_state['auto_scan'] = False

st.subheader("⚙️ Control Panel")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🔍 Scan Now (Once)", use_container_width=True):
        st.session_state['run_once'] = True
with c2:
    if st.button("🚀 Start Auto-Scan (5 Min)", type="primary", use_container_width=True):
        st.session_state['auto_scan'] = True
with c3:
    if st.button("🛑 Stop Auto-Scan", use_container_width=True):
        st.session_state['auto_scan'] = False

# ==========================================
# 6. SCANNER ENGINE
# ==========================================
if st.session_state.get('run_once', False) or st.session_state['auto_scan']:
    st.session_state['run_once'] = False # Reset run once
    
    st.write(f"**Last Scan Completed At:** {datetime.now().strftime('%H:%M:%S')} (Scanning {len(WATCHLIST)} Stocks...)")
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
        except:
            pass 
        progress_bar.progress((i + 1) / len(WATCHLIST))
        
    status_text.text("✅ Scan Complete!")
    
    # Display Results
    if len(results) > 0:
        st.success(f"🔥 {len(results)} Strong Signals Found!")
        result_df = pd.DataFrame(results)
        st.dataframe(result_df, use_container_width=True, hide_index=True)
    else:
        st.info("Abhi koi clear breakout ya breakdown nahi mila. Market sideways ho sakti hai.")
        
    # Auto-Refresh Logic
    if st.session_state['auto_scan']:
        st.warning("⏳ Scanner is in Auto-Mode. Market will be scanned again in 5 minutes...")
        time.sleep(300) # 300 seconds = 5 minutes
        st.rerun()

st.markdown("---")
st.caption("© 2026 The Safal Trader. All rights reserved. (For Educational Purposes Only)")

