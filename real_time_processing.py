import numpy as np

def process_real_time(symbol, timeframe):
    while True:
        # Fetch latest data
        df = fetch_data(symbol, timeframe)
        df = compute_indicators(df)
        # Prepare data for prediction
        inputs = df[['close', 'RSI', 'SMA']].values[-100:]  # Last 100 time steps
        inputs = np.reshape(inputs, (1, inputs.shape[0], inputs.shape[1]))
        # Predict signal
        signal = model.predict(inputs)
        print(f"Predicted signal: {signal}")
        # Sleep for the timeframe duration
        time.sleep(exchange.parse_timeframe(timeframe))

# Example usage
process_real_time(symbol, timeframe)