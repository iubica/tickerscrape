#!/usr/bin/env python
#	Tags: phoenix-port, py3-port

import wx
import numpy as np
import pandas as pd
import DataFrameViewCtrl
import Config
import Format
import tickerscrape.morningstar

#---------------------------------------------------------------------------

#----------------------------------------------------------------------

def GetWindow(frame, nb, log):
    
    # Create the dataframe. First get the tickers.
    if Config.holdingsDf is None:
        Config.GetHoldings()

    # Make list of per-account tickers
    tickerList = list()

    # For each ticker in the config...
    for i in range(Config.holdingsDf.shape[0]):
        ticker = Config.holdingsDf.ix[i, "Ticker"]
        account = Config.holdingsDf.ix[i, "Account"]
        
        if (ticker, account) in tickerList:
            continue

        tickerList.append((ticker, account))

    # Create a performance dataframe
    pf = pd.DataFrame(index = np.arange(0, len(tickerList)),
                      columns = ['Ticker', 'Name', 'Account', 'Shares', 'Value'])

    row = 0
    for (ticker, account) in tickerList:
        pf.ix[row, "Ticker"] = ticker
        pf.ix[row, "Name"] = tickerscrape.morningstar.ticker_name(ticker.upper())
        pf.ix[row, "Account"] = account

        # Compute the shares
        shares = 0
        sharesSet = True
        costBasis = 0
        costBasisSet = True
        for i in range(Config.holdingsDf.shape[0]):
            ticker1 = Config.holdingsDf.ix[i, "Ticker"]
            account1 = Config.holdingsDf.ix[i, "Account"]
            shares1 = Config.holdingsDf.ix[i, "Shares"]
            costBasis1 = Config.holdingsDf.ix[i, "Cost Basis"]
            if ticker == ticker1 and account == account1:
                if shares1:                    
                    shares = shares + Format.StringToFloat(shares1)
                else:
                    sharesSet = False
                if costBasis1:
                    costBasis = costBasis + Format.StringToFloat(costBasis1)
                else:
                    costBasisSet = False

        if sharesSet:
            pf.ix[row, "Shares"] = Format.FloatToString(shares, 3)
        else:
            pf.ix[row, "Shares"] = ""
            
        if costBasisSet:
            pf.ix[row, "Cost Basis"] = "$" + Format.FloatToString(costBasis, 2)
        else:
            pf.ix[row, "Cost Basis"] = ""
            
        row = row+1
    
    # Promote 1st column as new index
    pf2 = pf.set_index("Ticker")
    pf = pf2

    pf.index.name = "Ticker"
        
        
        
    win = DataFrameViewCtrl.Panel(nb, pf, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>DataViewCtrl with DataViewIndexListModel</center></h2>

This sample shows how to derive a class from PyDataViewIndexListModel and use
it to interface with a list of data items. (This model does not have any
hierarchical relationships in the data.)

<p> See the comments in the source for lots of details.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run

    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
