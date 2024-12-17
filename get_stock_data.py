#!/usr/bin/env python
import urllib.request
import csv
import yfinance as yf
from datetime import datetime, timedelta

urls = ['https://archives.nseindia.com/content/indices/ind_nifty100list.csv',
        'https://archives.nseindia.com/content/indices/ind_nifty500list.csv',
        'https://archives.nseindia.com/content/indices/ind_nifty50list.csv']

header_saved = False
symbols = []

# Download CSV files and merge them
for url in urls:
    response = urllib.request.urlopen(url)
    csv_data = response.read().decode('utf-8').splitlines()
    reader = csv.reader(csv_data)
    header = next(reader)
    if not header_saved:
        symbols_index = header.index('Symbol')
        header_saved = True
    for row in reader:
        symbols.append(row[symbols_index] + '.NS')

# Get historical data for last 3 months for each stock
start_date = datetime.today() - timedelta(days=90)
end_date = datetime.today()
for symbol in symbols:
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)
        filename = f"{symbol}.csv"
        data.to_csv(filename)
        print(f"{filename} downloaded successfully!")
    except:
        print(f"Failed to get data for {symbol}")

# Get today's data for each stock
for symbol in symbols:
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='1d')
        filename = f"{symbol}.csv"
        data.to_csv(filename, mode='a', header=False)
        print(f"{filename} updated with today's data!")
    except:
        print(f"Failed to update data for {symbol}")

print("All historical data downloaded and updated successfully!")
