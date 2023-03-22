import numpy as np
import pandas as pd
from binance.client import Client
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from constants import BINANCE_API_KEY, BINANCE_API_SECRET

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
# print(data_ETHUSDT)
# print(data_BTCUSDT)

# Только Close price
eth_prices = data_ETHUSDT['Close'].values
btc_prices = data_BTCUSDT['Close'].values
prices = np.column_stack((eth_prices, btc_prices))

# Стандартизация данных
prices_std = (prices - prices.mean(axis=0)) / prices.std(axis=0)

# Метод главных компонент
pca = PCA(n_components=2)
principal_components = pca.fit_transform(prices_std)

# Исключение движений, связанных с BTCUSDT
eth_prices_excl_btc = principal_components[:, 0]

# print(eth_prices_excl_btc[:10])


while True:
    latest_data = get_klines('ETHUSDT', Client.KLINE_INTERVAL_1MINUTE, 1)


# In this code, we first load the data from a CSV file (ETHUSDT_futures.csv) using pandas. We then separate the data into two sets, one for ETHUSDT and one for BTCUSDT.
# Next, we standardize the data using z-scores, which will help ensure that both sets of data are on the same scale.
# We then perform PCA on the BTCUSDT data, using n_components=1 to extract a single component that explains the most variance in the data. We then use the transform method to project the BTCUSDT data onto this component.
# Finally, we subtract the BTCUSDT component from the ETHUSDT data using the dot function, which effectively removes the movements in ETHUSDT that are caused by movements in BTCUSDT.

# To define ETHUSDT futures price movements excluding BTCUSDT price movements, we can use a statistical method called linear regression analysis. This technique allows us to isolate the effect of BTCUSDT price movements on ETHUSDT futures and identify the unique price movements of ETHUSDT futures.
# To do this, we would first need to collect historical price data for both ETHUSDT futures and BTCUSDT. We would then use linear regression to model the relationship between the two prices, using BTCUSDT as the independent variable and ETHUSDT as the dependent variable. The resulting equation would allow us to predict the expected value of ETHUSDT futures given the value of BTCUSDT, and the difference between the predicted value and the actual value would represent the unique price movements of ETHUSDT futures.
# The parameters chosen for the linear regression analysis would depend on the specific dataset being analyzed, including the time period, frequency of data collection, and the number of data points. It is important to choose a large enough dataset to ensure statistical significance, while also balancing this with the need for timely analysis.
# Once the unique price movements of ETHUSDT futures have been identified, we can monitor the price in real-time and trigger an alert when the price changes by 1% in the last 60 minutes. This can be achieved using a Python program that continuously reads the current price and calculates the percentage change over the past 60 minutes. If the percentage change exceeds 1%, the program can display a message to the console.
# Overall, the combination of linear regression analysis and real-time monitoring can provide valuable insights into the unique price movements of ETHUSDT futures and help identify potential trading opportunities.