
import pandas as pd
import numpy as np
import ta

# =========================
# SIMPLE TRADING BOT (ALL-IN-ONE)
# =========================

def add_indicators(df):
    # EMA
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=9)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=21)

    # RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)

    # MACD
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    # Volume average
    if 'volume' in df.columns:
        df['vol_avg'] = df['volume'].rolling(20).mean()
    else:
        df['volume'] = 1
        df['vol_avg'] = 1

    return df


def candle_patterns(df):
    df['bullish_engulfing'] = False
    df['bearish_engulfing'] = False

    for i in range(1, len(df)):
        prev = df.iloc[i-1]
        curr = df.iloc[i]

        # Bullish Engulfing
        if curr['close'] > curr['open'] and prev['close'] < prev['open']:
            df.at[df.index[i], 'bullish_engulfing'] = True

        # Bearish Engulfing
        if curr['close'] < curr['open'] and prev['close'] > prev['open']:
            df.at[df.index[i], 'bearish_engulfing'] = True

    return df


def generate_signal(df):
    last = df.iloc[-1]

    buy = (
        last['ema_fast'] > last['ema_slow'] and
        last['rsi'] < 70 and
        last['macd'] > last['macd_signal'] and
        last['volume'] >= last['vol_avg'] and
        last.get('bullish_engulfing', False)
    )

    sell = (
        last['ema_fast'] < last['ema_slow'] and
        last['rsi'] > 30 and
        last['macd'] < last['macd_signal'] and
        last.get('bearish_engulfing', False)
    )

    if buy:
        return "BUY 📈"
    elif sell:
        return "SELL 📉"
    else:
        return "NO TRADE ⛔"


def get_dummy_data():
    data = {
        "open":  [100,101,102,101,103,104,105,106,107,108],
        "close": [101,102,101,103,104,105,106,107,108,109],
        "volume":[10,12,11,13,15,14,16,18,17,20]
    }
    return pd.DataFrame(data)


def run():
    df = get_dummy_data()
    df = add_indicators(df)
    df = candle_patterns(df)

    signal = generate_signal(df)
    print("LATEST SIGNAL:", signal)


if __name__ == "__main__":
    run()
