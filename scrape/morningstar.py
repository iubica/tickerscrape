#!/usr/bin/env python

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import web
import argparse
import unidecode

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
    A string with value "Cash", "CEF", "ETF", "Index", "Mutual Fund", "Other", "Stock"
    (or "" in case the ticker is neither)
    """

    # Special case for cash
    if ticker.lower() == "cash":
        return "Cash"

    if ticker.lower() == "other":
        return "Other"

    if ticker not in _ticker_cache:
        # The Morningstar URL for funds
        url = "http://quote.morningstar.com/Quote/Quote.aspx?ticker="
    
        # Get the page
        r = requests.get(url + ticker, allow_redirects = False)
   
        # Enable to inspect headers
        #print(r)
        #print(r.headers)

        if r.status_code == 302:
            if "/stock/" in r.headers['Location']:
                _ticker_cache[ticker] = "Stock"
            elif "/fund/" in r.headers['Location']:
                _ticker_cache[ticker] = "Mutual Fund"
            elif "//etfs." in r.headers['Location']:
                _ticker_cache[ticker] = "ETF"
                return("ETF")
            elif "//cef." in r.headers['Location']:
                _ticker_cache[ticker] = "CEF"
            elif "/indexquote/" in r.headers['Location']:
                _ticker_cache[ticker] = "Index"
            
    if ticker in _ticker_cache:
        return(_ticker_cache[ticker])
    
    return ""

def ticker_name(ticker):
    """
    Description:
    Get ETF, fund or stock name

    Parameters:
    ticker - The etf, fund, stock ticker.

    Returns:
    The ticker name, "" (in case the ticker can't be resolved)
    """

    if ticker in _name_cache:
        return(_name_cache[ticker])

    # Should not contain spaces
    if " " in ticker:
        return None

    # Ticker check    
    tt = ticker_type(ticker)

    name = None
    if tt == "CEF" or tt == "ETF" or tt == "Index" or tt == "Mutual Fund":
        name = fund_name(ticker)
    
    if tt == "Stock":
        name = stock_name(ticker)
    
    if name is not None:
        _name_cache[ticker] = name

    return name


def fund_name(ticker):
    """
    Description:
    Get a fund or ETF name

    Parameters:
    ticker - The etf, fund ticker.

    Returns:
    The ticker name, "" (in case the ticker is neither an ETF, nor fund)
    """

    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "CEF" and tt != "ETF" and tt != "Index" and tt != "Mutual Fund":
        return None    

    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t=" + ticker
    
    # Get the page
    web_page = web.get_web_page(url, False)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    ticker_name = soup.find("div", class_="r_title").find_next("h1").getText()

    return ticker_name.encode("ascii", "ignore").decode("utf-8")


def stock_name(ticker):
    """
    Description:
    Get a stock name

    Parameters:
    ticker - The etf, fund ticker.

    Returns:
    The ticker name, "" (in case the ticker is neither an ETF, nor fund)
    """

    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Stock":
        return None    

    # The Morningstar URL
    url = "http://performance.morningstar.com/stock/performance-return.action?t=" + ticker
    
    # Get the page
    web_page = web.get_web_page(url, False)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    ticker_name = soup.find("div", class_="r_title").find_next("h1").getText()

    return ticker_name.encode("ascii", "ignore").decode("utf-8")


def performance_history(ticker):
    """
    Description:
    Get ETF, fund or stock performance history. For ETFs and stocks, this is 
    based on price. For funds, this is based on NAV (net asset value).
    
    Parameters:
    ticker - The etf, fund or stock ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py pfh ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt == "CEF":
        df = etf_performance_history(ticker)
        df.drop(df.index[[1, 2, 3, 4, 5, 6, 7]], inplace=True)
        return df

    if tt == "ETF":
        df = etf_performance_history(ticker)
        df.drop(df.index[[1, 2, 3, 4, 5, 6]], inplace=True)
        return df

    if tt == "Index":
        df = index_performance_history(ticker)
        return df

    if tt == "Mutual Fund":
        df = etf_performance_history(ticker)
        df.drop(df.index[[0, 2, 3, 4, 5, 6, 7]], inplace=True)
        return df

    if tt == "Stock":
        df = stock_performance_history(ticker)
        df.drop(df.index[[1, 2, 3, 4]], inplace=True)
        return df

    return None

def nav_performance_history(ticker):
    """
    Description:
    Get ETF, fund or stock NAV (net asset value) performance history. For ETFs
    and funds, this is based on NAV. For stocks, this is based on price.
    
    Parameters:
    ticker - The etf, fund or stock ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py nav-pfh ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt == "ETF":
        df = etf_performance_history(ticker)
        df.drop(df.index[[0, 2, 3, 4, 5, 6]], inplace=True)
        return df

    if tt == "Mutual Fund":
        df = etf_performance_history(ticker)
        df.drop(df.index[[0, 2, 3, 4, 5, 6, 7]], inplace=True)
        return df

    if tt == "Index":
        df = index_performance_history(ticker)
        return df

    if tt == "Stock":
        df = stock_performance_history(ticker)
        df.drop(df.index[[1, 2, 3, 4]], inplace=True)
        return df

    return None

def etf_performance_history(ticker):
    """
    Description:
    Get etf or fund performance history. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py etf-pfh ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "CEF" and tt != "ETF" and tt != "Mutual Fund":
        return None    

    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/perform/Performance/cef/performance-history.action?&ops=clear&y=10&ndec=2&align=d&t="
    
    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    df.fillna(value="", inplace=True)

    return df

def fund_performance_history(ticker):
    """
    Description:
    Get etf or fund performance history. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py fund-pfh ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Mutual Fund" and tt != "ETF":
        return None    

    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/performance-history-1.action?&ops=clear&ndec=2&align=d&t="
    
    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    # For python 3 and later...
    if (sys.version_info[0] >= 3):
        # Fix the unprintable unicode characters
        df.index.name = unidecode.unidecode(df.index.name)
        df1 = df.applymap(lambda x: unidecode.unidecode(str(x)))
        df = df1

    return df


def index_performance_history(ticker):
    """
    Description:
    Get index performance history. 
    
    Parameters:
    ticker - The index ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py index-pfh ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "CEF" and tt != "ETF" and tt != "Index" and tt != "Mutual Fund" and tt != "Stock":
        return None    

    # The Morningstar URL for indexes
    url = "http://performance.morningstar.com/perform/Performance/index-c/performance-history-1.action?&ops=clear&y=10&ndec=2&align=d&t="
    
    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    df.fillna(value="", inplace=True)

    return df

def stock_performance_history(ticker):
    """
    Description:
    Get stock performance history. Does not work for stocks.
    
    Parameters:
    ticker - The stock ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py stock-pfh ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    
    if tt != "Stock":
        return None    

    # The Morningstar URL
    url = "http://performance.morningstar.com/perform/Performance/stock/performance-history-1.action?&ops=clear&y=10&ndec=2&align=d&t="

    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    df.fillna(value="", inplace=True)

    return df

def fund_performance_history2(ticker):
    """
    Description:
    Get fund performance history.
    
    Parameters:
    ticker - The fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py pfh2 ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Mutual Fund":
        return None    

    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 12)

    # Trim last three rows
    df.drop(df.tail(3).index,inplace=True)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df

def trailing_total_returns(ticker):
    """
    Description:
    Get trailing total returns (price for etfs, stocks, NAV for funds)
    
    Parameters:
    ticker - The ticker.

    Returs: 
    DataFrame with the trailing total returns.
    Run 'morningstar.py ttl ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt == "CEF":
        df = etf_trailing_total_returns(ticker)
        df.drop(df.index[[1, 2, 3, 4, 5]], inplace=True)
        return df

    if tt == "ETF":
        df = etf_trailing_total_returns(ticker)
        df.drop(df.index[[1, 2, 3, 4]], inplace=True)
        return df

    if tt == "Index":
        df = index_trailing_total_returns(ticker)
        return df

    if tt == "Mutual Fund":
        df = etf_trailing_total_returns(ticker)
        df.drop(df.index[[0, 2, 3, 4, 5]], inplace=True)
        return df

    if tt == "Stock":
        df = etf_trailing_total_returns(ticker)
        df.drop(df.index[[1, 2, 3]], inplace=True)
        return df

    return None

def nav_trailing_total_returns(ticker):
    """
    Description:
    Get trailing total returns (NAV for etfs, funds, and price for stocks)
    
    Parameters:
    ticker - The ticker.

    Returs: 
    DataFrame with the trailing total returns.
    Run 'morningstar.py nav-ttl ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt == "CEF":
        df = etf_trailing_total_returns(ticker)
        df.drop(df.index[[0, 2, 3, 4, 5]], inplace=True)
        return df

    if tt == "ETF":
        df = etf_trailing_total_returns(ticker)
        df.drop(df.index[[0, 2, 3, 4]], inplace=True)
        return df

    if tt == "Index":
        df = index_trailing_total_returns(ticker)
        return df

    if tt == "Mutual Fund":
        df = etf_trailing_total_returns(ticker)
        df.drop(df.index[[0, 2, 3, 4, 5]], inplace=True)
        return df

    if tt == "Stock":
        df = etf_trailing_total_returns(ticker)
        df.drop(df.index[[1, 2, 3]], inplace=True)
        return df

    return None

def etf_trailing_total_returns(ticker):
    """
    Description:
    Get trailing total returns. 
    
    Parameters:
    ticker - The ticker.

    Returs: 
    DataFrame with the trailing total returns.
    Run 'morningstar.py etf-ttl ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "CEF" and tt != "ETF" and tt != "Index" and tt != "Mutual Fund" and tt != "Stock":
        return None    

    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/cef/trailing-total-returns.action?ops=clear&ndec=2&align=d&t="    

    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    df.fillna(value="", inplace=True)

    return df

def fund_trailing_total_returns(ticker):
    """
    Description:
    Get trailing total returns. 
    
    Parameters:
    ticker - The ticker.

    Returs: 
    DataFrame with the trailing total returns.
    Run 'morningstar.py ttl ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "ETF" and tt != "Mutual Fund" and tt != "Stock":
        return None    

    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/trailing-total-returns.action?t="    

    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    # For python 3 and later...
    if (sys.version_info[0] >= 3):
        # Fix the unprintable unicode characters
        df.index.name = unidecode.unidecode(df.index.name)
        df1 = df.applymap(lambda x: unidecode.unidecode(x))
        df = df1

    return df

def fund_trailing_total_returns2(ticker):
    """
    Description:
    Get trailing total returns. Only works for funds.

    Parameters:
    ticker - The fund ticker

    Returns:

    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Mutual Fund":
        return None    

    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 14)
    df.iloc[0, 1] = "Total Return %"
    df.iloc[0, 2] = unidecode.unidecode(df.iloc[0, 2]).replace("\r", "").replace("\n", "")
    df.iloc[0, 3] = unidecode.unidecode(df.iloc[0, 3]).replace("\r", "").replace("\n", "")
    df.iloc[0, 4] = "% Rank in Cat"

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def index_trailing_total_returns(ticker):
    """
    Description:
    Get trailing total returns. 
    
    Parameters:
    ticker - The ticker.

    Returs: 
    DataFrame with the trailing total returns.
    Run 'morningstar.py index-ttl ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "CEF" and tt != "ETF" and tt != "Index" and tt != "Mutual Fund" and tt != "Stock":
        return None    

    # The Morningstar URL
    url = "http://performance.morningstar.com/perform/Performance/index-c/trailing-total-returns.action?ops=clear&ndec=2&align=d&t="    

    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    df.fillna(value="", inplace=True)

    return df

def historical_quarterly_returns(ticker, years = 5, frequency = "q"):
    """
    Description:
    Get historical quarterly returns.

    Parameters:
    ticker - The etf, fund or stock ticker.
    years - The number of years. Default: 5.
    frequency - "q" for quarterly, "m" for monthly. Default: "q"
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt == "CEF":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[1]], axis=1, inplace=True)
        return df

    if tt == "ETF":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[1]], axis=1, inplace=True)
        return df

    if tt == "Index":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[1]], axis=1, inplace=True)
        return df
        
    if tt == "Mutual Fund":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[0]], axis=1, inplace=True)
        return df

    if tt == "Stock":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[1]], axis=1, inplace=True)
        return df

    return None

def nav_historical_quarterly_returns(ticker, years = 5, frequency = "q"):
    """
    Description:
    Get historical NAV quarterly returns.

    Parameters:
    ticker - The etf, fund or stock ticker.
    years - The number of years. Default: 5.
    frequency - "q" for quarterly, "m" for monthly. Default: "q"
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt == "CEF":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[0]], axis=1, inplace=True)
        return df

    if tt == "ETF":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[0]], axis=1, inplace=True)
        return df

    if tt == "Index":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[1]], axis=1, inplace=True)
        return df
        
    if tt == "Mutual Fund":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[0]], axis=1, inplace=True)
        return df

    if tt == "Stock":
        df = cef_historical_quarterly_returns(ticker, years, frequency)
        df.drop(df.columns[[1]], axis=1, inplace=True)
        return df

    return None

def cef_historical_quarterly_returns(ticker, years = 5, frequency = "q"):
    """
    Description:
    Get historical quarterly returns for cefs. 

    Parameters:
    ticker - the ticker

    Returns:

    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "CEF" and tt != "ETF" and tt != "Index" and tt != "Mutual Fund" and tt != "Stock":
        return None

    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/perform/Performance/cef/historical-returns.action?&ops=clear&y=%s&ndec=2&freq=%s&t=" % (years, frequency)
    
    df = web.get_web_page_table(url + ticker, False, 0)
    df.fillna(value="", inplace=True)

    # Promote 1st row and column as labels
    df1 = df.drop(df.columns[[3, 4, 5, 6, 7]], axis=1)
    df = web.dataframe_promote_1st_row_and_column_as_labels(df1)

    return df 

def fund_historical_quarterly_returns(ticker, years = 5, frequency = "q"):
    """
    Description:
    Get historical quarterly returns.

    Parameters:
    ticker - The etf, fund or stock ticker.
    years - The number of years. Default: 5.
    frequency - "q" for quarterly, "m" for monthly. Default: "q"
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "CEF" and tt != "ETF" and tt != "Index" and tt != "Mutual Fund" and tt != "Stock":
        return None    

    if frequency != "q" and frequency != "m":
        return None

    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/historical-returns.action?&ops=clear&y=%s&freq=%s&t=" % (years, frequency)
    
    df = web.get_web_page_table(url + ticker, False, 0)

    df.fillna(value="", inplace=True)
    df1 = df.drop(df.columns[[2, 3, 4, 5, 6, 7]], axis=1)
    df = df1

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def fund2_historical_quarterly_returns(ticker):
    """
    Description:
    Get historical quarterly returns for etfs and funds. 
    Does not work with stocks.

    Parameters:
    ticker - the etf or fund ticker

    Returns:

    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Mutual Fund" and tt != "ETF":
        return None    

    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 16)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def cef_quote(ticker):
    """
    Description:
    Get the cef net asset value, and other related data.

    Parameters:
    ticker - The fund ticker.

    Returns:

    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "CEF":
        return None    

    # The Morningstar URL for etfs
    url = "http://cef.morningstar.com/cefq/cef-header?&t=" + ticker
    
    # Get the page
    web_page = web.get_web_page(url, False)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    df = pd.DataFrame(columns = range(1), 
                      index = range(16))
    
    # Set the index
    df['new_index'] = None
    df['new_index'][0] = "Last Price"
    df['new_index'][1] = "Day Change"
    df['new_index'][2] = "Day Change %"
    df['new_index'][3] = "As Of"
    df['new_index'][4] = "Last Closing Price"
    df['new_index'][5] = "Day Range"
    df['new_index'][6] = "52-WK Range"
    df['new_index'][7] = "1-Year Z-Statistic"
    df['new_index'][8] = "Market Value"
    df['new_index'][9] = "Total Leverage Ratio"
    df['new_index'][10] = "Last Actual NAV"
    df['new_index'][11] = "Last Actual NAV Date"
    df['new_index'][12] = "Last Actual Disc/Premium"
    df['new_index'][13] = "6-Month Avg Disc/Prem"
    df['new_index'][14] = "3-Year Avg Disc/Prem"
    df['new_index'][15] = "Total Dist. Rate (Share Price)"

    # Promote the 'new_index' column as the new index
    df2 = df.set_index('new_index')
    df = df2

    # Clear the index name
    df.index.name = ""

    # Set the ticker name as column label
    df.columns = [ticker.upper()]

    df.iloc[0, 0] = soup.find("div", {"id": "lastPrice"}).getText().strip()
    df.iloc[1, 0] = soup.find("span", {"id": "price-daychange-value"}).getText().strip()
    df.iloc[2, 0] = soup.find("span", {"id": "price-daychange-per"}).getText().strip()
    df.iloc[3, 0] = soup.find("span", {"id" : "last-date"}).getText().strip()
    df.iloc[4, 0] = soup.find("span", {"id" : "last-closing-price"}).getText().strip()
    df.iloc[5, 0] = soup.find("td", {"id" : "day-range"}).getText().strip()
    df.iloc[6, 0] = soup.find("td", {"id" : "fiftytwo-range"}).getText().strip()
    df.iloc[7, 0] = soup.findAll("td")[3].getText().strip()
    df.iloc[8, 0] = soup.findAll("td")[4].getText().strip()
    df.iloc[9, 0] = soup.findAll("td")[5].getText().strip()
    df.iloc[10, 0] = soup.find("td", {"id" : "last-act-nav"}).getText().strip()
    df.iloc[11, 0] = soup.findAll("td")[8].getText().strip()
    df.iloc[12, 0] = soup.find("td", {"id" : "last-discount"}).getText().strip()
    df.iloc[13, 0] = soup.findAll("td")[10].getText().strip()
    df.iloc[14, 0] = soup.findAll("td")[11].getText().strip()
    df.iloc[15, 0] = soup.findAll("td")[12].getText().strip()

    return df

def etf_quote(ticker):
    """
    Description:
    Get the fund net asset value, and other related data.

    Parameters:
    ticker - The fund ticker.

    Returns:

    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "ETF":
        return None    

    # The Morningstar URL for etfs
    url = "http://etfs.morningstar.com/quote-banner?&t=" + ticker
    
    # Get the page
    web_page = web.get_web_page(url, False)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    df = pd.DataFrame(columns = range(1), 
                      index = range(21))
    
    # Set the index
    df['new_index'] = None
    df['new_index'][0] = "Last Price"
    df['new_index'][1] = "Day Change"
    df['new_index'][2] = "Day Change %"
    df['new_index'][3] = "As Of"
    df['new_index'][4] = "Intraday Indicative Value"
    df['new_index'][5] = "IIV Change"
    df['new_index'][6] = "IIV Change %"
    df['new_index'][7] = "IIV As Of"
    df['new_index'][8] = "NAV"
    df['new_index'][9] = "Open Price"
    df['new_index'][10] = "Day Range"
    df['new_index'][11] = "52-Week Range"
    df['new_index'][12] = "12-Mo. Yield"
    df['new_index'][13] = "Total Assets"
    df['new_index'][14] = "Expenses"
    df['new_index'][15] = "Prem/Discount"
    df['new_index'][16] = "Volume"
    df['new_index'][17] = "Avg Vol."
    df['new_index'][18] = "Sec. Yield %"
    df['new_index'][19] = "Bid/Ask/Spread"
    df['new_index'][20] = "Category"

    # Promote the 'new_index' column as the new index
    df2 = df.set_index('new_index')
    df = df2

    # Clear the index name
    df.index.name = ""

    # Set the ticker name as column label
    df.columns = [ticker.upper()]

    df.iloc[0, 0] = soup.find("div", {"id": "lastPrice"}).getText().strip()
    df.iloc[1, 0] = soup.find("span", {"id": "day_change"}).getText().strip()
    df.iloc[2, 0] = soup.find("span", {"id": "day_changeP"}).getText().strip()
    df.iloc[3, 0] = soup.find("span", {"id" : "isDate"}).getText().strip() + " " + soup.find("span", {"id" : "Timezone"}).getText().strip()
    df.iloc[4, 0] = soup.find("div", {"id" : "IIV_lastPrice"}).getText().strip()
    df.iloc[5, 0] = soup.find("span", {"id" : "IIV_day_change"}).getText().strip()
    df.iloc[6, 0] = soup.find("span", {"id" : "IIV_day_changeP"}).getText().strip()
    df.iloc[7, 0] = soup.find("span", {"id" : "isDateIV"}).getText().strip() + " " + soup.find("span", {"id" : "Timezone"}).getText().strip()
    df.iloc[8, 0] = soup.find("span", {"id": "NAV"}).getText().strip()
    df.iloc[9, 0] = soup.find("span", {"id": "OpenPrice"}).getText().strip()
    df.iloc[10, 0] = soup.find("span", {"id": "dayRange"}).getText().strip()
    df.iloc[11, 0] = soup.find("span", {"id": "week52Range"}).getText().strip()
    df.iloc[12, 0] = soup.find("span", {"id": "Yield"}).getText().strip()
    df.iloc[13, 0] = soup.find("span", {"id": "totalAssets"}).getText().strip()
    df.iloc[14, 0] = soup.find("span", {"id": "Expenses"}).getText().strip()
    df.iloc[15, 0] = soup.find("span", {"id": "premDiscount"}).getText().strip()
    df.iloc[16, 0] = soup.find("span", {"id": "volume"}).getText().strip()

    volume = soup.find("span", {"id": "volume"})
    df.iloc[17, 0] = volume.parent.find_next_sibling("td", class_="gr_table_colm2b").find("span").getText().strip()

    df.iloc[18, 0] = soup.find("span", {"id": "Leverage"}).getText().strip()
    df.iloc[19, 0] = soup.find("span", {"id": "bid"}).getText().strip() + "/" + soup.find("span", {"id": "ask"}).getText().strip() + "/" + soup.find("span", {"id": "BidAskSpread"}).getText().strip() + "%"
    df.iloc[20, 0] = soup.find("span", {"id": "MorningstarCategory"}).getText().strip()

    # For python 3 and later...
    if (sys.version_info[0] >= 3):
        # Fix the unprintable unicode characters
        df1 = df.applymap(lambda x: unidecode.unidecode(x))
        df = df1

    return df

def fund_quote(ticker):
    """
    Description:
    Get the fund net asset value, and other related data.

    Parameters:
    ticker - The fund ticker.

    Returns:

    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Mutual Fund" and tt != "ETF":
        return None    

    # The Morningstar URL for funds
    url = "http://quotes.morningstar.com/fund/c-header?&t=" + ticker
    
    # Get the page
    web_page = web.get_web_page(url, False)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    df = pd.DataFrame(columns = range(1), 
                      index = range(15))
    
    # Set the index
    df['new_index'] = None
    df['new_index'][0] = soup.find("h3", {"gkey": "NAV"}).getText().strip()
    df['new_index'][1] = soup.find("h3", {"gkey": "NavChange"}).getText().strip() + " %"
    df['new_index'][2] = soup.find("span", {"gkey": "AsOf"}).getText().strip()
    df['new_index'][3] = soup.find("span", {"gkey": "OneDayReturnAsOf"}).getText().strip()
    df['new_index'][4] = soup.find("h3", {"gkey": "ttmYield"}).getText().strip()
    df['new_index'][5] = soup.find("h3", {"gkey": "Load"}).getText().strip()
    df['new_index'][6] = soup.find("h3", {"gkey": "TotalAssets"}).getText().strip()
    df['new_index'][7] = soup.find("a", {"gkey": "ExpenseRatio"}).getText().strip()
    df['new_index'][8] = soup.find("a", {"gkey": "FeeLevel"}).getText().strip()
    df['new_index'][9] = soup.find("h3", {"gkey": "Turnover"}).getText().strip()
    df['new_index'][10] = soup.find("h3", {"gkey": "Status"}).getText().strip()
    df['new_index'][11] = soup.find("h3", {"gkey": "MinInvestment"}).getText().strip()
    df['new_index'][12] = soup.find("h3", {"gkey": "Yield"}).getText().strip()
    df['new_index'][13] = soup.find("h3", {"gkey": "MorningstarCategory"}).getText().strip()
    df['new_index'][14] = soup.find("h3", {"gkey": "InvestmentStyle"}).getText().strip()

    # Promote the 'new_index' column as the new index
    df2 = df.set_index('new_index')
    df = df2

    # Clear the index name
    df.index.name = ""

    # Set the ticker name as column label
    df.columns = [ticker.upper()]

    df.iloc[0, 0] = soup.find("span", {"vkey": "NAV"}).getText().strip()
    df.iloc[1, 0] = soup.find("div", {"vkey": "DayChange"}).getText().strip()
    df.iloc[2, 0] = soup.find("span", {"id" : "asOfDate", "vkey": "LastDate"}).getText().strip()
    df.iloc[3, 0] = soup.find("span", {"id" : "oneDayReturnAsOfDate", "vkey": "LastDate"}).getText().strip()
    df.iloc[4, 0] = soup.find("span", {"vkey": "ttmYield"}).getText().strip()
    df.iloc[5, 0] = soup.find("span", {"vkey": "Load"}).getText().strip()
    df.iloc[6, 0] = soup.find("span", {"vkey": "TotalAssets"}).getText().strip()
    df.iloc[7, 0] = soup.find("span", {"vkey": "ExpenseRatio"}).getText().strip()
    df.iloc[8, 0] = soup.find("span", {"vkey": "FeeLevel"}).getText().strip()
    df.iloc[9, 0] = soup.find("span", {"vkey": "Turnover"}).getText().strip()
    df.iloc[10, 0] = soup.find("span", {"vkey": "Status"}).getText().strip()
    df.iloc[11, 0] = soup.find("span", {"vkey": "MinInvestment"}).getText().strip()
    df.iloc[12, 0] = soup.find("span", {"vkey": "Yield"}).getText().strip()
    df.iloc[13, 0] = soup.find("span", {"vkey": "MorningstarCategory"}).getText().strip()
    df.iloc[14, 0] = soup.find("span", {"vkey": "InvestmentStyle"}).getText().strip()

    # For python 3 and later...
    if (sys.version_info[0] >= 3):
        # Fix the unprintable unicode characters
        df1 = df.applymap(lambda x: unidecode.unidecode(x))
        df = df1

    return df

def stock_quote(ticker):
    """
    Description:
    Get the etf or stock quote, and other related data.

    Parameters:
    ticker - The etf or stock ticker.

    Returns:

    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "ETF" and tt != "Stock":
        return None    

    # The Morningstar URL for funds
    url = "http://quotes.morningstar.com/stock/c-header?&t=" + ticker
    
    # Get the page
    web_page = web.get_web_page(url, False)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    df = pd.DataFrame(columns = range(1), 
                      index = range(18))
    
    # Set the index
    df['new_index'] = None
    df['new_index'][0] = soup.find("h3", {"gkey": "LastPrice"}).getText().strip()
    df['new_index'][1] = soup.find("h3", {"gkey": "DayChange"}).getText().strip()
    df['new_index'][2] = "Day Change %"
    df['new_index'][3] = "After Hours"
    df['new_index'][4] = "After Hours Change"
    df['new_index'][5] = "After Hours Change %"
    df['new_index'][6] = soup.find("span", {"gkey": "AsOf"}).getText().strip()
    df['new_index'][7] = soup.find("h3", {"gkey": "OpenPrice"}).getText().strip()
    df['new_index'][8] = soup.find("h3", {"gkey": "DayRange"}).getText().strip()
    df['new_index'][9] = soup.find("h3", {"gkey": "_52Week"}).getText().strip()
    df['new_index'][10] = soup.find("h3", {"gkey": "ProjectedYield"}).getText().strip()
    df['new_index'][11] = soup.find("h3", {"gkey": "MarketCap"}).getText().strip()
    df['new_index'][12] = soup.find("h3", {"gkey": "Volume"}).getText().strip()
    df['new_index'][13] = soup.find("h3", {"gkey": "AverageVolume"}).getText().strip()
    df['new_index'][14] = soup.find("span", {"gkey": "PE"}).getText().strip()
    df['new_index'][15] = soup.find("h3", {"gkey": "PB"}).getText().strip()
    df['new_index'][16] = soup.find("h3", {"gkey": "PS"}).getText().strip()
    df['new_index'][17] = soup.find("h3", {"gkey": "PC"}).getText().strip()

    # Promote the 'new_index' column as the new index
    df2 = df.set_index('new_index')
    df = df2

    # Clear the index name
    df.index.name = ""

    # Set the ticker name as column label
    df.columns = [ticker.upper()]

    df.iloc[0, 0] = soup.find("div", {"vkey": "LastPrice"}).getText().strip()
    df.iloc[1, 0] = soup.find("div", {"vkey": "DayChange"}).getText().split("|")[0].strip()
    df.iloc[2, 0] = soup.find("div", {"vkey": "DayChange"}).getText().split("|")[1].strip()

    afth = soup.find("span", {"id": "after-hours"})
    if afth:
        df.iloc[3, 0] = afth.getText().strip()
    else:
        df.iloc[3, 0] = ""    

    afth = soup.find("span", {"id": "after-daychange-value"})
    if afth:
        df.iloc[4, 0] = afth.getText().strip()
    else:
        df.iloc[4, 0] = ""    

    afth = soup.find("span", {"id": "after-daychange-per"})
    if afth:
        df.iloc[5, 0] = afth.getText().strip()
    else:
        df.iloc[5, 0] = ""    

    df.iloc[6, 0] = soup.find("span", {"id": "asOfDate"}).getText().strip() + " " + soup.find("span", {"id": "timezone"}).getText().strip()
    df.iloc[7, 0] = soup.find("span", {"vkey": "OpenPrice"}).getText().strip()
    df.iloc[8, 0] = soup.find("span", {"vkey": "DayRange"}).getText().strip()
    df.iloc[9, 0] = soup.find("span", {"vkey": "_52Week"}).getText().strip()
    df.iloc[10, 0] = soup.find("span", {"vkey": "ProjectedYield"}).getText().strip()
    df.iloc[11, 0] = soup.find("span", {"id": "MarketCap"}).getText().strip()
    df.iloc[12, 0] = soup.find("span", {"vkey": "Volume"}).getText().strip()
    df.iloc[13, 0] = soup.find("span", {"vkey": "AverageVolume"}).getText().strip()
    df.iloc[14, 0] = soup.find("span", {"vkey": "PE"}).getText().strip()
    df.iloc[15, 0] = soup.find("span", {"vkey": "PB"}).getText().strip()
    df.iloc[16, 0] = soup.find("span", {"vkey": "PS"}).getText().strip()
    df.iloc[17, 0] = soup.find("span", {"vkey": "PC"}).getText().strip()

    # For python 3 and later...
    if (sys.version_info[0] >= 3):
        # Fix the unprintable unicode characters
        df1 = df.applymap(lambda x: unidecode.unidecode(x))
        df = df1

    return df

def fund_asset_allocation(ticker):
    """
    Description:
    Get etf or fund asset allocation. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py aas ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Mutual Fund" and tt != "ETF":
        return None    

    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 1)

    # Create new dataframe from rows 0, 3, 5, 7, 9, 11
    df1 = pd.DataFrame(columns = range(7), 
                       index = range(6))

    df1.iloc[0] = df.iloc[0]
    df1.iloc[1] = df.iloc[3]
    df1.iloc[2] = df.iloc[5]
    df1.iloc[3] = df.iloc[7]
    df1.iloc[4] = df.iloc[9]
    df1.iloc[5] = df.iloc[11]

    # Special handling of two cells
    df1.iloc[0, 0] = df.iloc[1, 0]
    df1.iloc[0, 5] = "Benchmark" 

    df = df1

    # For python 3 and later...
    if (sys.version_info[0] >= 3):
        # Fix the unprintable unicode characters
        df1 = df.applymap(lambda x: unidecode.unidecode(str(x)))
        df = df1

    # Promote 1st row and column as labels
    df1 = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df = df1

    return df

def fund_market_capitalization(ticker):
    """
    Description:
    Get etf or fund market capitalization. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py aas ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Mutual Fund" and tt != "ETF":
        return None    

    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 2)

    # Create new dataframe from rows 0, 2, 4, 6, 8, 10
    df1 = pd.DataFrame(columns = range(4), 
                       index = range(6))

    df1.iloc[0] = df.iloc[0]
    df1.iloc[1] = df.iloc[2]
    df1.iloc[2] = df.iloc[4]
    df1.iloc[3] = df.iloc[6]
    df1.iloc[4] = df.iloc[8]
    df1.iloc[5] = df.iloc[10]

    df = df1

    # Promote 1st row and column as labels
    df1 = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df = df1

    return df

def fund_sector_weightings(ticker):
    """
    Description:
    Get etf or fund sector weightings. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py aas ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Mutual Fund" and tt != "ETF":
        return None    

    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 5)

    df.fillna(value="", inplace=True)

    # Create new dataframe from rows 0, 2, 4, 6, 8, 10
    df1 = pd.DataFrame(columns = range(8), 
                       index = range(12))

    df1.iloc[0] = df.iloc[0]
    df1.iloc[1] = df.iloc[4]
    df1.iloc[2] = df.iloc[6]
    df1.iloc[3] = df.iloc[8]
    df1.iloc[4] = df.iloc[10]
    df1.iloc[5] = df.iloc[15]
    df1.iloc[6] = df.iloc[17]
    df1.iloc[7] = df.iloc[19]
    df1.iloc[8] = df.iloc[21]
    df1.iloc[9] = df.iloc[26]
    df1.iloc[10] = df.iloc[28]
    df1.iloc[11] = df.iloc[30]

    df1.iloc[0, 0] = "Type"
    df1.iloc[0, 1] = "Category"
    df1.iloc[1, 1] = "Cyclical"
    df1.iloc[2, 1] = "Cyclical"
    df1.iloc[3, 1] = "Cyclical"
    df1.iloc[4, 1] = "Cyclical"
    df1.iloc[5, 1] = "Sensitive"
    df1.iloc[6, 1] = "Sensitive"
    df1.iloc[7, 1] = "Sensitive"
    df1.iloc[8, 1] = "Sensitive"
    df1.iloc[9, 1] = "Defensive"
    df1.iloc[10, 1] = "Defensive"
    df1.iloc[11, 1] = "Defensive"

    # Remove column 5
    del df1[5]

    df = df1

    # Promote 1st row and column as labels
    df1 = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df = df1

    return df

def fund_market_regions(ticker):
    """
    Description:
    Get etf or fund market regions. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py aas ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Mutual Fund" and tt != "ETF":
        return None    

    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 6)

    df.fillna(value="", inplace=True)

    # Create new dataframe from rows 0, 2, 4, 6, 8, 10
    df1 = pd.DataFrame(columns = range(4), 
                       index = range(16))

    df1.iloc[0] = df.iloc[0]
    df1.iloc[1] = df.iloc[3]
    df1.iloc[2] = df.iloc[5]
    df1.iloc[3] = df.iloc[7]
    df1.iloc[4] = df.iloc[9]
    df1.iloc[5] = df.iloc[11]
    df1.iloc[6] = df.iloc[13]
    df1.iloc[7] = df.iloc[15]
    df1.iloc[8] = df.iloc[17]
    df1.iloc[9] = df.iloc[19]
    df1.iloc[10] = df.iloc[21]
    df1.iloc[11] = df.iloc[23]
    df1.iloc[12] = df.iloc[25]
    df1.iloc[13] = df.iloc[27]
    df1.iloc[14] = df.iloc[32]
    df1.iloc[15] = df.iloc[34]

    df = df1

    # For python 3 and later...
    if (sys.version_info[0] >= 3):
        # Fix the unprintable unicode characters
        df1 = df.applymap(lambda x: unidecode.unidecode(str(x)))
        df = df1

    # Promote 1st row and column as labels
    df1 = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df = df1

    return df

def stock_profile(ticker):
    """
    Description:
    Get stock profile.
    
    Parameters:
    ticker - The stock ticker.

    Returs: 
    DataFrame with the stock profile history. 
    Run 'morningstar.py stock-profile ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Stock":
        return None    

    # The Morningstar URL
    url = "http://quotes.morningstar.com/stockq/c-company-profile?&t="
    
    # Get the page
    web_page = web.get_web_page(url + ticker, False)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    df = pd.DataFrame(columns = range(1), 
                      index = range(6))
    
    # Set the index
    df['new_index'] = None
    df['new_index'][0] = "Sector"
    df['new_index'][1] = "Industry"
    df['new_index'][2] = "Stock Type"
    df['new_index'][3] = "Employees"
    df['new_index'][4] = "Fiscal Year Ends"
    df['new_index'][5] = "Stock Style"

    # Promote the 'new_index' column as the new index
    df2 = df.set_index('new_index')
    df = df2

    # Clear the index name
    df.index.name = ""

    # Set the ticker name as column label
    df.columns = [ticker.upper()]

    df.iloc[0, 0] = soup.find_all("div", {"class": "gr_colm1"})[0].find("span", {"class": "gr_text7"}).getText().strip()
    df.iloc[1, 0] = soup.find_all("div", {"class": "gr_colm1a"})[0].find("span", {"class": "gr_text7"}).getText().strip()
    df.iloc[2, 0] = soup.find_all("div", {"class": "gr_colm1a"})[1].find("span", {"class": "gr_text7"}).getText().strip()
    df.iloc[3, 0] = soup.find_all("div", {"class": "gr_colm1"})[1].find("span", {"class": "gr_text7"}).getText().strip()
    df.iloc[4, 0] = soup.find_all("div", {"class": "gr_colm1a"})[2].find("span", {"class": "gr_text7"}).getText().strip()
    df.iloc[5, 0] = soup.find_all("div", {"class": "gr_colm1a"})[3].find("span", {"class": "gr_text7"}).getText().strip()

    return df

def stock_competitors(ticker):
    """
    Description:
    Get stock competitors.
    
    Parameters:
    ticker - The stock ticker.

    Returs: 
    DataFrame with the stock competitors. 
    Run 'morningstar.py stock-competitors ticker' to see the result format.
    """
    # Ticker check    
    tt = ticker_type(ticker)
    if tt != "Stock":
        return None    

    # The Morningstar URL
    url = "http://quotes.morningstar.com/stockq/c-competitors?&t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 0)    

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df.rename(columns={ df.columns[3]: "TTM Sales $mil" }, inplace=True)
    df.drop(df.index[0], inplace=True)
    df.drop(df.columns[2], axis=1, inplace=True)

    return df

def _parse_ticker_type_f(args):
    type = ticker_type(args.ticker)

    if type != "":
        print(type)

def _parse_ticker_name_f(args):
    type = ticker_name(args.ticker)

    if type != "":
        print(type)

def _parse_fund_name_f(args):
    type = fund_name(args.ticker)

    if type != "":
        print(type)

def _parse_stock_name_f(args):
    type = stock_name(args.ticker)

    if type != "":
        print(type)

def _parse_pfh_f(args):
    df = performance_history(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_nav_pfh_f(args):
    df = nav_performance_history(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_etf_pfh_f(args):
    df = etf_performance_history(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_index_pfh_f(args):
    df = index_performance_history(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_fund_pfh_f(args):
    df = fund_performance_history(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_stock_pfh_f(args):
    df = stock_performance_history(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_pfh2_f(args):
    df = fund_performance_history2(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_ttl_f(args):
    df = trailing_total_returns(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_nav_ttl_f(args):
    df = nav_trailing_total_returns(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_etf_ttl_f(args):
    df = etf_trailing_total_returns(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_fund_ttl_f(args):
    df = fund_trailing_total_returns(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_ttl2_f(args):
    df = fund_trailing_total_returns2(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_index_ttl_f(args):
    df = index_trailing_total_returns(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_qtr_f(args):
    df = historical_quarterly_returns(args.ticker, args.years, args.frequency)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_nav_qtr_f(args):
    df = nav_historical_quarterly_returns(args.ticker, args.years, args.frequency)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_cef_qtr_f(args):
    df = cef_historical_quarterly_returns(args.ticker, args.years, args.frequency)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_fund_qtr_f(args):
    df = fund_historical_quarterly_returns(args.ticker, args.years, args.frequency)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_qtr2_f(args):
    df = fund2_historical_quarterly_returns(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_cef_quote(args):
    df = cef_quote(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_etf_quote(args):
    df = etf_quote(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_fund_quote(args):
    df = fund_quote(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_stock_quote(args):
    df = stock_quote(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_aal(args):
    df = fund_asset_allocation(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_mkc(args):
    df = fund_market_capitalization(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_sect(args):
    df = fund_sector_weightings(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_reg(args):
    df = fund_market_regions(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_stock_profile(args):
    df = stock_profile(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_stock_competitors(args):
    df = stock_competitors(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Morningstar data.')

    # Subparsers
    subparsers = parser.add_subparsers(help='Sub-command help')

    parser_ticker_type = subparsers.add_parser('ticker-type', help='Get ticker type (cef, etf, index, fund, stock, cash)')
    parser_ticker_type.add_argument('ticker', help='Ticker')
    parser_ticker_type.set_defaults(func=_parse_ticker_type_f)

    parser_ticker_name = subparsers.add_parser('ticker-name', help='Get name (all)')
    parser_ticker_name.add_argument('ticker', help='Ticker')
    parser_ticker_name.set_defaults(func=_parse_ticker_name_f)

    parser_fund_name = subparsers.add_parser('fund-name', help='Get name (cef, etf, index, fund)')
    parser_fund_name.add_argument('ticker', help='Ticker')
    parser_fund_name.set_defaults(func=_parse_fund_name_f)

    parser_stock_name = subparsers.add_parser('stock-name', help='Get name (stock)')
    parser_stock_name.add_argument('ticker', help='Ticker')
    parser_stock_name.set_defaults(func=_parse_stock_name_f)

    parser_pfh = subparsers.add_parser('pfh', help='Performace history (all)')
    parser_pfh.add_argument('ticker', help='Ticker')
    parser_pfh.set_defaults(func=_parse_pfh_f)

    parser_nav_pfh = subparsers.add_parser('nav-pfh', help='NAV performace history (etfs, funds, stocks)')
    parser_nav_pfh.add_argument('ticker', help='Ticker')
    parser_nav_pfh.set_defaults(func=_parse_nav_pfh_f)

    parser_etf_pfh = subparsers.add_parser('etf-pfh', help='Performace history (etfs, funds)')
    parser_etf_pfh.add_argument('ticker', help='Ticker')
    parser_etf_pfh.set_defaults(func=_parse_etf_pfh_f)

    parser_fund_pfh = subparsers.add_parser('fund-pfh', help='Performace history (funds)')
    parser_fund_pfh.add_argument('ticker', help='Ticker')
    parser_fund_pfh.set_defaults(func=_parse_fund_pfh_f)

    parser_index_pfh = subparsers.add_parser('index-pfh', help='Performace history (all)')
    parser_index_pfh.add_argument('ticker', help='Ticker')
    parser_index_pfh.set_defaults(func=_parse_index_pfh_f)

    parser_stock_pfh = subparsers.add_parser('stock-pfh', help='Performace history (stocks)')
    parser_stock_pfh.add_argument('ticker', help='Ticker')
    parser_stock_pfh.set_defaults(func=_parse_stock_pfh_f)

    parser_pfh2 = subparsers.add_parser('pfh2', help='Performace history 2 (funds)')
    parser_pfh2.add_argument('ticker', help='Ticker')
    parser_pfh2.set_defaults(func=_parse_pfh2_f)

    parser_ttl = subparsers.add_parser('ttl', help='Trailing total returns (all)')
    parser_ttl.add_argument('ticker', help='Ticker')
    parser_ttl.set_defaults(func=_parse_ttl_f)

    parser_etf_ttl = subparsers.add_parser('etf-ttl', help='Trailing total returns (all)')
    parser_etf_ttl.add_argument('ticker', help='Ticker')
    parser_etf_ttl.set_defaults(func=_parse_etf_ttl_f)

    parser_nav_ttl = subparsers.add_parser('nav-ttl', help='NAV trailing total returns (all)')
    parser_nav_ttl.add_argument('ticker', help='Ticker')
    parser_nav_ttl.set_defaults(func=_parse_nav_ttl_f)

    parser_fund_ttl = subparsers.add_parser('fund-ttl', help='Trailing total returns (etfs, funds, stocks)')
    parser_fund_ttl.add_argument('ticker', help='Ticker')
    parser_fund_ttl.set_defaults(func=_parse_fund_ttl_f)

    parser_index = subparsers.add_parser('index-ttl', help='Trailing total returns (indexes)')
    parser_index.add_argument('ticker', help='Ticker')
    parser_index.set_defaults(func=_parse_index_ttl_f)

    parser_ttl2 = subparsers.add_parser('ttl2', help='Trailing total returns 2 (funds)')
    parser_ttl2.add_argument('ticker', help='Ticker')
    parser_ttl2.set_defaults(func=_parse_ttl2_f)

    parser_qtr = subparsers.add_parser('qtr', help='Historical quarterly returns (all)')
    parser_qtr.add_argument('ticker', help='Ticker')
    parser_qtr.add_argument('-y', '--years', type=int, default=5, help='Number of years (default 5)')
    parser_qtr.add_argument('-f', '--frequency', default='q', help='Frequency (m=monthly, q=quarterly, default=q)')
    parser_qtr.set_defaults(func=_parse_qtr_f)

    parser_nav_qtr = subparsers.add_parser('nav-qtr', help='NAV historical quarterly returns (all)')
    parser_nav_qtr.add_argument('ticker', help='Ticker')
    parser_nav_qtr.add_argument('-y', '--years', type=int, default=5, help='Number of years (default 5)')
    parser_nav_qtr.add_argument('-f', '--frequency', default='q', help='Frequency (m=monthly, q=quarterly, default=q)')
    parser_nav_qtr.set_defaults(func=_parse_nav_qtr_f)

    parser_cef_qtr = subparsers.add_parser('cef-qtr', help='Historical quarterly returns (all)')
    parser_cef_qtr.add_argument('ticker', help='Ticker')
    parser_cef_qtr.add_argument('-y', '--years', type=int, default=5, help='Number of years (default 5)')
    parser_cef_qtr.add_argument('-f', '--frequency', default='q', help='Frequency (m=monthly, q=quarterly, default=q)')
    parser_cef_qtr.set_defaults(func=_parse_cef_qtr_f)

    parser_fund_qtr = subparsers.add_parser('fund-qtr', help='Historical quarterly returns (all)')
    parser_fund_qtr.add_argument('ticker', help='Ticker')
    parser_fund_qtr.add_argument('-y', '--years', type=int, default=5, help='Number of years (default 5)')
    parser_fund_qtr.add_argument('-f', '--frequency', default='q', help='Frequency (m=monthly, q=quarterly, default=q)')
    parser_fund_qtr.set_defaults(func=_parse_fund_qtr_f)

    parser_qtr2 = subparsers.add_parser('qtr2', help='Historical quarterly returns (etfs, funds)')
    parser_qtr2.add_argument('ticker', help='Ticker')
    parser_qtr2.set_defaults(func=_parse_qtr2_f)

    parser_cef_quote = subparsers.add_parser('cef-quote', help='CEF quote')
    parser_cef_quote.add_argument('ticker', help='Ticker')
    parser_cef_quote.set_defaults(func=_parse_cef_quote)

    parser_etf_quote = subparsers.add_parser('etf-quote', help='ETF quote')
    parser_etf_quote.add_argument('ticker', help='Ticker')
    parser_etf_quote.set_defaults(func=_parse_etf_quote)

    parser_fund_quote = subparsers.add_parser('fund-quote', help='Fund quote')
    parser_fund_quote.add_argument('ticker', help='Ticker')
    parser_fund_quote.set_defaults(func=_parse_fund_quote)

    parser_stock_quote = subparsers.add_parser('stock-quote', help='Stock quote')
    parser_stock_quote.add_argument('ticker', help='Ticker')
    parser_stock_quote.set_defaults(func=_parse_stock_quote)

    parser_aal = subparsers.add_parser('aal', help='Asset allocation (etfs, funds)')
    parser_aal.add_argument('ticker', help='Ticker')
    parser_aal.set_defaults(func=_parse_aal)

    parser_mkc = subparsers.add_parser('mkc', help='Market capitalization (etfs, funds)')
    parser_mkc.add_argument('ticker', help='Ticker')
    parser_mkc.set_defaults(func=_parse_mkc)

    parser_sect = subparsers.add_parser('sect', help='Sector weightings (etfs, funds)')
    parser_sect.add_argument('ticker', help='Ticker')
    parser_sect.set_defaults(func=_parse_sect)

    parser_reg = subparsers.add_parser('reg', help='World regions (etfs, funds)')
    parser_reg.add_argument('ticker', help='Ticker')
    parser_reg.set_defaults(func=_parse_reg)

    parser_stock_profile = subparsers.add_parser('stock-profile', help='Stock profile')
    parser_stock_profile.add_argument('ticker', help='Ticker')
    parser_stock_profile.set_defaults(func=_parse_stock_profile)

    parser_stock_competitors = subparsers.add_parser('stock-competitors', help='Stock competitors')
    parser_stock_competitors.add_argument('ticker', help='Ticker')
    parser_stock_competitors.set_defaults(func=_parse_stock_competitors)

    args = parser.parse_args()
    args.func(args)
