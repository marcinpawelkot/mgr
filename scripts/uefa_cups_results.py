import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np


def collect_uefa_ids(page_content):
    table = BeautifulSoup(str(page_content.findAll('tbody')))
    trs = table.find_all('tr')
    ids = [(tr.find('a').text, tr.attrs['data-team-id']) for tr in trs[1:]]
    return ids

def collect_table(url, club_id):
    table = pd.read_html(url + club_id + '/profile/history/index.html',
                        header=0)
    table[0]['UefaId'] = club_id
    return table[0]


def prepare_uefa_results(uefa_results):
    uefa_results = uefa_results.replace(np.nan, '', regex=True)
    uefa_results['Year'] = uefa_results['Season'].str[:4].astype(int)
    uefa_results['Stage'] = uefa_results['Stage'] + uefa_results['Stage reached']
    uefa_results.rename(columns={"P": "MatchesPlayed", "W": "Wins", "D": "Draws","L": "Losses"}, inplace=True)
    return uefa_results[['Year', 'UefaId', 'Competition', 'Stage', 'MatchesPlayed', 'Wins', 'Draws', 'Losses']]
