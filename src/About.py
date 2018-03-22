#!/usr/bin/env python

import sys

import wx
import wx.html
import wx.lib.wxpTag

import version

#---------------------------------------------------------------------------

class MyAboutBox(wx.Dialog):
    text = '''
<html>
<body bgcolor="#4169e1">
<center><table bgcolor="#e18b5c" width="100%%" cellspacing="0"
cellpadding="0" border="1">
<tr>
    <td align="center">
    <h1>TickerScrape %s</h1>
    (%s)<br>
    Running on Python %s and wxPython %s.<br>
    </td>
</tr>
</table>

<p><b>TickerScrape</b> is a toolkit for investment portfolio management.</p> 

<p>It is written by <b>Andrei Radulescu-Banu</b>, Copyright (c) 2018, and it is released under an MIT license.</p>

<p><b>wxPython</b> is produced by <b>Robin Dunn</b> and<br>
<b>Total Control Software,</b> Copyright (c) 1997-2017.</p>

<p><wxp module="wx" class="Button">
    <param name="label" value="Okay">
    <param name="id" value="ID_OK">
</wxp></p>
</center>
</body>
</html>
'''
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About the wxPython demo',)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
            html.SetStandardFonts()
        py_version = sys.version.split()[0]
        txt = self.text % (version.VERSION_STRING,
                           ", ".join(wx.PlatformInfo[1:]),
                           py_version, 
                           wx.VERSION_STRING
                           )
        html.SetPage(txt)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)

#---------------------------------------------------------------------------



if __name__ == '__main__':
    app = wx.App()
    dlg = MyAboutBox(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()

