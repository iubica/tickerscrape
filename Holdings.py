#!/usr/bin/env python
#	Tags: phoenix-port, py3-port

import wx
import wx.dataview as dv
import os, sys
import csv
import pandas as pd
import Config
import tickerscrape.morningstar

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
    def __init__(self, log):
        dv.DataViewIndexListModel.__init__(self, Config.holdingsDf.shape[0])
        self.log = log

    # Convert model column to data frame column
    def _GetDataFrameCol(self, modelCol):
        dataFrameCol = None
        
        if modelCol == 0:
            dataFrameCol = 0
        elif modelCol == 1:
            dataFrameCol = 1
        elif modelCol == 3:
            dataFrameCol = 2
        elif modelCol == 4:
            dataFrameCol = 3
        elif modelCol == 5:
            dataFrameCol = 4

        return dataFrameCol

    # Convert data frame column to model column
    def _GetModelCol(self, dataFrameCol):
        modelCol = None

        if dataFrameCol == 0:
            modelCol = 0
        elif dataFrameCol == 1:
            modelCol = 1
        elif dataFrameCol == 2:
            modelCol = 3
        elif dataFrameCol == 3:
            modelCol = 4
        elif dataFrameCol == 4:
            modelCol = 5

        return modelCol

    # All of our columns are strings.  If the model or the renderers
    # in the view are other types then that should be reflected here.
    def GetColumnType(self, col):
        colType = "string"
        
        return colType

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row, col):
        if col == 2:
            ticker = Config.holdingsDf.iloc[row, 1]
            value = tickerscrape.morningstar.name(ticker)
            return value if value else ""

        dataFrameCol = self._GetDataFrameCol(col)
        
        value = ""
        if dataFrameCol is not None:
            value = str(Config.holdingsDf.iloc[row, dataFrameCol])

        #self.log.write("GetValue: (%d,%d) %s\n" % (row, col, value))
        return value

    # This method is called when the user edits a data item in the view.
    def SetValueByRow(self, value, row, col):
        #self.log.write("SetValue: (%d,%d) %s\n" % (row, col, value))
        dataFrameCol = self._GetDataFrameCol(col)
 
        if not self.ValidateValueByRow(value, row, col):
            return False

        if dataFrameCol is not None:
            Config.holdingsDf.iloc[row, dataFrameCol] = value
            Config.HoldingsChanged(True)
            return True

        return False

    def ValidateValueByRow(self, value, row, col):
        if col == 0:
            if not Config.AccountFind(value):
                self.log.write("Invalid account '%s', should be one of %s\n" % (value, Config.AccountList()))
                return False

        return True

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return 5

    # Report the number of rows in the model
    def GetRowCount(self):
        rowCount = Config.holdingsDf.shape[0]
        #self.log.write('GetRowCount() = %d' % rowCount)
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


    # This is called to assist with sorting the data in the view.  The
    # first two args are instances of the DataViewItem class, so we
    # need to convert them to row numbers with the GetRow method.
    # Then it's just a matter of fetching the right values from our
    # data set and comparing them.  The return value is -1, 0, or 1,
    # just like Python's cmp() function.
    def Compare(self, item1, item2, col, ascending):
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        if col == 0:
            return cmp(int(Config.holdingsDf.iloc[row1, col]), int(Config.holdingsDf.iloc[row2, col]))
        else:
            return cmp(Config.holdingsDf.iloc[row1, col], self.idata[row2, col])

    def AddRow(self, id, value):
        self.log.write('AddRow(%s)' % value)
        # update data structure
        Config.holdingsDf.loc[id-1] = value
        # notify views
        self.RowAppended()

    def DeleteRows(self, rows):
        self.log.write('DeleteRows(%s)' % rows)

        # Drop the list of rows from the dataframe
        Config.holdingsDf.drop(rows, inplace=True)
        # Reset the dataframe index, and don't add an index column
        Config.holdingsDf.reset_index(inplace=True, drop=True)

        # notify the view(s) using this model that it has been removed
        self.Reset(Config.holdingsDf.shape[0])        

    def MoveUp(self, rows):
        self.log.write("MoveUp() rows %s\n" % rows)

        if rows:
            for row in rows:
                a = Config.holdingsDf.iloc[row-1].copy()
                b = Config.holdingsDf.iloc[row].copy()
                Config.holdingsDf.iloc[row-1] = b
                Config.holdingsDf.iloc[row] = a
                Config.HoldingsChanged(True)

            # notify the view(s) using this model that it has been removed
            self.Reset(Config.holdingsDf.shape[0])        

    def MoveDown(self, rows):
        self.log.write("MoveDown() rows %s\n" % rows)

        if rows:
            for row in rows:
                a = Config.holdingsDf.iloc[row+1].copy()
                b = Config.holdingsDf.iloc[row].copy()
                Config.holdingsDf.iloc[row+1] = b
                Config.holdingsDf.iloc[row] = a
                Config.HoldingsChanged(True)

            # notify the view(s) using this model that it has been removed
            self.Reset(Config.holdingsDf.shape[0])        

class HoldingsPanel(wx.Panel):
    def __init__(self, parent, log, model=None):
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
            self.model = HoldingsModel(log)
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
        self.dvc.AppendTextColumn("Account", 0, width=150,
                                  mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Ticker", 1, width=70,
                                  mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Name", 2, width=150)
        self.dvc.AppendTextColumn("Shares", 3, width=80, 
                                  mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Cost Basis", 4, width=100, 
                                  mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Purchase Date", 5, width=100, 
                                  mode=dv.DATAVIEW_CELL_EDITABLE)

        # Through the magic of Python we can also access the columns
        # as a list via the Columns property.  Here we'll mark them
        # all as sortable and reorderable.
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

        # set the Sizer property (same as SetSizer)
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)

        # Add some buttons to help out with the tests
        self.buttonAddRow = wx.Button(self, label="Add Row")
        self.Bind(wx.EVT_BUTTON, self.OnAddRow, self.buttonAddRow)
        self.buttonDeleteRows = wx.Button(self, label="Delete Row(s)")
        self.Bind(wx.EVT_BUTTON, self.OnDeleteRows, self.buttonDeleteRows)
        self.buttonMoveUp = wx.Button(self, label="Move Up")
        self.Bind(wx.EVT_BUTTON, self.OnMoveUp, self.buttonMoveUp)
        self.buttonMoveDown = wx.Button(self, label="Move Down")
        self.Bind(wx.EVT_BUTTON, self.OnMoveDown, self.buttonMoveDown)

        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        btnbox.Add(self.buttonAddRow, 0, wx.LEFT|wx.RIGHT, 5)
        btnbox.Add(self.buttonDeleteRows, 0, wx.LEFT|wx.RIGHT, 5)
        btnbox.Add(self.buttonMoveUp, 0, wx.LEFT|wx.RIGHT, 5)
        btnbox.Add(self.buttonMoveDown, 0, wx.LEFT|wx.RIGHT, 5)
        self.Sizer.Add(btnbox, 0, wx.TOP|wx.BOTTOM, 5)

        # Initial state for buttons
        self.buttonDeleteRows.Disable()
        self.buttonMoveUp.Disable()
        self.buttonMoveDown.Disable()

        # Bind some events so we can see what the DVC sends us
        self.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.OnEditingDone, self.dvc)
        self.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnValueChanged, self.dvc)
        self.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.OnSelectionChanged, self.dvc)


    def OnDeleteRows(self, evt):
        # Remove the selected row(s) from the model. The model will take care
        # of notifying the view (and any other observers) that the change has
        # happened.
        items = self.dvc.GetSelections()
        rows = [self.model.GetRow(item) for item in items]

        self.log.write("OnDeleteRows() rows %s\n" % rows)
        self.model.DeleteRows(rows)


    def OnAddRow(self, evt):
        # Add some bogus data to a new row in the model's data
        id = len(Config.holdingsDf) + 1
        self.log.write("OnAddRow() id %d\n" % id)
        value = ["", "New ticker", "", "", ""]
        self.model.AddRow(id, value)

        # Clear the selection
        self.dvc.SetSelections(dv.DataViewItemArray())

    def OnMoveUp(self, evt):
        items = self.dvc.GetSelections()
        rows = [self.model.GetRow(item) for item in items]

        self.model.MoveUp(rows)

        # Keep the moved-up rows selected
        items = dv.DataViewItemArray()
        for row in rows:
            items.append(self.model.GetItem(row - 1))
            self.dvc.SetSelections(items)

    def OnMoveDown(self, evt):
        items = self.dvc.GetSelections()
        rows = [self.model.GetRow(item) for item in items]

        self.model.MoveDown(rows)

        # Keep the moved-down rows selected
        items = dv.DataViewItemArray()
        for row in rows:
            items.append(self.model.GetItem(row + 1))
            self.dvc.SetSelections(items)

    def OnEditingDone(self, evt):
        #self.log.write("OnEditingDone\n")
        pass

    def OnValueChanged(self, evt):
        # Can be used to verify format validity
        #self.log.write("OnValueChanged\n")
        pass

    def OnSelectionChanged(self, evt):

        items = self.dvc.GetSelections()
        rows = [self.model.GetRow(item) for item in items]

        self.log.write("OnSelectionChanged, rows selected %s\n" % rows)
        
        # Is there any selection?
        if rows == []:
            self.buttonDeleteRows.Disable()
        else:
            self.buttonDeleteRows.Enable()

        # Is the top line selected?
        if 0 in rows:
            self.buttonMoveUp.Disable()
        else:
            self.buttonMoveUp.Enable()

        # Is the bottom line selected?
        if (self.model.GetRowCount() - 1) in rows:
            self.buttonMoveDown.Disable()
        else:
            self.buttonMoveDown.Enable()
            

#----------------------------------------------------------------------

def GetWindow(frame, nb, log):
    
    if Config.holdingsDf is None:
        Config.HoldingsRead()

    if Config.accountsDf is None:
        Config.AccountsRead()

    print(Config.holdingsDf)

    win = HoldingsPanel(nb, log)
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

