import pandas as pd
from bs4 import BeautifulSoup


def uefa_ids(page_content):
    table = BeautifulSoup(str(page_content.findAll('tbody')))
    trs = table.find_all('tr')
    ids = [tr.attrs['data-team-id'] for tr in trs]
    teams = [tr.find('a').text for tr in trs]
    tds = table.find_all('td', {'class': "table_member-country"})
    countries = [td.text for td in tds]
    return pd.DataFrame(dict(CountryCode=countries, Team=teams, UefaId=ids))

def results_table(url, club_id):
    table = pd.read_html(url + club_id + '/profile/history/index.html',
                         header=0)
    table[0]['UefaId'] = club_id
    return table[0]
