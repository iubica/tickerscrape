"""
Routines for caching web queries
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import six

_web_cache = dict()

def get_web_page(url, force):
    """
    Gets a web page from the web, or from the local cache, in case it is cached.

    Arguments:
    url - the URL to retrieve
    force - if True, overwrite the cache
    
    Return value:
    The contents of the web page
    """
    if force or (url not in _web_cache):
        r = requests.get(url)
        _web_cache[url] = r.content                

    return _web_cache[url]


def get_web_page_table(url, force, table_idx):
    """
    Gets a web page table in DataFrame format

    Arguments:
    url - the URL to retrieve
    force - if True, overwrite the cache
    table_idx - the index of the table
    
    Return value:
    The DataFrame associated to the table
    """
    # Get the page
    web_page = get_web_page(url, force)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    # List of all tables
    tables = soup.find_all('table')

    # Specific tables
    table = tables[table_idx]

    # Get the number of rows and columns
    row_count = len(table.find_all('tr'))
    column_count = 0

    for row in table.find_all('tr'):
        column_idx = len(row.find_all('th')) + len(row.find_all('td'))
        if column_count < column_idx:
            column_count = column_idx
    
    #print("row_count = %s, column_count = %s"%(row_count, column_count))

    df = pd.DataFrame(columns = range(column_count), 
                      index = range(row_count))
    
    row_idx = 0
    for row in table.find_all('tr'):
        column_idx = 0
        columns = row.find_all('th') + row.find_all('td')
        for column in columns:
            column_text = column.get_text()
    
            #print("row_idx %d, cloumn_idx %d, text %s" % (row_idx, column_idx, column_text))
            df.iat[row_idx, column_idx] = column_text
            column_idx += 1
        row_idx += 1

    return df

def dataframe_promote_1st_row_and_column_as_labels(df):
    """
    Moves the DataFrame first row as column labels, and the first column
    as row labels.

    Arguments:
    df - the DataFrame

    Returns: the updated Dataframe
    """
    table_name = df.at[0, 0].strip()

    df.at[0, 0] = "_"

    # Promote 1st row as column labels
    transform = lambda x: x.strip() if isinstance(x, six.string_types) else x
    df.columns = df.iloc[0].map(transform)
    df = df[1:]
    
    # Promote 1st column as new index
    df2 = df.set_index("_")
    df = df2

    df.index.name = table_name

    return df

if __name__ == "__main__":
    pass
