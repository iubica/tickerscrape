"""
Status bar functionality
"""
import wx

_statusBar = None

def Init(sb):
    """ 
    Description:
    Initialize the status bar.

    Arguments:
    sb - the status bar object
    """
    global _statusBar
    _statusBar = sb
    
def DeInit():
    """ 
    Description:
    Deinitialize the status bar
    """
    _statusBar = None

def Set(msg, field = 0, time = 3):
    """ 
    Set the status text.

    Arguments:
    msg - the text message
    field - the field to set
    time - how long to keep the message
    """
    _statusBar.SetStatusText(msg, field)
