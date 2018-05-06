# -*- coding: utf-8 -*-

"""
stock.py
technical test
"""

import argparse
import time
import pandas as pd

__author__     = "Giuseppe D'Onofrio"
__copyright__  = "Copyright 2018, Giuseppe D'Onofrio"
__project__    = "Super Simple Stock Market"
__credits__    = ["Giuseppe D'Onofrio"]
__version__    = "0.0.1"
__maintainer__ = "Giuseppe D'Onofrio"
__email__      = "gidonof@gmail.com"
__status__     = "Development"


class stockOpt(object):
  @classmethod
  def __init__( self, price ):
    """ constructor method """
    self.PRICE = price
    self.startTime = time.time()
    # self.PRESET=60*15
    self.PRESET = 5

  def vwsp(self, df):
    volume = df.quantity_of_shares.values
    price = df.traded_price.values
    return df.assign(vwsp=(price * volume).cumsum() / volume.cumsum())

  def calcPEratio( self, row ):
    """ method to calc Price-Earnings Ratio """
    if row['Dividend_Yield'] != 0:
      return self.PRICE / row['Dividend_Yield']
    else:
      return 0

  def geometricMean( self, prices):
    """ method to calc the Geometric mean from a list of values """
    return reduce(lambda px, py: px*py, prices)**(1.0/len(prices))

  def calcDividend( self, row):
    """ method to calc the Dividend yield """
    if row['Type'] == "Preferred":
      return (row['Fixed_Dividend']  * row['Par_Value']) / self.PRICE
    elif row['Type'] == "Common":
      return row['Last_Dividend'] / self.PRICE

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument( '-p', "--price", required=True)
  args = parser.parse_args()
  if (args.price == None and args.length == None):
    parser.print_help()

  # to expand the display of Pandas dataframes
  pd.set_option('expand_frame_repr', False)
  #
  newStock = stockOpt(int(args.price))
  #
  # first dataframe referred to : "Table1. Sample data from the Global Beverage Corporation Exchange"
  df1 = pd.DataFrame({"TEA": ["Common", 0, None, 100],
                      "POP": ["Common", 8, None, 100],
                      "ALE": ["Common", 23, None, 60],
                      "GIN": ["Preferred", 8, 0.02, 100],
                      "JOE": ["Common", 13, None, 250],
                      }, index=['Type', 'Last_Dividend', 'Fixed_Dividend', 'Par_Value'])
  df1.index.rename('Stock_Symbol', inplace=True)
  df_table1 = df1.T

  # request a.i. -> 'Given any price as input, calculate the dividend yield' - (added to dataframe 'df_table1'):
  df_table1['Dividend_Yield'] = df_table1.apply(newStock.calcDividend, axis=1)

  # request a.ii. -> 'Given any price as input, calculate the P/E Ratio' - (added to dataframe 'df_table1'):
  df_table1['P/E_Ratio'] = df_table1.apply(newStock.calcPEratio, axis=1)

  # Display the results ( last two dataframe columns ) of the first two requests (a.i., and a.ii.)
  print df_table1

  # sample dataframe filled manually by inventing numbers (just to try some methods)...
  # second dataframe referred to the request a.iii -> 'Record a trade, with timestamp, quantity of shares, buy or sell indicator and traded price":
  df2 = pd.DataFrame({"2018-05-05 09:00": ["a", 100, "B", 10.2],
                      "2018-05-05 09:01": ["b", 20, "B", 15.4],
                      "2018-05-05 09:02": ["c", 50, "B", 8.25],
                      "2018-05-05 09:03": ["d", 10, "S", 32.3],
                      "2018-05-05 09:04": ["e", 25, "S", 27.1],
                      "2018-05-05 09:05": ["f", 27, "S", 19.0],
                      "2018-05-05 09:06": ["g", 13, "B", 15.2],
                      "2018-05-05 09:07": ["h", 30, "B", 19.8],
                      "2018-05-05 09:08": ["i", 10, "S", 2.6],
                      "2018-05-05 09:09": ["j", 25, "B", 8.13],
                      "2018-05-05 09:10": ["k", 10, "S", 50.3],
                      "2018-05-05 09:11": ["l", 12, "S", 30.2],
                      "2018-05-05 09:12": ["m", 90, "S", 27.3],
                      "2018-05-05 09:13": ["n", 15, "B", 12.3],
                      "2018-05-05 09:14": ["o", 40, "B", 14.2],
                      }, index=['stock_ref', 'quantity_of_shares', 'indicator', 'traded_price'])
  print '\n'

  df2.index.rename('time', inplace=True)
  df_trade = df2.T
  # request a.iv. -> 'Calculate Volume Weighted Stock Price based on trades in past 15 minutes'
  # (last column of the returned dataframe)
  print newStock.vwsp(df_trade)
  print '\n'

  # request b. -> 'Calculate the GBCE All Share Index using the geometric mean of prices for all stocks'
  print "Geometric Mean = {}".format(newStock.geometricMean(df_trade['traded_price'].tolist()))


