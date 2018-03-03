import sys, os
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    os.environ['TCL_LIBRARY'] = "C:\\Users\\andrei\\AppData\\Local\\Programs\\Python\\Python36\\DLLs"
    os.environ['TK_LIBRARY'] = "C:\\Users\\andrei\\AppData\\Local\\Programs\\Python\\Python36\\DLLs"

executables = [
    Executable('wxPortfolio.py', base=base)
]

# Dependencies are automatically detected, but might need fine tuning.
build_exe_options = {
    'packages': ['idna'],
    'includes': ['pandas', 'numpy', 
                 'wx', 'wx.adv', 'wx.lib.agw.aui', 'wx.html',
                 'wx.lib.msgpanel', 'wx.lib.mixins.inspection',
                 'wx.dataview',
                 'requests',
                 'bs4',
                 'six',
                 'tabulate',
                 'unidecode',
                 'xml.etree.ElementTree'],
    'include_files': ['bitmaps/', 'bmp_source/', 'cursors/', 'data/', 
                      'scrape/', 'views/', 'widgets/']
    }

# To do: need to vastly expand the list of include_files, else wxPython does not find the bits and pieces it needs.

setup(name='wxPortfolio',
      version='0.1',
      description='Portfolio management software',
      options = {"build_exe" : build_exe_options},
      executables=executables
)
