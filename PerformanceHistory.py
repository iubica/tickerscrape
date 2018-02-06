#!/usr/bin/env python
#	Tags: phoenix-port, py3-port

import wx
import pandas as pd
import DataFrameViewCtrl
import Config

#---------------------------------------------------------------------------

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    
    if Config.holdingsDf is None:
        Config.GetHoldings()

    win = DataFrameViewCtrl.Panel(nb, Config.holdingsDf, log)
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

