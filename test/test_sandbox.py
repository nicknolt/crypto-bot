import unittest
from typing import List

import numpy as np
import pandas as pd
import ta
from binance import Client

def convert(klines: List) -> pd.DataFrame:

    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                        'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
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

    return df

class HistoricalKLines:

    def __init__(self, dataframe: pd.DataFrame):
        self._data = dataframe

    def sma(self, windows_size: int) -> float:
        sma = ta.trend.sma_indicator(self._data['close'], windows_size)
        lastIndex = sma.first_valid_index()

        return sma[lastIndex]


class Rule:

    def __init__(self):
        self._data: HistoricalKLines = None

        self._sma200 = None
        self._sma600 = None
        self._usdt = 10
        self._btc = 0

    @property
    def sma200(self) -> float:
        if not self._sma200:
            self._sma200 = self._data.sma(windows_size=200)

        return self._sma200

    @property
    def sma600(self) -> float:
        if not self._sma600:
            self._sma600 = self._data.sma(windows_size=600)

        return self._sma600

    def apply(self, data: HistoricalKLines):
        self._data = data

        for index, row in data._data.iterrows():

            print("KIKOO")

            if self.sma200 > self.sma600 and self._usdt > 10:
                # btc = usdt / df['close'][index]
                self._btc = self._usdt / row['close']
                self._btc = self._btc - 0.007 * self._btc
                self._usdt = 0
                print("Buy BTC at", row['close'], '$ the', index)

            if self.sma200 < self.sma600 and self._btc > 0.0001:
                # usdt = btc * df['close'][index]
                self._usdt = self._btc * row['close']
                self._usdt = self._usdt - 0.007 * self._usdt
                self._btc = 0
                print("Sell BTC at", row['close'], '$ the', index)

    # def condition(self) -> bool:
    #     pass
    #
    # def when_true(self):
    #     pass


            

class TestSandbox(unittest.TestCase):

    def test_binance(self):
        client = Client()
        klinesT = client.get_historical_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, start_str="01 may 2021")
        print("OK")

    def test_convert(self):
        client = Client()
        klinesT = client.get_historical_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, start_str="01 may 2021")
        df = convert(klinesT)
        histo = HistoricalKLines(dataframe=df)

        rule = Rule()
        rule.apply(histo)
