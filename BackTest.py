import pandas as pd
from binance.client import Client
import ta
import pandas_ta as pda
import matplotlib.pyplot as plt
import numpy as np
from termcolor import colored

client = Client()

klinesT = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "10 september 2021")

# COUCOU

df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
del df['ignore']
del df['close_time']
del df['quote_av']
del df['trades']
del df['tb_base_av']
del df['tb_quote_av']

df['close'] = pd.to_numeric(df['close'])
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])
df['open'] = pd.to_numeric(df['open'])
print(df)

df = df.set_index(df['timestamp'])
df.index = pd.to_datetime(df.index, unit='ms')
del df['timestamp']
print(df)
# plt.plot(df['close'], label='Close')
# plt.plot(df['high'])
# plt.plot(df['low'])
# plt.plot(df['open'])
# plt.legend()
# plt.show()

df['SMA200'] = ta.trend.sma_indicator(df['close'], 5)
df['SMA600'] = ta.trend.sma_indicator(df['close'], 30)
print(df)
# plt.plot(df['SMA200'], label='SMA 200')
plt.scatter(df['SMA200'].index, df['SMA200'].values, color='y', label='SMA200')
# plt.scatter(df['SMA600'].index, df['SMA600'].values, color='b', label='SMA600')

plt.plot(df['SMA600'], label='SMA 600')
plt.plot(df['close'], label='close')

# plt.legend()
# plt.show()

usdt = 1000
btc = 0
lastIndex = df.first_valid_index()
df_buy = pd.Series([])
df_sell = pd.Series([])

for index, row in df.iterrows():
  if df['SMA200'][lastIndex] < df['SMA600'][lastIndex] and usdt > 10:
    btc = usdt / df['close'][index]
    btc = btc - 0.007 * btc
    usdt = 0
    print("Buy BTC at",df['close'][index],'$ the', index)
    df_buy.loc[index] = df['close'][index]


  if df['SMA200'][lastIndex] > df['SMA600'][lastIndex] and df['SMA200'][lastIndex] > df['close'][lastIndex] and btc > 0.0001:
    usdt = btc * df['close'][index]
    usdt = usdt - 0.007 * usdt
    btc = 0
    print("Sell BTC at",df['close'][index],'$ the', index)
    df_sell.loc[index] = df['close'][index]

  lastIndex = index

plt.scatter(df_buy.index, df_buy.values, color='red', label='buy')
plt.scatter(df_sell.index, df_sell.values, color='green', label='sell')

plt.legend()
plt.show()


finalResult = usdt + btc * df['close'].iloc[-1]
print("Final result",finalResult,'USDT')

print("Buy and hold result", (1000 / df['close'].iloc[0]) * df['close'].iloc[-1],'USDT')

# ----- Functions Definition -------
def get_chop(high, low, close, window):
    tr1 = pd.DataFrame(high - low).rename(columns = {0:'tr1'})
    tr2 = pd.DataFrame(abs(high - close.shift(1))).rename(columns = {0:'tr2'})
    tr3 = pd.DataFrame(abs(low - close.shift(1))).rename(columns = {0:'tr3'})
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').dropna().max(axis = 1)
    atr = tr.rolling(1).mean()
    highh = high.rolling(window).max()
    lowl = low.rolling(window).min()
    ci = 100 * np.log10((atr.rolling(window).sum()) / (highh - lowl)) / np.log10(window)
    return ci


# -----------------------------------------------------------------

#df.drop(df.columns.difference(['open','high','low','close','volume']), 1, inplace=True)

#Simple Moving Average
# df['SMA']=ta.trend.sma_indicator(df['close'], window=12)

#Exponential Moving Average
#df['EMA1']=ta.trend.ema_indicator(close=df['close'], window=13)
#df['EMA2']=ta.trend.ema_indicator(close=df['close'], window=38)

# #Relative Strength Index (RSI)
# df['RSI'] =ta.momentum.rsi(close=df['close'], window=14)

# #MACD
# MACD = ta.trend.MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
# df['MACD'] = MACD.macd()
# df['MACD_SIGNAL'] = MACD.macd_signal()
# df['MACD_DIFF'] = MACD.macd_diff() #Histogramme MACD

# #Stochastic RSI
# df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=14, smooth1=3, smooth2=3) #Non moyenn??
# df['STOCH_RSI_D'] = ta.momentum.stochrsi_d(close=df['close'], window=14, smooth1=3, smooth2=3) #Orange sur TradingView
# df['STOCH_RSI_K'] =ta.momentum.stochrsi_k(close=df['close'], window=14, smooth1=3, smooth2=3) #Bleu sur TradingView

# #Ichimoku
# df['KIJUN'] = ta.trend.ichimoku_base_line(high=df['high'], low=df['low'], window1=9, window2=26)
# df['TENKAN'] = ta.trend.ichimoku_conversion_line(high=df['high'], low=df['low'], window1=9, window2=26)
# df['SSA'] = ta.trend.ichimoku_a(high=df['high'], low=df['low'], window1=9, window2=26)
# df['SSB'] = ta.trend.ichimoku_b(high=df['high'], low=df['low'], window2=26, window3=52)

# #Bollinger Bands
# BOL_BAND = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
# df['BOL_H_BAND'] = BOL_BAND.bollinger_hband() #Bande Sup??rieur
# df['BOL_L_BAND'] = BOL_BAND.bollinger_lband() #Bande inf??rieur
# df['BOL_MAVG_BAND'] = BOL_BAND.bollinger_mavg() #Bande moyenne

# #Average True Range (ATR)
# df['ATR'] = ta.volatility.average_true_range(high=df['high'], low=df['low'], close=df['close'], window=14)

# #Super Trend
# ST_length = 10
# ST_multiplier = 3.0
# superTrend = pda.supertrend(high=df['high'], low=df['low'], close=df['close'], length=ST_length, multiplier=ST_multiplier)
# df['SUPER_TREND'] = superTrend['SUPERT_'+str(ST_length)+"_"+str(ST_multiplier)] #Valeur de la super trend
# df['SUPER_TREND_DIRECTION'] = superTrend['SUPERTd_'+str(ST_length)+"_"+str(ST_multiplier)] #Retourne 1 si vert et -1 si rouge

# #Awesome Oscillator
# df['AWESOME_OSCILLATOR'] = ta.momentum.awesome_oscillator(high=df['high'], low=df['low'], window1=5, window2=34)

# # Kaufman???s Adaptive Moving Average (KAMA)
# df['KAMA'] = ta.momentum.kama(close=df['close'], window=10, pow1=2, pow2=30)

# #Choppiness index
# df['CHOP'] = get_chop(high=df['high'], low=df['low'], close=df['close'], window=14)

df
