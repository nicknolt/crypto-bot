import pandas as pd
from binance.client import Client as Client_Binance
import ta
import pandas_ta as pda
import matplotlib.pyplot as plt
import numpy as np
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


if __name__ == '__main__':
    pass