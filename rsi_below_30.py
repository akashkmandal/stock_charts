#!/usr/bin/python3
import pandas as pd
import mplfinance as mpf
import os
import random

data_path = "./"

rsi_period = 30
rsi_threshold = 30
rsi_near_threshold = 2  # 2% range around the RSI threshold

# Function to calculate RSI
def calculate_rsi(data, period):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

valid_dfs = []
for filename in os.listdir(data_path):
    if filename.endswith(".NS.csv"):
        df = pd.read_csv(os.path.join(data_path, filename))
        stock_name = os.path.splitext(os.path.basename(filename))[0]
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        df['RSI'] = calculate_rsi(df['Close'], rsi_period)
        
        # Check if the latest RSI is below the threshold or near it within 2%
        last_rsi = df['RSI'].iloc[-1]
        if last_rsi < rsi_threshold or abs(last_rsi - rsi_threshold) <= rsi_near_threshold:
            valid_dfs.append((df, stock_name))

random.shuffle(valid_dfs)  # Shuffle the valid_dfs list in random order

# Plot the charts for valid stocks
for df, stock_name in valid_dfs:
    mpf.plot(df, type='candle', volume=True, title=f"{stock_name} - Near 30 RSI Strategy", figsize=(15, 10))
