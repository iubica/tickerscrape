#!/usr/bin/env python

import sys, os

try:
    path = os.path.dirname(__file__)
    os.chdir(path)
except:
    pass

# Add these folders to the module search path
sys.path.append(".")
sys.path.append("src")
sys.path.append("views")
sys.path.append("widgets")
sys.path.append("scrape")

import TickerMain
TickerMain.main()
