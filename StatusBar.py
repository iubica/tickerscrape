"""
Status bar functionality
"""
import wx
if not "wxGTK" in wx.PlatformInfo:
    import time, threading

_statusBar = None
_statusBarTimer = None

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
    
    global _statusBarTimer
    global _statusBar

    if not "wxGTK" in wx.PlatformInfo:
        # Reset the timer
        if _statusBarTimer:
            _statusBarTimer.cancel()

    # Release memory
    _statusBarTimer = None
    _statusBar = None

def _TimerCallback():
    """ 
    Description:
    Called upon timer expiration to clear the status text
    """
    
    _statusBar.SetStatusText("", 0)

def Set(msg, time = 3):
    """ 
    Set the status text.

    Arguments:
    msg - the text message
    time - how long to keep the message, in seconds
    """
    _statusBar.SetStatusText(msg, 0)
    
    global _statusBarTimer

    if not "wxGTK" in wx.PlatformInfo:
        # Reset the timer
        if _statusBarTimer:
            _statusBarTimer.cancel()
    
        # Should we set a timer?
        if time:
            _statusBarTimer = threading.Timer(time, _TimerCallback)
            _statusBarTimer.start()
