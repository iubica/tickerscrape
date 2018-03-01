#!/usr/bin/env python

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import web
import argparse
import unidecode
import json
import titlecase

"""
Module for parsing Morningstar web data.
"""

_ticker_cache = dict()
_name_cache = dict()

def ticker_type(ticker):
    """
    Description:
    Finds the security type.

    Parameters:
    ticker - The security ticker.

    Returns:
    A string with value "Cash", "CEF", "ETF", "Index", "Mutual Fund", "Stock"
    (or "" in case the ticker is neither)
    """

    # Special case for cash
    if ticker.lower() == "cash":
        return "Cash"

    if ticker in _ticker_cache:
        return(_ticker_cache[ticker])
    
    # The Fidelity URL 
    url = "https://fastquote.fidelity.com/service/quote/json?productid=embeddedquotes&symbols="
    
    # Get the page
    r = web.get_web_page(url + ticker, False)
    #print(r[1:-1])
    
    # Strip the '(' at beginning and the ')' at end
    data = json.loads(r[1:-1])
    #print(data)
    
    if (data["STATUS"]["ERROR_CODE"] != "0"):
        _ticker_cache[ticker] = ""
        return ""
        
    try:
        fstype = data["QUOTES"][ticker]["SECURITY_TYPE"]
    except:
        _ticker_cache[ticker] = ""
        return ""
        
    if fstype == "Equity":
        fitype = ""
        try:
            fitype = data["QUOTES"][ticker]["ISSUE_DESCRIPTION"]
        except:
            pass

        if fitype == "ETF":
            stype = "ETF"
        else:
            stype = "Stock"
    elif fstype == "MutualFund":
        stype = "Fund"
    else:
        stype = fstype
        
    _ticker_cache[ticker] = stype

    return stype

def ticker_name(ticker):
    """
    Description:
    Get security name

    Parameters:
    ticker - The security ticker.

    Returns:
    The ticker name, "" (in case the ticker can't be resolved)
    """

    if ticker in _name_cache:
        return(_name_cache[ticker])

    # Should not contain spaces
    if " " in ticker:
        return None

    # The Fidelity URL 
    url = "https://fastquote.fidelity.com/service/quote/json?productid=embeddedquotes&symbols="
    
    # Get the page
    r = web.get_web_page(url + ticker, False)
    #print(r[1:-1])
    
    # Strip the '(' at beginning and the ')' at end
    data = json.loads(r[1:-1])
    #print(data)
    
    if (data["STATUS"]["ERROR_CODE"] != "0"):
        _name_cache[ticker] = ""
        return ""
        
    try:
        fname = data["QUOTES"][ticker]["NAME"]
        fstype = data["QUOTES"][ticker]["SECURITY_TYPE"]
    except:
        _name_cache[ticker] = ""
        return ""
      
    if fstype != "Index":
        name = titlecase.titlecase(fname)
    else:
        name = fname
        
    if name is not None:
        _name_cache[ticker] = name

    return name


def _parse_ticker_type_f(args):
    type = ticker_type(args.ticker)

    if type != "":
        print(type)

def _parse_ticker_name_f(args):
    type = ticker_name(args.ticker)

    if type != "":
        print(type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Fidelity data.')

    # Subparsers
    subparsers = parser.add_subparsers(help='Sub-command help')

    parser_ticker_type = subparsers.add_parser('ticker-type', help='Get ticker type (cef, etf, index, fund, stock, cash)')
    parser_ticker_type.add_argument('ticker', help='Ticker')
    parser_ticker_type.set_defaults(func=_parse_ticker_type_f)

    parser_ticker_name = subparsers.add_parser('ticker-name', help='Get name (all)')
    parser_ticker_name.add_argument('ticker', help='Ticker')
    parser_ticker_name.set_defaults(func=_parse_ticker_name_f)

    args = parser.parse_args()
    args.func(args)
