import unittest
from commun.ConnectionTools import Connection


class MyTestCase(unittest.TestCase):
    def test_plot_charts(self):

        self.assertEqual(True, False)

    def test_acqdata(self):
        connect = Connection()
        connect.init_connection_binance()
        connect.acq_data()

if __name__ == '__main__':
    unittest.main()
