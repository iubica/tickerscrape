# viewdata.py

"""
Globals for the main.py wxPython views.
"""

import wx
import pandas as pd
import Main

#-------------------------------------------------------------------------------
#
# viewPngs
#
# These are the images names used in the wxPortfolio treectrl.
# These come from images.py or bitmaps/imagename.ext
#
# viewPngs = ["imagename1", "imagename2", "etc"]
#
#-------------------------------------------------------------------------------

viewPngs = ["overview", # Top level views
            "custom", # Portfolio
            "custom", # Performance
            "custom", # Config
            "recent", # Recent Additions/Updates
            "frame",  # ...
            "dialog", 
            "moredialog", 
            "core",
            "book", 
            "customcontrol", 
            "morecontrols", 
            "layout", 
            "process",
            "clipboard", 
            "images", 
            "miscellaneous"]


#-------------------------------------------------------------------------------
#
# viewTree
#
# These are the View Catagory Headers
# and View Module Names(Ex: Frame.py without ext)
#
# ('View Category Name', [
#       'ViewModuleName1',
#       'ViewModuleName2',
#       'Etc',
#       ]),
#
# The ViewModuleName should correspond to a ViewModuleName.py file in the
# top folder, with the following globals and methods:
#   overview - HTML string showing in the Help tab 
#   runTest(frame, nb, log) - returns panel object for module
#
#-------------------------------------------------------------------------------

viewTree = [
    # portfolio views
    ('Portfolio', [
        'Holdings',
        'Accounts',
    ]),

    ('Performance', [
        'PerformanceHistory',
        'TrailingTotalReturns',
    ]),

    ('Config', [
        'AccountTypes',
    ]),

    # new stuff
    ('Recent Additions/Updates', [
        'FileCtrl',
        'Overlay',
        'RearrangeDialog',
        'RichMessageDialog',
        'ToolTip',
        'TimePickerCtrl',
        'BannerWindow',
    ]),

    # managed windows == things with a (optional) caption you can close
    ('Frames and Dialogs', [
        'AUI_DockingWindowMgr',
        'AUI_MDI',
        'Dialog',
        'Frame',
        'MDIWindows',
        'MiniFrame',
        'Wizard',
    ]),

    # the common dialogs
    ('Common Dialogs', [
        'AboutBox',
        'ColourDialog',
        'DirDialog',
        'FileDialog',
        'FindReplaceDialog',
        'FontDialog',
        'MessageDialog',
        'MultiChoiceDialog',
        'PageSetupDialog',
        'PrintDialog',
        'ProgressDialog',
        'SingleChoiceDialog',
        'TextEntryDialog',
        'RearrangeDialog',
        'RichMessageDialog',
        'NotificationMessage',
        'RichToolTip',
    ]),

    # dialogs from libraries
    ('More Dialogs', [
        'ImageBrowser',
        'ScrolledMessageDialog',
    ]),

    # core controls
    ('Core Windows/Controls', [
        'BitmapButton',
        'Button',
        'CheckBox',
        'CheckListBox',
        'Choice',
        'ComboBox',
        'CommandLinkButton',
        'DVC_CustomRenderer',
        'DVC_DataViewModel',
        'DVC_IndexListModel',
        'DVC_ListCtrl',
        'DVC_TreeCtrl',
        'Gauge',
        'Grid',
        'Grid_MegaExample',
        'GridLabelRenderer',
        'ListBox',
        'ListCtrl',
        'ListCtrl_virtual',
        'ListCtrl_edit',
        'Menu',
        'PopupMenu',
        'PopupWindow',
        'RadioBox',
        'RadioButton',
        'SashWindow',
        'ScrolledWindow',
        'SearchCtrl',
        'Slider',
        'SpinButton',
        'SpinCtrl',
        'SpinCtrlDouble',
        'SplitterWindow',
        'StaticBitmap',
        'StaticBox',
        'StaticText',
        'StatusBar',
        'StockButtons',
        'TextCtrl',
        'ToggleButton',
        'ToolBar',
        'TreeCtrl',
        'Validator',
    ]),

    ('"Book" Controls', [
        'AUI_Notebook',
        'Choicebook',
        'FlatNotebook',
        'Listbook',
        'Notebook',
        'Toolbook',
        'Treebook',
    ]),

    ('Custom Controls', [
        'AnalogClock',
        'ColourSelect',
        'ComboTreeBox',
        'Editor',
        'FileCtrl',
        'GenericButtons',
        'GenericDirCtrl',
        'ItemsPicker',
        #'LEDNumberCtrl',  # TODO
        'MultiSash',
        'PlateButton',
        'PopupControl',
        'PyColourChooser',
        'TreeListCtrl',  # TODO or toss it?
    ]),

    # controls coming from other libraries
    ('More Windows/Controls', [
        'ActiveX_FlashWindow',
        'ActiveX_IEHtmlWindow',
        'ActiveX_PDFWindow',
        'BitmapComboBox',
        'Calendar',
        'CalendarCtrl',
        'CheckListCtrlMixin',
        'CollapsiblePane',
        'ComboCtrl',
        'ContextHelp',
        'DatePickerCtrl',
        #'DynamicSashWindow',  # TODO
        'EditableListBox',
        'ExpandoTextCtrl',
        'FancyText',
        'FileBrowseButton',
        'FloatBar',
        'FloatCanvas',
        'HtmlWindow',
        'HTML2_WebView',
        'InfoBar',
        'IntCtrl',
        'MaskedEditControls',
        'MaskedNumCtrl',
        'MediaCtrl',
        'MultiSplitterWindow',
        'OwnerDrawnComboBox',
        'Pickers',
        'PropertyGrid',
        'PyCrust',
        'PyPlot',
        'PyShell',
        'ResizeWidget',
        'RichTextCtrl',
        'ScrolledPanel',
        #'SplitTree',         # TODO or toss it?
        'StyledTextCtrl_1',
        'StyledTextCtrl_2',
        'TablePrint',
        'Throbber',
        'Ticker',
        'TimeCtrl',
        'TimePickerCtrl',
        'TreeMixin',
        'VListBox',
    ]),

    # How to lay out the controls in a frame/dialog
    ('Window Layout', [
        'GridBagSizer',
        'LayoutAnchors',
        'LayoutConstraints',
        'Layoutf',
        'ScrolledPanel',
        'SizedControls',
        'Sizers',
        'WrapSizer',
        'XmlResource',
        'XmlResourceHandler',
        'XmlResourceSubclass',
    ]),

    # ditto
    ('Process and Events', [
        'DelayedResult',
        'EventManager',
        'KeyEvents',
        'Process',
        'PythonEvents',
        'Threads',
        'Timer',
        ##'infoframe',    # needs better explanation and some fixing
    ]),

    # Clipboard and DnD
    ('Clipboard and DnD', [
        'CustomDragAndDrop',
        'DragAndDrop',
        'URLDragAndDrop',
    ]),

    # Images
    ('Using Images', [
        'AdjustChannels',
        'AlphaDrawing',
        'AnimateCtrl',
        'ArtProvider',
        'BitmapFromBuffer',
        'Cursor',
        'DragImage',
        'Image',
        'ImageAlpha',
        'ImageFromStream',
        'Img2PyArtProvider',
        'Mask',
        'RawBitmapAccess',
        'Throbber',
    ]),

    # Other stuff
    ('Miscellaneous', [
        'AlphaDrawing',
        'BannerWindow',
        'Cairo',
        'Cairo_Snippets',
        'ColourDB',
        ##'DialogUnits',   # needs more explanations
        'DragScroller',
        'DrawXXXList',
        'FileHistory',
        'FontEnumerator',
        'GetMouseState',
        'GraphicsContext',
        'GraphicsGradient',
        'GLCanvas',
        'I18N',
        'Joystick',
        'MimeTypesManager',
        'MouseGestures',
        'OGL',
        'Overlay',
        'PDFViewer',
        'PenAndBrushStyles',
        'PrintFramework',
        'PseudoDC',
        'RendererNative',
        'ShapedWindow',
        'Sound',
        'StandardPaths',
        'SystemSettings',
        'ToolTip',
        'UIActionSimulator',
        'Unicode',
    ]),

    ('Check out the samples dir too', []),

]

#---------------------------------------------------------------------------
# Get the entire portfolio
def PortfolioRead():
    HoldingsRead()
    AccountsRead()
    AccountTypesRead()

#---------------------------------------------------------------------------
# Save the entire portfolio
def PortfolioSave():
    HoldingsSave()
    AccountsSave()
    AccountTypesSave()

#---------------------------------------------------------------------------
# Called with changed = True or False when holdings are different (or unchanged)
# from the holdings.csv, and called with changed = None to just return
# the status of the holdings (whether they have changed or not)

def PortfolioChanged():
    return _holdingsChanged or _accountsChanged or _accountTypesChanged

#---------------------------------------------------------------------------

# The holdings dataframe
holdingsDf = None
_holdingsChanged = False

#---------------------------------------------------------------------------
# Get portfolio holdings from holdings.csv

def HoldingsRead():
    # Get the wxPython standard paths
    sp = wx.StandardPaths.Get()

    # Get the global holdings table
    global holdingsDf

    try:
        holdingsDf = pd.read_csv(sp.GetUserDataDir() + "/holdings.csv")

        HoldingsChanged(False)
    except OSError as e:
        # Create an empty DataFrame with unordered columns
        holdingsDf = pd.DataFrame.from_dict({
            "Account": ["", ""],
            "Ticker": ["SPY", "FUSEX"],
            "Shares": ["100", "150"],
            "Cost Basis": ["150000.00", "100.00"],
            "Purchase Date": ["2/3/2011", "2/4/2011"]
        })
        
        # Order the columns
        holdingsDf = holdingsDf[["Account",
                                 "Ticker", 
                                 "Shares", 
                                 "Cost Basis", 
                                 "Purchase Date"]]

        # Holdings have been modified
        HoldingsChanged(True)

    holdingsDf.fillna("", inplace=True)
    #print(holdingsDf)

#---------------------------------------------------------------------------
# Save portfolio holdings to holdings.csv

def HoldingsSave():
    # Get the wxPython standard paths
    sp = wx.StandardPaths.Get()

    # Save the holdings table
    df = holdingsDf.set_index("Account", inplace=False)    
    df.to_csv(sp.GetUserDataDir() + "/holdings.csv")

    # Holdings are now in sync
    HoldingsChanged(False)

#---------------------------------------------------------------------------
# Called with changed = True or False when holdings are different (or unchanged)
# from the holdings.csv, and called with changed = None to just return
# the status of the holdings (whether they have changed or not)

def HoldingsChanged(changed):
    global _holdingsChanged

    if changed is not None:
        if Main.portfolioFrame:
            Main.portfolioFrame.EnableFileMenuSaveItem(changed)
        _holdingsChanged = changed

    return _holdingsChanged


#---------------------------------------------------------------------------

# The accounts dataframe
accountsDf = None
_accountsChanged = False

#---------------------------------------------------------------------------
# Get portfolio accounts from accounts.csv

def AccountsRead():
    # Get the wxPython standard paths
    sp = wx.StandardPaths.Get()

    # Get the global accounts table
    global accountsDf

    try:
        accountsDf = pd.read_csv(sp.GetUserDataDir() + "/accounts.csv")

        AccountsChanged(False)
    except OSError as e:
        # Create an empty DataFrame with unordered columns
        accountsDf = pd.DataFrame.from_dict({
            "Account Name": ["Account One", "Account Two"],
            "Account Number": ["100", "101"],
            "Type": ["Brokerage", "401K"],
        })
        
        # Order the columns
        accountsDf = accountsDf[["Account Name", 
                                 "Account Number", 
                                 "Type"]]

        # Accounts have been modified
        AccountsChanged(True)

    accountsDf.fillna("", inplace=True)
    #print(accountsDf)

#---------------------------------------------------------------------------
# Save portfolio accounts to accounts.csv

def AccountsSave():
    # Get the wxPython standard paths
    sp = wx.StandardPaths.Get()

    # Save the accounts table
    df = accountsDf.set_index("Account Name", inplace=False)    
    df.to_csv(sp.GetUserDataDir() + "/accounts.csv")

    # Accounts are now in sync
    AccountsChanged(False)

#---------------------------------------------------------------------------
# Called with changed = True or False when accounts are different (or unchanged)
# from the accounts.csv, and called with changed = None to just return
# the status of the accounts (whether they have changed or not)

def AccountsChanged(changed):
    global _accountsChanged

    if changed is not None:
        if Main.portfolioFrame:
            Main.portfolioFrame.EnableFileMenuSaveItem(changed)
        _accountsChanged = changed

    return _accountsChanged

#---------------------------------------------------------------------------
def AccountList():
    return accountsDf.iloc[:,0].tolist()

#---------------------------------------------------------------------------
def AccountFind(acct):
    acctList = accountsDf.iloc[:,0].tolist()
    if acct in acctList:
        return True
    return False

#---------------------------------------------------------------------------
def AccountChange(acctOld, acctNew):
    acctChanged = False
    holdingsChanged = False

    if AccountFind(acctNew):
        return False, "Account '%s' already configured" % acctNew

    for i in range(accountsDf.shape[0]):
        if accountsDf.iloc[i,0] == acctOld:
            accountsDf.iloc[i,0] = acctNew
            acctChanged = True

    if not acctChanged:
        return False, "Account '%s' does not exist" % acctOld

    # Also change the holdings
    for i in range(holdingsDf.shape[0]):
        if holdingsDf.iloc[i,0] == acctOld:
            holdingsDf.iloc[i,0] = acctNew
            holdingsChanged = True

    if acctChanged:
        AccountsChanged(True)

    if holdingsChanged:
        HoldingsChanged(True)

    return True, None


#---------------------------------------------------------------------------

# The accounts dataframe
accountTypesDf = None
_accountTypesChanged = False

#---------------------------------------------------------------------------
# Get portfolio account types from accountTypes.csv

def AccountTypesRead():
    # Get the wxPython standard paths
    sp = wx.StandardPaths.Get()

    # Get the global accounts table
    global accountTypesDf

    try:
        accountTypesDf = pd.read_csv(sp.GetUserDataDir() + "/accountTypes.csv")

        AccountTypesChanged(False)
    except OSError as e:
        # Create an empty DataFrame with unordered columns
        accountTypesDf = pd.DataFrame.from_dict({
            "Account Type": ["Brokerage", "401K", "Roth 401K", "IRA", "Roth IRA", "529"],
            "Long Term Capital Gains Tax": ["15%", "", "", "", "", ""],
            "Short Term Capital Gains Tax": ["35%", "", "", "", "", ""],
            "Liquidation Tax": ["", "35%", "", "35%", "", ""],
        })
        
        # Order the columns
        accountTypesDf = accountTypesDf[["Account Type", 
                                         "Long Term Capital Gains Tax", 
                                         "Short Term Capital Gains Tax", 
                                         "Liquidation Tax"]]
        
        # Accounts have been modified
        AccountTypesChanged(True)

    accountTypesDf.fillna("", inplace=True)
    #print(accountsDf)

#---------------------------------------------------------------------------
# Save portfolio account types to accountTypes.csv

def AccountTypesSave():
    # Get the wxPython standard paths
    sp = wx.StandardPaths.Get()

    # Save the accounts table
    df = accountTypesDf.set_index("Account Type", inplace=False)    
    df.to_csv(sp.GetUserDataDir() + "/accountTypes.csv")

    # AccountTypes are now in sync
    AccountTypesChanged(False)

#---------------------------------------------------------------------------
def AccountTypesChanged(changed):
    global _accountTypesChanged

    if changed is not None:
        if Main.portfolioFrame:
            Main.portfolioFrame.EnableFileMenuSaveItem(changed)
        _accountTypesChanged = changed

    return _accountTypesChanged

#---------------------------------------------------------------------------
def AccountTypesList():
    return accountTypesDf.iloc[:,0].tolist()

#---------------------------------------------------------------------------
def AccountTypesFind(acct):
    acctList = accountTypesDf.iloc[:,0].tolist()
    if acct in acctList:
        return True
    return False

#---------------------------------------------------------------------------
def AccountTypesChange(acctTypeOld, acctTypeNew):
    acctTypesChanged = False
    acctChanged = False

    if AccountTypesFind(acctTypeNew):
        return False, "Account type '%s' already configured" % acctTypeNew

    for i in range(accountTypesDf.shape[0]):
        if accountTypesDf.iloc[i,0] == acctTypeOld:
            accountTypesDf.iloc[i,0] = acctTypeNew
            acctTypesChanged = True

    if not acctTypesChanged:
        return False, "Account type '%s' does not exist" % acctTypeOld

    # Also change the holdings
    for i in range(accountsDf.shape[0]):
        if accountsDf.iloc[i,0] == acctTypeOld:
            accountsDf.iloc[i,0] = acctTypeNew
            acctChanged = True

    if acctTypesChanged:
        AccountTypesChanged(True)

    if acctChanged:
        AccountsChanged(True)

    return True, None
