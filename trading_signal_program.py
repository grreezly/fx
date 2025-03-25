import ccxt
import sys
print(sys.path)
import pandas as pd
print(pd.__version__)
import time
import talib
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



# Initialize exchange
exchange = ccxt.binance()

def fetch_data(symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def compute_indicators(df):
    df['RSI'] = talib.RSI(df['close'], timeperiod=14)
    df['SMA'] = talib.SMA(df['close'], timeperiod=50)
    return df

def create_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def process_real_time(symbol, timeframe):
    while True:
        df = fetch_data(symbol, timeframe)
        df = compute_indicators(df)
        inputs = df[['close', 'RSI', 'SMA']].values[-100:]
        inputs = np.reshape(inputs, (1, inputs.shape[0], inputs.shape[1]))
        signal = model.predict(inputs)
        print(f"Predicted signal: {signal}")
        time.sleep(exchange.parse_timeframe(timeframe))

def animate(i, symbol, timeframe):
    df = fetch_data(symbol, timeframe)
    df = compute_indicators(df)
    plt.cla()
    plt.plot(df['timestamp'], df['close'], label='Close')
    plt.plot(df['timestamp'], df['SMA'], label='SMA')
    plt.scatter(df['timestamp'], df['RSI'], label='RSI', color='red')
    plt.legend(loc='upper left')
    plt.tight_layout()

# Main program
symbols = ['EUR/USD', 'GBP/USD', 'XAU/USD']
timeframes = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1w', '1M']

print("Available symbols: ", symbols)
print("Available timeframes: ", timeframes)

chosen_symbol = input("Please choose a symbol from the above list: ")
chosen_timeframe = input("Please choose a timeframe from the above list: ")

input_shape = (100, 3)
model = create_model(input_shape)

ani = FuncAnimation(plt.gcf(), animate, fargs=(chosen_symbol, chosen_timeframe), interval=60000)
plt.show()

process_real_time(chosen_symbol, chosen_timeframe)