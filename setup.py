import sys, os
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    os.environ['TCL_LIBRARY'] = "C:\\Users\\andrei\\AppData\\Local\\Programs\\Python\\Python36\\DLLs"
    os.environ['TK_LIBRARY'] = "C:\\Users\\andrei\\AppData\\Local\\Programs\\Python\\Python36\\DLLs"

executables = [
    Executable('TickerScrape.py', base=base)
]

# Dependencies are automatically detected, but might need fine tuning.
build_exe_options = {
    'packages': ['numpy', 'pandas', 'idna'],
    'includes': ['numpy', 'pandas',  
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
                      'scrape/', 'views/', 'widgets/',
                      'Main.py', 'Format.py', 'TickerScrape.iss', 'README.md'],
    # Modules referenced by dynamic modules under 'views/' but not included
    # in Main.py must be include_files. For example: Format.py.
    'include_msvcr': True, # Some users of cx_freeze swear this is needed
    }

setup(name='wxPortfolio',
      version='0.1',
      description='Portfolio management software',
      options = {"build_exe" : build_exe_options},
      executables=executables
)
