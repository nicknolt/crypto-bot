import unittest
from commun.ConnectionTools import Connection
from commun.DAO import TraitmentData
from commun.PlotsTools import ChartPlot as CT


class TestConnectionTools(unittest.TestCase):
    def setUp(self) -> None:
        self.connect = Connection(crypto="BTCUSDT", start_date="10 september 2021")
        self.connect.init_connection_binance()
        self.data_select = TraitmentData()

    def test_acq_data(self):
        data = self.connect.acq_data()
        # print(data)

    def test_select_data(self):
        data = self.connect.acq_data()
        self.data_select.select_data(data)


class MyTestPlot(unittest.TestCase):
    def setUp(self) -> None:
        self.connect = Connection()
        self.connect.init_connection_binance()
        self.data_select = TraitmentData()


    def test_plot_charts(self):
        data = self.connect.acq_data()
        self.data_select.select_data(data)
        CT.plot_charts(data=self.data_select.data['close'])

if __name__ == '__main__':
    unittest.main()
