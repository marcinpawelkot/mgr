import pandas as pd
import requests
from bs4 import BeautifulSoup

def collect_uefa_ids(page_content):
    table = BeautifulSoup(str(page_content.findAll('div', {'class': 'grid-box col-xs-12 col-sm-12 col-md-12 col-lg-12'})))
    trs = table.find_all('tr')
    ids = [(tr.find('a').text, tr.attrs['data-team-id']) for tr in trs[1:]]
    return ids

def collect_table(url, club_id):
    table = pd.read_html(url + club_id + '/profile/history/index.html',
                        header=0)
    table[0]['club_id'] = club_id
    return table[0]
