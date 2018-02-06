#!/usr/bin/env python
#	Tags: phoenix-port, py3-port

import wx
import wx.dataview as dv
import os, sys
import csv
import pandas as pd
import Config
#---------------------------------------------------------------------------

#----------------------------------------------------------------------

# This model class provides the data to the view when it is asked for.
# Since it is a list-only model (no hierarchical data) then it is able
# to be referenced by row rather than by item object, so in this way
# it is easier to comprehend and use than other model types.  In this
# example we also provide a Compare function to assist with sorting of
# items in our model.  Notice that the data items in the data model
# object don't ever change position due to a sort or column
# reordering.  The view manages all of that and maps view rows and
# columns to the model's rows and columns as needed.
#
# For this example our data is stored in a simple list of lists.  In
# real life you can use whatever you want or need to hold your data.

class HoldingsModel(dv.DataViewIndexListModel):
    def __init__(self, df, log):
        dv.DataViewIndexListModel.__init__(self, df.shape[0])
        self.df = df
        self.log = log

    # All of our columns are strings.  If the model or the renderers
    # in the view are other types then that should be reflected here.
    def GetColumnType(self, col):
        colType = "string"
        
        return colType

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row, col):
        value = ""
        if self.df.iloc[row, col]:
            value = str(self.df.iloc[row, col])

        self.log.write("GetValue: (%d,%d) %s\n" % (row, col, value))
        return value

    # This method is called when the user edits a data item in the view.
    def SetValueByRow(self, value, row, col):
        return False

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return len(self.df.columns) + 1

    # Report the number of rows in the model
    def GetCount(self):
        rowCount = self.df.shape[0]
        self.log.write('GetRowCount() = %d' % rowCount)
        return rowCount

    # Called to check if non-standard attributes should be used in the
    # cell at (row, col)
    def GetAttrByRow(self, row, col, attr):
        ##self.log.write('GetAttrByRow: (%d, %d)' % (row, col))
        if col == 4:
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

class HoldingsPanel(wx.Panel):
    def __init__(self, parent, df, log, model=None):
        self.df = df
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        # Create a dataview control
        self.dvc = dv.DataViewCtrl(self,
                                   style=wx.BORDER_THEME
                                   | dv.DV_ROW_LINES # nice alternating bg colors
                                   #| dv.DV_HORIZ_RULES
                                   | dv.DV_VERT_RULES
                                   | dv.DV_MULTIPLE
                                   )

        # Create an instance of our simple model...
        if model is None:
            self.model = HoldingsModel(self.df, log)
        else:
            self.model = model

        # ...and associate it with the dataview control.  Models can
        # be shared between multiple DataViewCtrls, so this does not
        # assign ownership like many things in wx do.  There is some
        # internal reference counting happening so you don't really
        # need to hold a reference to it either, but we do for this
        # example so we can fiddle with the model from the widget
        # inspector or whatever.
        self.dvc.AssociateModel(self.model)

        # Now we create some columns.  The second parameter is the
        # column number within the model that the DataViewColumn will
        # fetch the data from.  This means that you can have views
        # using the same model that show different columns of data, or
        # that they can be in a different order than in the model.

        idx = 0
        header_list = list(self.df.columns)

        for column in df:
            self.dvc.AppendTextColumn(header_list[idx], idx, width=100, 
                                      mode=dv.DATAVIEW_CELL_EDITABLE)
            print(df[column])
            idx += 1

        # Through the magic of Python we can also access the columns
        # as a list via the Columns property.  Here we'll mark them
        # all as sortable and reorderable.
        for c in self.dvc.Columns:
            c.Sortable = False
            c.Reorderable = False

        # set the Sizer property (same as SetSizer)
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)

        # Add some buttons to help out with the tests
        self.buttonNewView = wx.Button(self, label="New View", name="newView")
        self.Bind(wx.EVT_BUTTON, self.OnNewView, self.buttonNewView)

        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        btnbox.Add(self.buttonNewView, 0, wx.LEFT|wx.RIGHT, 5)
        self.Sizer.Add(btnbox, 0, wx.TOP|wx.BOTTOM, 5)


    def OnNewView(self, evt):
        f = wx.Frame(None, title="New view, shared model", size=(600,400))
        HoldingsPanel(f, self.df, self.log, self.model)
        b = f.FindWindowByName("newView")
        b.Disable()
        f.Show()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    
    if Config.holdingsDf is None:
        Config.GetHoldings()

    win = HoldingsPanel(nb, Config.holdingsDf, log)
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

