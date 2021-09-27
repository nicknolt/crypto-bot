from datetime import datetime
from typing import List

from binance import Client
from pandas import DataFrame


class DataSource:

    def get_historic(self, date_from: datetime, date_to: datetime) -> List:

        client = Client()

        date_from_ts = int(date_from.timestamp()*1000)
        date_to_ts = int(date_to.timestamp()*1000)

        klinesT = client.get_historical_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, start_str=date_from_ts, end_str=date_to_ts)

        return klinesT