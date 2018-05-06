import unittest
import stock
import pandas as pd

__author__  = "gidonof"
__project__ = "Super Simple Stock Market"
__repo__    = "https://github.com/gidonof/Super_Simple_Stock_Market"

class testStock(unittest.TestCase):
  """ Generic unittest

      This Class contains 5 test methods
      running this unit test we should obtain an output like:

      .
      ----------------------------------------------------------------------
      Ran 5 tests in 0.004s

      OK

      """

  @classmethod
  def setUp(self):
    self.newStock = stock.stockOpt()

  def test_calcPEratio(self):
    """ to test 'calcPEratio' method """
    result = self.newStock.calcPEratio(10, 2)
    self.assertEqual(result, 5)

  def test_calcDividend(self):
    """ to test 'calcDividend' method with a part of dataframe """
    df = pd.DataFrame({"GIN": ["Preferred", 8, 0.02, 100]}, index=['Type', 'Last_Dividend', 'Fixed_Dividend', 'Par_Value'])
    df.index.rename('Stock_Symbol', inplace=True)
    df2 = df.T
    result= self.newStock.calcDividend(df2.loc["GIN"], 10)
    self.assertEqual(result, .2)

  def test_rootOf(self):
    """ to test 'rootOf' method """
    result = self.newStock.rootOf( 4, 2)
    self.assertEqual(result, 2.0)

  def test_priceAndVolume( self ):
    """ to test price&Volume method """
    result = self.newStock.priceAndVolume(10.15, 20)
    self.assertEqual(result, 203)

  def test_geometricMean( self ):
    """ to test geometricMean method """
    result = self.newStock.geometricMean([2, 5, 12])
    self.assertEqual(result, 4.93242414866094)

if __name__ == '__main__':
    unittest.main()

