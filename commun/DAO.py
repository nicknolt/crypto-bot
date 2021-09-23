import json
from typing import List
import pandas as pd
from abc import ABC, abstractmethod



class DaoFiles(object):
    pass

    def creat_files(self):
        pass

class TraitmentData(object):
    def __init__(self):
        self.data = None

    def select_data(self, data_brut: List[List[str]]):
        df = pd.DataFrame(data_brut,
                          columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
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

        # df = df.set_index(df['timestamp'])
        # df.index = pd.to_datetime(df.index, unit='ms')
        # del df['timestamp']
        self.data = df
        # print(df)
