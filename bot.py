import numpy as np
import pandas as pd
from binance.client import Client
import statsmodels.api as sm
from constants import BINANCE_API_KEY, BINANCE_API_SECRET
import time

# Параметры подключения к Binance API
api_key = BINANCE_API_KEY
api_secret = BINANCE_API_SECRET
client = Client(api_key, api_secret)

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

# Последние 120 свечей фьючерса ETHUSDT и BTCUSDT с интервалом 1 минута
data_ETHUSDT = get_klines('ETHUSDT', Client.KLINE_INTERVAL_1MINUTE, 120)
data_BTCUSDT = get_klines('BTCUSDT', Client.KLINE_INTERVAL_1MINUTE, 120)

# Только Close price
y = data_ETHUSDT['Close'].values
x = data_BTCUSDT['Close'].values

# Тест на коинтеграцию, уровень значимости 0.05
coint = sm.tsa.stattools.coint(y, x)
if coint[1] < 0.05:
    print("Переменные коинтегрированы.")
else:
    print("Переменные не коинтегрированы.")

# Новые параметры
x = np.hstack([x.reshape(-1, 1), data_ETHUSDT[['Open', 'High', 'Low', 'Volume']].to_numpy()])

# Регрессия
model = sm.OLS(y, sm.add_constant(x))
results = model.fit()
# print(results.summary())

# Коэффициенты
# print("Коэффициент линейной зависимости от BTCUSDT:", results.params[1])
# print("Константа:", results.params[0])

# Функция для выявления процента изменения
def has_1pct_change(time_series):
    min_val = time_series[0]
    max_val = time_series[0]


    for val in time_series:
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val

    pct_change = abs(max_val - min_val) / min_val * 100

    if pct_change >= 1.:
        return pct_change

    return False

# Вечный цикл оповещений
while True:
    latest_data_eth = get_klines('ETHUSDT', Client.KLINE_INTERVAL_1MINUTE, 60)
    latest_data_btc = get_klines('BTCUSDT', Client.KLINE_INTERVAL_1MINUTE, 60)

    # Собственные колебания ETHUSDT
    eth_without_btc = latest_data_eth['Close'].values - results.params[1] * latest_data_btc['Close'].values
    
    change = has_1pct_change(eth_without_btc)
    if change:
        print(f'В течении последнего часа произошло изменение на {change:.2f}%')

    time.sleep(60 * 60)