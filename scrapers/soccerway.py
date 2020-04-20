import pandas as pd
from bs4 import BeautifulSoup


def leagues_links_soccerway(page_content):
    countries, links = [], []
    leagues_table = page_content.findAll('div', {'class': 'row'})
    for league in leagues_table:
        links.append(league.find('a').get('href'))
        countries.append(league.find('a').text)
    return pd.DataFrame(dict(Country=countries, Link=links))


def seasons_in_league(content, country):
    countries_league = content.findAll('select', {'name': 'season_id'})
    leagues = BeautifulSoup(str(countries_league))
    seasons, links = [], []
    for line in leagues.findAll('option'):
        links.append(line['value'])
        seasons.append(line.text)
    return pd.DataFrame(dict(Season=seasons, Link=links, Country=country))


def rounds_links(content):
    content = content.findAll('li', {'class': 'expanded'})
    rounds = BeautifulSoup(str(content))
    round_link = {}
    for line in rounds.findAll('a'):
        round_link[line.text] = line.attrs['href']
    return round_link


def result_table(suffix):
    url = 'https://int.soccerway.com/' + suffix
    return pd.read_html(url,
                        index_col=0,
                        header=0,
                        attrs={'class': 'leaguetable sortable table detailed-table'})[0]
