#!/usr/bin/env python
#	Tags: phoenix-port, py3-port

import wx
import pandas as pd
import DataFrameViewCtrl
import Config
import morningstar

#---------------------------------------------------------------------------

#----------------------------------------------------------------------

def GetWindow(frame, nb, log):
    
    # Create the dataframe. First get the tickers.
    if Config.holdingsDf is None:
        Config.GetHoldings()

    # Get the SPY performance history
    pfh1 = morningstar.trailing_total_returns("SPY")

    # Remove last row
    pfh = pfh1.drop(pfh1.index[[0]])

    tickerList = list()

    # For each ticker in the config...
    for i in range(Config.holdingsDf.shape[0]):
        ticker = Config.holdingsDf.ix[i, "Ticker"]
        
        if ticker in tickerList:
            continue

        tickerList.append(ticker)

        df = morningstar.trailing_total_returns(ticker)
        if df is not None:
            pfh = pfh.append(df)
            
    win = DataFrameViewCtrl.Panel(nb, pfh, log)
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

