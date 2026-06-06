import streamlit as st
import requests
import time
from datetime import datetime

# ==========================================
# ⚙️ CONFIGURATION & TARGET ENDPOINTS
# ==========================================
# MUST match the exact Firebase URL used in your local_trader.py script
FIREBASE_URL = "https://your-project-id-default-rtdb.firebaseio.com/engine_state.json"

# Set up clean institutional page parameters
st.set_page_config(
    page_title="US30 Elite Terminal",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom injection to give the UI a dark, sleek proprietary feel
st.markdown("""
    <style>
        .reportview-container { background: #0e1117; }
        .metric-box {
            background-color: #161b22;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #30363d;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🌌 DASHBOARD HEADER & TITLE ASSEMBLY
# ==========================================
st.title("🦅 US30 Institutional Automation Node")
st.markdown("---")

# ==========================================
# 🛰️ REAL-TIME REMOTE DATA HANDSHAKE
# ==========================================
try:
    # Query the free Google Realtime Database
    response = requests.get(FIREBASE_URL, timeout=3)
    
    if response.status_code == 200 and response.json() is not None:
        data = response.json()
        
        # Extract fields with safe default fallbacks
        daily_pnl = data.get("daily_pnl", 0.0)
        weekly_pnl = data.get("weekly_pnl", 0.0)
        sentiment = data.get("sentiment", 0)
        status = data.get("status", "UNKNOWN_OFFLINE")
        timestamp_str = data.get("timestamp", "N/A")
        
        # ------------------------------------------
        # 🟢 ROW 1: CORE SYSTEM METRICS & PNL CARDS
        # ------------------------------------------
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Format Daily PnL color dynamically based on account balance performance
            pnl_color = "🟢" if daily_pnl >= 0 else "🔴"
            st.metric(
                label=f"{pnl_color} Daily Net Profit/Loss",
                value=f"${daily_pnl:,.2f}",
                delta=f"{((daily_pnl / 50000.0) * 100):.2f}% vs $50k Base Account"
            )
            
        with col2:
            st.metric(
                label="📊 Weekly Cumulative Curve",
                value=f"${weekly_pnl:,.2f}",
                delta=f"Cap Target Allocation: $1,000.00"
            )
            
        with col3:
            # Translate raw macro integer score into standard reading
            sentiment_label = "NEUTRAL"
            if sentiment >= 4:
                sentiment_label = "STRONG BULLISH MATRIX"
            elif sentiment <= -4:
                sentiment_label = "STRONG BEARISH MATRIX"
            elif sentiment > 0:
                sentiment_label = "MILDLY BULLISH"
            elif sentiment < 0:
                sentiment_label = "MILDLY BEARISH"
                
            st.metric(
                label="📡 Macro Alpha Intelligence Bias",
                value=f"Score: {sentiment}",
                delta=sentiment_label,
                delta_color="normal" if sentiment != 0 else "off"
            )
            
        st.markdown("---")
        
        # ------------------------------------------
        # 🟠 ROW 2: ENGINE SYSTEM STATUS ALERTS
        # ------------------------------------------
        st.subheader("🛡️ Executive Guardrail Management Console")
        
        # Color match specific status signals to clear dashboard visibility profiles
        if "BREACHED" in status or "HALTED" in status:
            st.error(f"🛑 CRITICAL ALGORITHM STATE TRIGGERED: {status}")
            st.sidebar.warning("Action Required: Risk parameters triggered a hard layout closure.")
        elif "PAUSED" in status or "LIMIT_SECURED" in status:
            st.success(f"🎉 CELEBRATION PROTOCOL ACTIVE: {status}")
        elif "NEWS_BLOCK" in status:
            st.warning(f"⚠️ MACRO FILTER INTERVENTION: {status}")
        else:
            st.info(f"⚡ SYSTEM METRICS CLEAR: {status}")
            
        # ------------------------------------------
        # 🔵 ROW 3: DATABASE HEARTBEAT & AUDIT TRAIL
        # ------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption(f"🔒 Secure Google Firebase Database Heartbeat Loop Active | Remote Node Last Ping: **{timestamp_str}**")
        
        # Calculate latency verification window
        try:
            last_ping_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            time_delta = (datetime.now() - last_ping_time).total_seconds()
            if time_delta > 10:
                st.sidebar.error(f"⚠️ Remote execution engine communication lag detected! Last trace: {int(time_delta)}s ago.")
            else:
                st.sidebar.success("📡 Cloud Pipeline: 100% Operational Latency Balanced")
        except:
            pass

    else:
        # State display if database exists but contains empty root keys
        st.warning("🔄 Link established with Google Firebase. Waiting for local_trader.py script to broadcast first account snapshot...")
        st.info("Ensure your home computer terminal script is running and your WebRequest firewall settings are cleared inside MetaTrader 5.")

except Exception as connection_error:
    # Comprehensive failover block if network drops or initialization keys mismatch
    st.error("❌ Google Cloud Stream Handshake Failure")
    st.markdown(f"**Diagnostic Tracking Trace:** `{connection_error}`")
    st.markdown("---")
    st.info("💡 **Quick Deployment Checklist:** Check if your unique Firebase project subdomain ID matches your hardcoded variable assignment string inside this file.")

# ==========================================
# 🔄 AUTOMATIC ENGINE RERUN TIMING LOOP
# ==========================================
# Restricts query pacing to 2-second windows to conform to Google's Always-Free processing limits
time.sleep(2)
st.rerun()
