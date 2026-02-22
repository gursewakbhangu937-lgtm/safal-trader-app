import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# ==========================================
# 1. PAGE SETUP & ZERO-LAG TRADING THEME
# ==========================================
st.set_page_config(page_title="The Safal Trader Ultra Pro", page_icon="📈", layout="wide")

# --- CUSTOM CSS FOR ZERO-LAG TRADING THEME ---
page_bg_color = """
<style>
/* TradingView Dark Theme Background with Grid */
[data-testid="stAppViewContainer"] {
    background-color: #131722;
    background-image: 
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 30px 30px;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

/* Premium Text Colors */
.stMarkdown, .stTitle, .stHeader, .stSubheader, .stText, p, h1, h2, h3, label {
    color: #E0E3EB !important;
}

/* Make tables and success/info boxes look good in dark mode */
[data-testid="stDataFrame"] {
    background-color: #1E222D;
    border-radius: 8px;
    padding: 10px;
}

div.stButton > button:first-child {
    background-color: #2962FF;
    color: white;
    border: none;
    border-radius: 5px;
    font-weight: bold;
}
div.stButton > button:first-child:hover {
    background-color: #1E53E5;
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)
# -------------------------------------------

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
    st.title("🔒 Login - The Safal Trader Terminal")
    st.markdown("### Kripya Premium Scanner use karne ke liye apna **User ID** aur **Password** darj karein.")
    
    with st.form("login_form"):
        username = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("🚀 Secure Login")
        
        if submit_button:
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state['logged_in'] = True
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
    st.title("📈 The Safal Trader Terminal")
    st.caption("Live Market Auto-Scanner | 250+ High Volume Stocks")
with col2:
    if st.button("Logout 🔒", key="logout_btn"):
        st.session_state['logged_in'] = False
        st.session_state['auto_scan'] = False
        st.rerun()

st.divider()

# ==========================================
# 4. EXPANDED WATCHLIST (251 High Volume Stocks)
# ==========================================
WATCHLIST = [
    # Nifty 50 & Major Large Caps
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "SBIN.NS", "INFY.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS",
    "LT.NS", "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "ADANIENT.NS", "KOTAKBANK.NS", "TITAN.NS", "ONGC.NS", "TATAMOTORS.NS",
    "NTPC.NS", "AXISBANK.NS", "ADANIPORTS.NS", "ULTRACEMCO.NS", "ASIANPAINT.NS", "COALINDIA.NS", "BAJAJFINSV.NS", "BAJAJ-AUTO.NS", "POWERGRID.NS", "NESTLEIND.NS",
    "WIPRO.NS", "M&M.NS", "HAL.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "GRASIM.NS", "SBILIFE.NS", "BEL.NS", "LTIM.NS", "TRENT.NS", "INDUSINDBK.NS",
    "HINDALCO.NS", "CIPLA.NS", "DRREDDY.NS", "BRITANNIA.NS", "APOLLOHOSP.NS", "EICHERMOT.NS", "DIVISLAB.NS", "TECHM.NS", "BPCL.NS", "SHRIRAMFIN.NS",
    # High Momentum Midcaps & F&O Stocks
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
    if st.button("🚀 Start Auto-Pilot (5 Min)", use_container_width=True, help="Har 5 minute mein apne aap scan karega."):
        st.session_state['auto_scan'] = True
with c3:
    if st.button("🛑 Stop Auto-Pilot", use_container_width=True):
        st.session_state['auto_scan'] = False

# ==========================================
# 6. SCANNER ENGINE & PRO RESULTS
# ==========================================
if st.session_state.get('run_once', False) or st.session_state['auto_scan']:
    st.session_state['run_once'] = False
    
    st.toast(f"Market Scan Initiated: {len(WATCHLIST)} Stocks...", icon="⚡") 
    progress_bar = st.progress(0)
    status_text = st.empty()
    results = []
    
    for i, symbol in enumerate(WATCHLIST):
        stock_name = symbol.replace(".NS", "")
        if i % 10 == 0: 
             status_text.markdown(f"**Scanning:** `{stock_name}` ({i+1}/{len(WATCHLIST)})")
        
        try:
            df = yf.download(symbol, period="5d", interval="5m", progress=False)
            if df.empty: continue
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean(); loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss; df['RSI'] = 100 - (100 / (1 + rs))
            df['Vol_SMA'] = df['Volume'].rolling(20).mean()
            
            curr = df.iloc[-2]; prev_high = df['High'].iloc[:-20].max(); prev_low = df['Low'].iloc[:-20].min()
            
            if (curr['Close'] > prev_high) and (curr['Volume'] > curr['Vol_SMA']):
                results.append({"Stock": stock_name, "Signal": "🚀 BREAKOUT", "Price (₹)": curr['Close'], "RSI": int(curr['RSI']), "Volume Spike": f"{curr['Volume']/curr['Vol_SMA']:.1f}x"})
            elif (curr['Close'] < prev_low) and (curr['Volume'] > curr['Vol_SMA']):
                results.append({"Stock": stock_name, "Signal": "🔻 BREAKDOWN", "Price (₹)": curr['Close'], "RSI": int(curr['RSI']), "Volume Spike": f"{curr['Volume']/curr['Vol_SMA']:.1f}x"})
        except: pass 
        progress_bar.progress((i + 1) / len(WATCHLIST))
        
    status_text.empty()
    progress_bar.empty()
    st.toast("Scan Complete!", icon="✅")
    
    # === PRO RESULTS DISPLAY ===
    if len(results) > 0:
        st.success(f"🔥 {len(results)} High-Momentum Signals Found!")
        result_df = pd.DataFrame(results)
        
        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Signal": st.column_config.TextColumn("Signal", help="Trade Direction"),
                "RSI": st.column_config.ProgressColumn(
                    "RSI Strength", help="Relative Strength Index (0-100)", format="%d", min_value=0, max_value=100,
                ),
                 "Price (₹)": st.column_config.NumberColumn("Price (₹)", format="₹%.2f"),
            }
        )
    else:
        st.info("Currently No High-Probability Setups. Market might be sideways.")
        
    if st.session_state['auto_scan']:
        st.warning("⏳ Auto-Pilot Active. Next scan in 5 minutes...")
        time.sleep(300)
        st.rerun()

st.divider()
st.markdown("<h5 style='text-align: center; color: #50535e;'>© 2026 The Safal Trader | Institutional Terminal</h5>", unsafe_allow_html=True)
