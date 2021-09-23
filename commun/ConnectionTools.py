import pandas as pd
from binance.client import Client as Client_Binance
import ftx
import ta
import pandas_ta as pda
import matplotlib.pyplot as plt
import numpy as np
from math import *
from termcolor import colored
from typing import List


class Connection(object):
    def __init__(self, crypto: str = "BTCUSDT", start_date: str = "10 september 2021"):
        self.crypto: str = crypto
        self.start_date: str = start_date

    def init_connection_binance(self):
        self.client_B = Client_Binance()

    def init_connection_ftx(self):
        pass

    def acq_data(self) -> List[List[str]]:
        klinesT: List[List[str]] = self.client_B.get_historical_klines(self.crypto, Client_Binance.KLINE_INTERVAL_15MINUTE, self.start_date)
        return klinesT

class ConnectionFTX(object):
    def truncate(n, decimals=0):
        r = floor(float(n) * 10 ** decimals) / 10 ** decimals
        return str(r)

    def getBalance(myclient, coin):
        jsonBalance = myclient.get_balances()
        if jsonBalance == []:
            return 0
        pandaBalance = pd.DataFrame(jsonBalance)
        if pandaBalance.loc[pandaBalance['coin'] == coin].empty:
            return 0
        else:
            return float(pandaBalance.loc[pandaBalance['coin'] == coin]['free'])

    pairSymbol = 'ETH/USD'
    fiatSymbol = 'USD'
    cryptoSymbol = 'ETH'
    myTruncate = 3
    i = 9
    j = 21
    accountName = ''
    goOn = True

    client = ftx.FtxClient(
        api_key='',
        api_secret='',
        subaccount_name=accountName
    )
    result = client.get_balances()

    data = client.get_historical_data(
        market_name=pairSymbol,
        resolution=3600,
        limit=1000,
        start_time=float(round(time.time())) - 150 * 3600,
        end_time=float(round(time.time())))
    df = pd.DataFrame(data)


if __name__ == '__main__':
    pass