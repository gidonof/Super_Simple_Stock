# -*- coding: utf-8 -*-

import time
import datetime
import pandas as pd
from mylogging import Logger
import numpy as np
import collections

__author__  = "gidonof"
__project__ = "Super Simple Stock Market"
__repo__    = "https://github.com/gidonof/Super_Simple_Stock_Market"

class stockOpt(object):
  @classmethod
  def __init__( self ):
    """ constructor method """
    self.PRICE = 10
    self.startTime = time.time()
    # self.PRESET=60*15
    self.PRESET = 5
    self.stockDict = collections.OrderedDict()
    self.logger = Logger(self.__class__.__name__).get()

  def timeStamp( self ):
    """ method to obtain a preset timestamp """
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')

  def priceAndVolume(self, price, volume):
    return price*volume

  def vwsp( self, price, quantity):
    return (price * quantity).cumsum() / quantity.cumsum()

  def vwsp(self, df):
    volume = df.volume.values
    price = df.price.values
    return df.assign(vwsp=(price * volume).cumsum() / volume.cumsum())


  def calcPEratio( self, Price, dividend ):
    """ method to calc Price-Earnings Ratio """
    if dividend != 0:
      return Price / dividend
    else:
      return 0

  def calcDividend( self, stock, Price ):
    """ method to calc the Dividend yield """
    if stock.Type == "Preferred":
      return (stock.Fixed_Dividend * stock.Par_Value) / Price
    elif stock.Type == "Common":
      return stock.Last_Dividend / Price

  def getRandNum( self, max, size ):
    return np.random.randint(max, size=size)[0]

  def rootOf( self, num, root ):
    if root > 0: return num ** (1 / float(root))

  def fillDataFrame( self ):
    """ method to fill randomly a dataframe """
    df = pd.DataFrame({"TEA": ["Common", self.getRandNum(50, 1), None, self.getRandNum(500, 1)],
                       "POP": ["Common", self.getRandNum(50, 1), None, self.getRandNum(500, 1)],
                       "ALE": ["Common", self.getRandNum(50, 1), None, self.getRandNum(500, 1)],
                       "GIN": ["Preferred", self.getRandNum(50, 1), self.getRandNum(1, 1),
                               self.getRandNum(500, 1)],
                       "JOE": ["Common", self.getRandNum(500, 1), None, self.getRandNum(500, 1)],
                       }, index=['Type', 'Last_Dividend', 'Fixed_Dividend', 'Par_Value'])
    df.index.rename('Stock_Symbol', inplace=True)
    return df.T

  def geometricMean(self, prices):
    """ method to calc the Geometric mean from a list of values """
    return reduce(lambda px, py: px*py, prices)**(1.0/len(prices))


if __name__ == '__main__':
  newStock = stockOpt()
  while True:
    df2 = newStock.fillDataFrame()
    for stock in df2.index.values:
      print "{} - {}: Dividend Yield = {} pennies, P/E Ratio = {}".format(newStock.timeStamp(), stock,
                                                                          newStock.calcDividend(df2.loc[stock],
                                                                                                newStock.PRICE),
                                                                          newStock.calcPEratio(newStock.PRICE,
                                                                                               newStock.calcDividend(
                                                                                                 df2.loc[stock],
                                                                                                 newStock.PRICE)))
      dividend = newStock.calcDividend(df2.loc[stock], newStock.PRICE)
      price_earnings = newStock.calcPEratio(newStock.PRICE, newStock.calcDividend(df2.loc[stock], newStock.PRICE))
      # newStock.logger.info("{} - {}: Dividend Yield = {} pennies, P/E Ratio = {}".format(newStock.timeStamp(), stock, newStock.calcDividend(df2.loc[stock], newStock.PRICE) , newStock.calcPEratio(newStock.PRICE, newStock.calcDividend(df2.loc[stock], newStock.PRICE))))
    time.sleep(1)
    print("\n")
    timing = newStock.timeStamp()


    df_trade = pd.DataFrame({newStock.timeStamp(): [newStock.getRandNum(15.0, 5), newStock.getRandNum(100, 5), "b"]

                            }, index=['price', 'volume', 'buy/sell indicator'] )


    df_trade.index.rename('date', inplace=True)

    print 'Trade recorded:\n{}\n'.format(newStock.vwsp(df_trade.T))

    prices = [2, 5, 12]
    print 'Geometric Mean = {}'.format(newStock.geometricMean(prices))

    #raw_input()


  #time.sleep(newStock.PRESET - ((time.time() - newStock.startTime) % newStock.PRESET))
  # newStock.logger.info("{} - {}: Dividend Yield = {} pennies, P/E Ratio = {}".format(newStock....)
