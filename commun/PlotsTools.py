import matplotlib.pyplot as plt
import numpy as np
import math

class ChartPlot(object):
    def __init__(self):
        self.show = plt.show()

    def plot_charts(self):
        figure = plt.figure(figsize=(15,4))
        x = np.arange(0, math.pi * 2, 0.05)
        y = np.sin(x)
        ax = figure.add_subplot()
        ax.plot(x, y)
        ax.set_title("sine wave")
        ax.set_xlabel('angle')
        ax.set_ylabel('sine')
        plt.show()