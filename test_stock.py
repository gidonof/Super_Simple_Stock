# -*- coding: utf-8 -*-

"""
test_stock.py
test of 'stock.py'
"""

__author__     = "Giuseppe D'Onofrio"
__copyright__  = "Copyright 2018, Giuseppe D'Onofrio"
__project__    = "Super Simple Stock Market"
__credits__    = ["Giuseppe D'Onofrio"]
__version__    = "0.0.1"
__maintainer__ = "Giuseppe D'Onofrio"
__email__      = "gidonof@gmail.com"
__status__     = "Development"

import unittest
import stock
import pandas as pd


class testStock(unittest.TestCase):
  """ unittest Class

      This Class contains 4 test methods:
      - test_calcDividend
      - test_calcPEratio
      - test_vwsp
      - test_geometricMean

  """

  @classmethod
  def setUp(self):
    self.newStock = stock.stockOpt(10)
    self.df = pd.DataFrame({"GIN": ["Preferred", 8, 0.02, 100, 0.2]},
                           index=['Type', 'Last_Dividend', 'Fixed_Dividend', 'Par_Value', 'Dividend_Yield'])
    self.df.index.rename('Stock_Symbol', inplace=True)
    self.df_table1 = self.df.T

    self.df2 = pd.DataFrame({"2018-05-05 09:00": [100, "B", 10.2]},
                            index=['quantity_of_shares', 'indicator', 'traded_price'])
    self.df_trade = self.df2.T

  def test_calcPEratio(self):
    """ to test 'calcPEratio' method """
    result = self.newStock.calcPEratio(self.df_table1.iloc[0])
    self.assertEqual(result, 50.0)

  def test_calcDividend(self):
    """ to test 'calcDividend' method with a part of dataframe """

    result = self.newStock.calcDividend(self.df_table1.iloc[0])
    self.assertEqual(result, .2)

  def test_vwsp(self):
    """ to test vwsp method """
    result = self.newStock.vwsp(self.df_trade)
    self.assertEqual(result['vwsp'].iloc[0], 10.2)

  def test_geometricMean(self):
    """ to test geometricMean method """
    result = self.newStock.geometricMean([2, 5, 12])
    self.assertEqual(result, 4.93242414866094)


if __name__ == '__main__':
  unittest.main()
