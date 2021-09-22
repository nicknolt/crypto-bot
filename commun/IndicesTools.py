import ta
from pandas import Series


class ConditionsTrades(object):

    def __init__(self):
        pass


class IndicatorsTrades(object):

    def __init__(self):
        self.indicators: dict = {}

    def SMA(self, values: Series, nb_points: int):
        self.indicators[f'SMA{nb_points}'] = ta.trend.sma_indicator(values, nb_points)