#!/usr/bin/env python
#	Tags: phoenix-port, py3-port

import wx
import numpy as np
import pandas as pd
import DataFrameViewCtrl
import Config
import Format
import morningstar

#---------------------------------------------------------------------------

#----------------------------------------------------------------------

def GetWindow(frame, nb, log):
    
    # Create the dataframe. First get the tickers.
    if Config.holdingsDf is None:
        Config.GetHoldings()

    # Make an account list
    accountList = list()

    for i in range(Config.accountsDf.shape[0]):
        account = Config.accountsDf.ix[i, "Account Name"]
        
        if account in accountList:
            continue

        accountList.append(account)

    # Make list of per-account tickers
    tickerList = list()

    # For each ticker in the config...
    for i in range(Config.holdingsDf.shape[0]):
        ticker = Config.holdingsDf.ix[i, "Ticker"]

        if ticker in tickerList:
            continue

        tickerList.append(ticker)

    # Create a performance dataframe
    pf = pd.DataFrame(index = np.arange(0, len(accountList) + len(tickerList)),
                      columns = ["Ticker", "Last Price", "Units", "Current Value", "Cost Basis"])

    row = 0
    for account in accountList:
        pf.ix[row, "Ticker"] = account
        pf.ix[row, "Last Price"] = ""
        pf.ix[row, "Units"] = ""
        pf.ix[row, "Current Value"] = ""
        pf.ix[row, "Cost Basis"] = ""
        row = row+1
        for i in range(Config.holdingsDf.shape[0]):
            if Config.holdingsDf.ix[i, "Account"] != account:
                continue
            
            pf.ix[row, "Ticker"] = ticker
            pf.ix[row+1, "Ticker"] = " " + morningstar.ticker_name(ticker.upper())

            # Compute the units
            units = 0
            unitsSet = True
            costBasis = 0
            costBasisSet = True
            
            for j in range(Config.holdingsDf.shape[0]):
                if Config.holdingsDf.ix[j, "Ticker"] != ticker:
                    continue
                if Config.holdingsDf.ix[j, "Account"] != account:
                    continue

                units1 = Config.holdingsDf.ix[j, "Units"]
                costBasis1 = Config.holdingsDf.ix[j, "Cost Basis"]

                if units1:
                    units = units + Format.StringToFloat(units1)
                else:
                    unitsSet = False
                if costBasis1:
                    costBasis = costBasis + Format.StringToFloat(costBasis1)
                else:
                    costBasisSet = False

            if unitsSet:
                pf.ix[row, "Units"] = "{:,.3f}".format(units)
            else:
                pf.ix[row, "Units"] = ""
            pf.ix[row+1, "Units"] = ""
            
            pf.ix[row, "Last Price"] = ""
            pf.ix[row+1, "Last Price"] = ""

            pf.ix[row, "Current Value"] = ""
            pf.ix[row+1, "Current Value"] = ""

            if unitsSet and units and costBasisSet:
                pf.ix[row, "Cost Basis"] = "$" + "{:,.2f}".format(costBasis/units) + "/Share"
                pf.ix[row+1, "Cost Basis"] = " $" + "{:,.2f}".format(costBasis, 2)
            else:
                pf.ix[row, "Cost Basis"] = ""
            
            row = row+2
    
        pf.ix[row, "Ticker"] = ""
        pf.ix[row, "Last Price"] = ""
        pf.ix[row, "Units"] = ""
        pf.ix[row, "Current Value"] = ""
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

