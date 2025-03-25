import ccxt
import pandas as pd
import time

# Initialize exchange
exchange = ccxt.binance()

def fetch_data(symbol, timeframe, limit=100):
    # Fetch OHLCV data
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    # Convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Example usage
symbol = 'BTC/USDT'
timeframe = '1m'
data = fetch_data(symbol, timeframe)
print(data)