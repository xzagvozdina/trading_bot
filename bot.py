import numpy as np
import pandas as pd
from binance.client import Client
from sklearn.decomposition import PCA
from constants import BINANCE_API_KEY, BINANCE_API_SECRET

# Параметры подключения к Binance API
api_key = BINANCE_API_KEY
api_secret = BINANCE_API_SECRET
client = Client(api_key, api_secret)

# Фьючерс ETHUSDT
symbol = 'ETHUSDT'

# Функция для получения последних n свечей фьючерса symbol
def get_klines(symbol, interval, n):
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=n)
    df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                       'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                       'Taker buy quote asset volume', 'Ignore'])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    df = df.set_index('Close time')
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df = df.astype('float')
    return df

# Последние 120 свечей фьючерса ETHUSDT с интервалом 1 минута
data = get_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, 120)
print(data)