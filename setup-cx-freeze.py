import sys, os
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    os.environ['TCL_LIBRARY'] = "C:\\Users\\andrei\\AppData\\Local\\Programs\\Python\\Python36\\DLLs"
    os.environ['TK_LIBRARY'] = "C:\\Users\\andrei\\AppData\\Local\\Programs\\Python\\Python36\\DLLs"

executables = [
    Executable('TickerScrape.py', base=base, icon="bitmaps/ticker-scrape-logo.ico")

# Dependencies are automatically detected, but might need fine tuning.
build_exe_options = {
    # Full packages
    'packages': ['bs4', 'idna', 'numpy', 'pandas', 'platform', 'psutil', 
                 'requests', 'six', 'tabulate', 'unidecode', 'wx', 'xml'],
    # Additional modules inside other packages
    'includes': [],
    # List of excluded modules. Will exclude TickerMain, we include it
    # as source file.
    'excludes': ['TickerMain'],
    # Local files and folders
    'include_files': ['bitmaps/', 'bmp_source/', 'cursors/', 'data/', 
                      'scrape/', 'src/', 'views/', 'widgets/',
                      'README.md'],
    # Modules referenced by dynamic modules under 'views/' but not included
    # in Main.py must be include_files. For example: Format.py.
    'include_msvcr': True, # Some users of cx_freeze swear this is needed
    }

if sys.platform == 'win32':
    build_exe_options['include_files'].append('TickerScrape.iss')
    
setup(name='wxPortfolio',
      version='0.1',
      description='Portfolio management software',
      options = {"build_exe" : build_exe_options},
      executables=executables
)
