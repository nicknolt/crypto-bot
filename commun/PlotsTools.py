import matplotlib.pyplot as plt
import numpy as np
import math
import ta
from pandas import DataFrame

class ChartPlot(object):
    def __init__(self):
        pass

    @staticmethod
    def plot_charts(data):
        figure = plt.figure(figsize=(20,10))
        ax = figure.add_subplot(1,1,1)
        ax.plot(data, color='red')
        ax.set_title("Close Charts")
        ax.set_xlabel('Dates')
        ax.set_ylabel('Values')
        plt.show()

    @staticmethod
    def plot_scatter(data: DataFrame):
        data['SMA200'] = ta.trend.sma_indicator(data['close'], 5)
        data['SMA600'] = ta.trend.sma_indicator(data['close'], 30)