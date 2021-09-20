import ftx
import pandas as pd
import ta
import time
import json
from math import *
# IvlY5AD96BIHCOBNzcGtP3ggGo00bl6B8XHk6pkK ,,,, twx_JCgvkzChw7bfIUjTaX5Fq3-NahF6TlOI7SQ_
# si probleme install ftx : https://anaconda.org/conda-forge/ciso8601
accountName = 'steve.didienne@protonmail.com'
pairSymbol = 'BTC/USD'
fiatSymbol = 'USD'
cryptoSymbol = 'BTC'
myTruncate = 4

client = ftx.FtxClient(api_key='IvlY5AD96BIHCOBNzcGtP3ggGo00bl6B8XHk6pkK',
                       api_secret='twx_JCgvkzChw7bfIUjTaX5Fq3-NahF6TlOI7SQ_', subaccount_name=accountName)

data = client.get_historical_data(
    market_name=pairSymbol,
    resolution=900,
    limit=650,
    start_time=float(
        round(time.time())) - 650 * 900,
    end_time=float(round(time.time())))
df = pd.DataFrame(data)

df['SMA200'] = ta.trend.sma_indicator(df['close'], 200)
df['SMA600'] = ta.trend.sma_indicator(df['close'], 600)
print(df)


def getBalance(myclient, coin):
    """
    Récuperation des montants dispo sur ftx
    :param myclient:
    :param coin:
    :return:
    """
    jsonBalance = myclient.get_balances()
    pandaBalance = pd.DataFrame(jsonBalance)
    if pandaBalance.loc[pandaBalance['coin'] == coin].empty:
        return 0
    else:
        return float(pandaBalance.loc[pandaBalance['coin'] == coin]['free'])


def truncate(n, decimals=0):
    r = floor(float(n) * 10 ** decimals) / 10 ** decimals
    return str(r)


actualPrice = df['close'].iloc[-1]
fiatAmount = getBalance(client, fiatSymbol)
cryptoAmount = getBalance(client, cryptoSymbol)
print(actualPrice, fiatAmount, cryptoAmount)

if float(fiatAmount) > 5 and df['SMA200'].iloc[-2] > df['SMA600'].iloc[-2]:
    quantityBuy = truncate(float(fiatAmount) / actualPrice, myTruncate)
    buyOrder = client.place_order(
        market=pairSymbol,
        side="buy",
        price=None,
        size=quantityBuy,
        type='market')
    print(buyOrder)

elif float(cryptoAmount) > 0.0001 and df['SMA200'].iloc[-2] < df['SMA600'].iloc[-2]:
    buyOrder = client.place_order(
        market=pairSymbol,
        side="sell",
        price=None,
        size=truncate(cryptoAmount, myTruncate),
        type='market')
    print(buyOrder)
else:
    print("No opportunity")
