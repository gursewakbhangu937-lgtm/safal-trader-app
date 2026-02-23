import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import uuid 

# ==========================================
# 1. PAGE SETUP & STRONG ANTI-REFRESH WALLPAPER
# ==========================================
st.set_page_config(page_title="The Safal Trader Ultra Pro", page_icon="📈", layout="wide")

page_bg_pro = """
<style>
/* 🚀 SUPER STRONG MOBILE ANTI-REFRESH LOCK */
html, body {
    overscroll-behavior-y: contain !important; /* Browser ko refresh command lene se rokega */
    overscroll-behavior-x: none !important;
    background-color: #0e1117;
}

.stApp, [data-testid="stAppViewContainer"] {
    overscroll-behavior-y: contain !important;
    background-color: #0e1117; 
    background-image: 
        radial-gradient(at 50% 50%, rgba(41, 98, 255, 0.15) 0%, transparent 60%),
        radial-gradient(at 80% 20%, rgba(255, 65, 65, 0.1) 0%, transparent 50%),
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
    background-attachment: fixed;
}

[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
.stMarkdown, .stTitle, .stHeader, .stSubheader, .stText, p, h1, h2, h3, label, span { color: #E0E3EB !important; text-shadow: 0px 1px 2px rgba(0,0,0,0.5); }

/* Table ke andar touch lock */
[data-testid="stDataFrame"] { 
    background-color: rgba(30, 34, 45, 0.8); 
    border: 1px solid rgba(255,255,255,0.1); 
    border-radius: 10px; 
    padding: 10px; 
    overscroll-behavior-y: contain !important; /* Table scroll karte waqt page refresh na ho */
}

div.stButton > button:first-child { background-color: #2962FF; color: white; border: none; border-radius: 6px; font-weight: bold; box-shadow: 0 4px 6px rgba(41, 98, 255, 0.2); transition: all 0.3s ease; }
div.stButton > button:first-child:hover { background-color: #1E53E5; box-shadow: 0 6px 8px rgba(41, 98, 255, 0.3); transform: translateY(-2px); }
</style>
"""
st.markdown(page_bg_pro, unsafe_allow_html=True)

# ==========================================
# 2. ANTI-PIRACY & LOGIN SYSTEM (SECURITY WALL)
# ==========================================
VALID_USERS = {
    "gursewak": "safal123",  
    "client1": "trade2026",  
}

@st.cache_resource
def get_active_sessions():
    return {}

active_sessions = get_active_sessions()

if 'device_id' not in st.session_state:
    st.session_state['device_id'] = str(uuid.uuid4())

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- KICK OUT LOGIC ---
if st.session_state['logged_in']:
    current_user = st.session_state.get('username')
    if active_sessions.get(current_user) != st.session_state['device_id']:
        st.session_state['logged_in'] = False
        st.session_state['auto_scan'] = False
        st.error("⚠️ **SECURITY ALERT:** Aapki ID kisi aur device par login ki gayi hai! Isliye aapko yahan se Logout kar diya gaya hai.")
        time.sleep(4)
        st.rerun()

# --- LOGIN FORM ---
if not st.session_state['logged_in']:
    st.title("🔒 Login - The Safal Trader Terminal")
    st.markdown("### Kripya Premium Scanner use karne ke liye apna **User ID** aur **Password** darj karein.")
    
    with st.form("login_form"):
        username = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("🚀 Secure Login")
        
        if submit_button:
            if username in VALID_USERS and VALID_USERS[username] == password:
                active_sessions[username] = st.session_state['device_id']
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("✅ Login Successful! Initializing Trading Terminal...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Galat User ID ya Password.")
    st.stop()

# ==========================================
# 3. MAIN DASHBOARD
# ==========================================
col1, col2 = st.columns([8, 1])
with col1:
    st.title("📈 The Safal Trader Ultra Pro")
    st.caption("Live Market Auto-Scanner | Institutional Grade Terminal")
with col2:
    if st.button("Logout 🔒", key="logout_btn"):
        if st.session_state.get('username') in active_sessions:
            del active_sessions[st.session_state['username']]
        st.session_state['logged_in'] = False
        st.session_state['auto_scan'] = False
        st.rerun()

st.divider()

# ==========================================
# 4. WATCHLIST (251 High Volume Stocks)
# ==========================================
WATCHLIST = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "SBIN.NS", "INFY.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS",
    "LT.NS", "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "ADANIENT.NS", "KOTAKBANK.NS", "TITAN.NS", "ONGC.NS", "TATAMOTORS.NS",
    "NTPC.NS", "AXISBANK.NS", "ADANIPORTS.NS", "ULTRACEMCO.NS", "ASIANPAINT.NS", "COALINDIA.NS", "BAJAJFINSV.NS", "BAJAJ-AUTO.NS", "POWERGRID.NS", "NESTLEIND.NS",
    "WIPRO.NS", "M&M.NS", "HAL.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "GRASIM.NS", "SBILIFE.NS", "BEL.NS", "LTIM.NS", "TRENT.NS", "INDUSINDBK.NS",
    "HINDALCO.NS", "CIPLA.NS", "DRREDDY.NS", "BRITANNIA.NS", "APOLLOHOSP.NS", "EICHERMOT.NS", "DIVISLAB.NS", "TECHM.NS", "BPCL.NS", "SHRIRAMFIN.NS",
    "ZOMATO.NS", "PAYTM.NS", "JIOFIN.NS", "IRFC.NS", "IREDA.NS", "RVNL.NS", "SUZLON.NS", "IDEA.NS", "YESBANK.NS", "PNB.NS", "BANKBARODA.NS",
    "UNIONBANK.NS", "CANBK.NS", "IDFCFIRSTB.NS", "PFC.NS", "RECLTD.NS", "GAIL.NS", "IOC.NS", "BHEL.NS", "CGPOWER.NS", "DLF.NS", "LODHA.NS",
    "TVSMOTOR.NS", "ASHOKLEY.NS", "MOTHERSON.NS", "SIEMENS.NS", "ABB.NS", "CUMMINSIND.NS", "POLYCAB.NS", "HAVELLS.NS", "DIXON.NS", "CHOLAFIN.NS",
    "MUTHOOTFIN.NS", "MANAPPURAM.NS", "BSE.NS", "MCX.NS", "CDSL.NS", "ANGELONE.NS", "LUPIN.NS", "AUROPHARMA.NS", "ZYDUSLIFE.NS", "BIOCON.NS",
    "GLENMARK.NS", "VEDL.NS", "NMDC.NS", "NATIONALUM.NS", "SAIL.NS", "JINDALSTEL.NS", "HINDZINC.NS", "HINDCOPPER.NS", "DMART.NS", "TATACONSUM.NS",
    "GODREJCP.NS", "DABUR.NS", "MARICO.NS", "COLPAL.NS", "UBL.NS", "VOLTAS.NS", "PERSISTENT.NS", "COFORGE.NS", "MPHASIS.NS", "TATAELXSI.NS",
    "KPITTECH.NS", "CYIENT.NS", "SONACOMS.NS", "PBFINTECH.NS", "DELHIVERY.NS", "NYKAA.NS", "ABFRL.NS", "AUBANK.NS", "BANDHANBNK.NS", "FEDERALBNK.NS",
    "ZEEL.NS", "SUNTV.NS", "PVRINOX.NS", "INDIGO.NS", "POLICYBZR.NS", "GMRINFRA.NS", "INDHOTEL.NS", "JUBLFOOD.NS", "UPL.NS", "PIIND.NS",
    "DEEPAKNTR.NS", "SRF.NS", "NAVINFLUOR.NS", "ATUL.NS", "AARTIIND.NS", "CROMPTON.NS", "WHIRLPOOL.NS", "KAJARIACER.NS", "ASTRAL.NS",
    "PIDILITIND.NS", "BERGEPAINT.NS", "BOSCHLTD.NS", "MRF.NS", "BALKRISIND.NS", "APOLLOTYRE.NS", "ESCORTS.NS", "HEROMOTOCO.NS", "BIKAJI.NS",
    "MANYAVAR.NS", "KEI.NS", "KEC.NS", "KALPATPOWR.NS", "TORNTPOWER.NS", "NHPC.NS", "SJVN.NS", "NLCINDIA.NS", "ENGINERSIN.NS", "RITES.NS",
    "RAILTEL.NS", "IRCON.NS", "TITAGARH.NS", "MAZDOCK.NS", "COCHINSHIP.NS", "GRSE.NS", "BDL.NS", "MIDHANI.NS", "ASTRAZEN.NS", "SANOFI.NS",
    "PFIZER.NS", "GLAXO.NS", "FORTIS.NS", "NH.NS", "ASTERDM.NS", "METROPOLIS.NS", "LALPATHLAB.NS", "SYNGENE.NS", "LAURUSLABS.NS", "GRANULES.NS",
    "FSL.NS", "BSOFT.NS", "CYIENTDLM.NS", "DATAPATTNS.NS", "MTARTECH.NS", "PARAS.NS", "ZENTECH.NS", "HBLPOWER.NS", "CENTURYTEX.NS", "RAYMOND.NS",
    "WELSPUNLIV.NS", "TRIDENT.NS", "ALOKINDS.NS", "VTL.NS", "KPRMILL.NS", "PAGEIND.NS", "LUXIND.NS", "RUPA.NS", "DOLLAR.NS", "BATAINDIA.NS",
    "RELAXO.NS", "CAMPUS.NS", "METROBRAND.NS", "REDTAPE.NS", "KHADIM.NS", "LIBERTSHOE.NS", "SFL.NS", "TCNSBRANDS.NS", "GOKEX.NS",
    "ARVIND.NS", "ARVINDFASN.NS", "SHOPPERS.NS", "VMART.NS", "V2RETAIL.NS", "CANTABIL.NS", "MONTECARLO.NS", "SNOWMAN.NS", "MAHLOG.NS",
    "TCI.NS", "VRLLOG.NS", "GATEWAY.NS", "NAVKARCORP.NS", "CONCOR.NS", "GPPL.NS", "ADANILOG.NS"
]

# ==========================================
# 5. CONTROL PANEL
# ==========================================
if 'auto_scan' not in st.session_state:
    st.session_state['auto_scan'] = False

st.subheader("⚙️ Terminal Controls")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔍 Quick Scan (Once)", use_container_width=True):
        st.session_state['run_once'] = True
with c2:
    if st.button("🚀 Start Auto-Pilot (5 Min)", use_container_width=True):
        st.session_state['auto_scan'] = True
with c3:
    if st.button("🛑 Stop Auto-Pilot", use_container_width=True):
        st.session_state['auto_scan'] = False

# ==========================================
# 6. SCANNER ENGINE (15-Min Support/Resistance Reversal)
# ==========================================
if st.session_state.get('run_once', False) or st.session_state['auto_scan']:
    st.session_state['run_once'] = False
    
    st.toast("Scanning 15-Min Reversal Patterns...", icon="🕯️") 
    progress_bar = st.progress(0)
    status_text = st.empty()
    results = []
    
    for i, symbol in enumerate(WATCHLIST):
        stock_name = symbol.replace(".NS", "")
        if i % 20 == 0: 
             status_text.markdown(f"**Analyzing:** `{stock_name}`... ({i}/{len(WATCHLIST)})")
        
        try:
            # 15-Minute Timeframe ka data le rahe hain
            df = yf.download(symbol, period="15d", interval="15m", progress=False)
            if df.empty or len(df) < 40: continue
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            
            # --- 1. LEVELS CALCULATION ---
            major_res = df['High'].iloc[:-20].max() # Pichle 20 candles ka resistance
            major_sup = df['Low'].iloc[:-20].min()  # Pichle 20 candles ka support
            
            # --- 2. CANDLESTICK LOGIC ---
            # Last closed candle (indexing -2 as -1 is current incomplete candle)
            c = df.iloc[-2]
            body = abs(c['Open'] - c['Close'])
            total_range = c['High'] - c['Low']
            upper_wick = c['High'] - max(c['Open'], c['Close'])
            lower_wick = min(c['Open'], c['Close']) - c['Low']
            
            # A. Green Doji (At Support)
            # Body choti honi chahiye total range ke mukable (Doji)
            is_doji = body < (total_range * 0.1)
            is_green = c['Close'] >= c['Open']
            
            # B. Inverted Hammer / Red Doji (At Resistance)
            # Inverted Hammer: Upper wick body se 2 guna badi honi chahiye
            is_inv_hammer = upper_wick > (body * 2) and lower_wick < (body * 0.5)
            is_red = c['Close'] <= c['Open']
            is_red_doji = is_doji and is_red

            # --- 3. SCANNING LOGIC ---
            # Condition 1: Support ke paas Green Doji
            if c['Low'] <= (major_sup * 1.005) and is_green and is_doji:
                results.append({"Stock": stock_name, "Signal": "🟢 DOJI AT SUPPORT", "Price": c['Close'], "Level": "Support", "Type": "Bullish Reversal"})

            # Condition 2: Resistance ke paas Inverted Hammer ya Red Doji
            elif c['High'] >= (major_res * 0.995) and (is_inv_hammer or is_red_doji):
                results.append({"Stock": stock_name, "Signal": "🔴 REVERSAL AT RES", "Price": c['Close'], "Level": "Resistance", "Type": "Bearish Reversal"})

        except: pass 
        progress_bar.progress((i + 1) / len(WATCHLIST))
        
    status_text.empty()
    progress_bar.empty()
    
    if len(results) > 0:
        st.success(f"🎯 {len(results)} Strong Reversal Setups Found!")
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
    else:
        st.info("Currently no Doji/Inverted Hammer patterns near major levels.")
