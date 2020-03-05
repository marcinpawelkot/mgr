import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_page(url, suffix=""):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url + suffix, headers=headers)
    return BeautifulSoup(response.text, "html.parser")

def prepare_dataframe(dfs, concat=True):
    if concat:
        df = pd.concat(dfs)
    else:
        df = dfs
        
    df.replace('^\s+', '', regex=True, inplace=True)
    df.replace('\s+$', '', regex=True, inplace=True)
    return df.reset_index(drop=True)