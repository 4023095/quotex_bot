import streamlit as st
import pandas as pd
import ta
import random
import time

st.set_page_config(page_title="Quotex Signal Bot", layout="centered")

st.title("📊 Quotex RSI Signal Bot")

pair = st.selectbox("🔽 Select Pair", ["EUR/USD OTC", "GBP/JPY", "AUD/CAD", "USD/JPY"])
timeframe = st.radio("🕐 Select Timeframe", ["1m", "5m", "15m"])
start = st.button("▶️ Start Signal Bot")

def get_simulated_candles():
    candles = []
    for _ in range(50):
        open_price = random.uniform(1.0500, 1.1500)
        close_price = open_price + random.uniform(-0.005, 0.005)
        candles.append({"open": open_price, "close": close_price})
    return pd.DataFrame(candles)

def apply_rsi(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    latest_rsi = df['rsi'].iloc[-1]
    if latest_rsi < 30:
        return "CALL (UP) 📈", latest_rsi
    elif latest_rsi > 70:
        return "PUT (DOWN) 📉", latest_rsi
    else:
        return "NO SIGNAL ⚪", latest_rsi

if start:
    st.success(f"Started signal bot for {pair} | TF: {timeframe}")
    while True:
        with st.spinner("⏳ Waiting 45 seconds..."):
            time.sleep(45)
        df = get_simulated_candles()
        signal, rsi_value = apply_rsi(df)
        st.write(f"🔔 **Signal for {pair} ({timeframe})**: `{signal}` | RSI: {round(rsi_value, 2)}")
