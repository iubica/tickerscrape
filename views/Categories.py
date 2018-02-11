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

class CategoriesModel(dv.DataViewIndexListModel):
    def __init__(self, log):
        dv.DataViewIndexListModel.__init__(self, Config.categoriesDf.shape[0])
        self.log = log

    # Convert model column to data frame column
    def _GetDataFrameCol(self, modelCol):
        return modelCol

    # Convert data frame column to model column
    def _GetModelCol(self, dataFrameCol):
        return dataFrameCol

    # All of our columns are strings.  If the model or the renderers
    # in the view are other types then that should be reflected here.
    def GetColumnType(self, col):
        return "string"

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row, col):
        dataFrameCol = self._GetDataFrameCol(col)
        
        value = ""
        if dataFrameCol is not None:
            value = str(Config.categoriesDf.iloc[row, dataFrameCol])

        #self.log.write("GetValue: (%d,%d) %s\n" % (row, col, value))
        return value

    # This method is called when the user edits a data item in the view.
    def SetValueByRow(self, value, row, col):
        dataFrameCol = self._GetDataFrameCol(col)
 
        #self.log.write("SetValue: (%d,%d) %s\n" % (row, col, value))

        if not self.ValidateValueByRow(value, row, col):
            return False

        if dataFrameCol is not None:
            if col == 0:
                ret, err = Config.CategoriesChange(Config.categoriesDf.iloc[row, dataFrameCol], value)
                if not ret:
                    self.log.write("%s\n", err)
                return ret
            else:
                # Simple change of values
                Config.categoriesDf.iloc[row, dataFrameCol] = value
                Config.CategoriesChanged(True)

            return True

        return False

    def ValidateValueByRow(self, value, row, col):
        if col == 0:
            # Prevent duplicate categories
            for i in range(Config.categoriesDf.shape[0]):
                if i == row:
                    continue
                if Config.categoriesDf.ix[i,"Category Name"] == value:
                    self.log.write("Duplicate category name '%s' not allowed\n" % value)
                    return False

        return True

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return 3

    # Report the number of rows in the model
    def GetRowCount(self):
        rowCount = Config.categoriesDf.shape[0]
        #self.log.write('GetRowCount() = %d' % rowCount)
        return rowCount

    # Called to check if non-standard attributes should be used in the
    # cell at (row, col)
    def GetAttrByRow(self, row, col, attr):
        return False

    def AddRow(self, id, value):
        #self.log.write('AddRow(%s)' % value)
        # update data structure
        Config.categoriesDf.loc[id-1] = value
        # notify views
        self.RowAppended()

    def DeleteRows(self, rows):
        #self.log.write('DeleteRows(%s)' % rows)

        # Drop the list of rows from the dataframe
        Config.categoriesDf.drop(rows, inplace=True)
        # Reset the dataframe index, and don't add an index column
        Config.categoriesDf.reset_index(inplace=True, drop=True)

        # notify the view(s) using this model that it has been removed
        self.Reset(Config.categoriesDf.shape[0])        

    def MoveUp(self, rows):
        #self.log.write("MoveUp() rows %s\n" % rows)

        if rows:
            for row in rows:
                a = Config.categoriesDf.iloc[row-1].copy()
                b = Config.categoriesDf.iloc[row].copy()
                Config.categoriesDf.iloc[row-1] = b
                Config.categoriesDf.iloc[row] = a
                Config.CategoriesChanged(True)

            # notify the view(s) using this model that it has been removed
            self.Reset(Config.categoriesDf.shape[0])        

    def MoveDown(self, rows):
        #self.log.write("MoveDown() rows %s\n" % rows)

        if rows:
            for row in rows:
                a = Config.categoriesDf.iloc[row+1].copy()
                b = Config.categoriesDf.iloc[row].copy()
                Config.categoriesDf.iloc[row+1] = b
                Config.categoriesDf.iloc[row] = a
                Config.CategoriesChanged(True)

            # notify the view(s) using this model that it has been removed
            self.Reset(Config.categoriesDf.shape[0])        

class CategoriesPanel(wx.Panel):
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
            self.model = CategoriesModel(log)
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
        self.dvc.AppendTextColumn("Category Name", 0, width=200,
                                  mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Category Group", 1, width=225,
                                  mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Benchmark", 2, width=100,
                                  mode=dv.DATAVIEW_CELL_EDITABLE)

        for c in self.dvc.Columns:
            c.Sortable = False
            c.Reorderable = False

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
        id = len(Config.categoriesDf) + 1
        self.log.write("OnAddRow() id %d\n" % id)
        value = ["New category name", "", ""]
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

        #self.log.write("OnSelectionChanged, rows selected %s\n" % rows)
        
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
    
    if Config.categoriesDf is None:
        Config.CategoriesRead()

    win = CategoriesPanel(nb, log)
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

