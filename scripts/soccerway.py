import pandas as pd
from bs4 import BeautifulSoup
import requests

def optimize_df(df):
    df.reset_index(inplace=True, drop=True)
    df.drop(df.columns[[0, 11, 12]], axis=1, inplace=True)
    df.drop(df.index[[16, 17]], inplace=True)


def leagues_links_soccerway(page_content): #tutaj zbieramy linki do poszczegolnych lig
    countries = []
    links = []
    countries_table = page_content.findAll('div', {'class': 'row'})
    for t in countries_table:
        links.append(t.find('a').get('href'))
        countries.append(t.find('a').text)
    return pd.DataFrame(dict(Country=countries, Link=links))

def seasons_in_league(content, country):
    countries_league = content.findAll('select', {'name': 'season_id'})
    leagues = BeautifulSoup(str(countries_league))
    seasons = []
    links= []
    for line in leagues.findAll('option'):
        links.append(line['value'])
        seasons.append(line.text)
    return pd.DataFrame(dict(Season=seasons, Link=links, Country=country))

def rounds_table(content, season, country):
    content = content.findAll('select', {'name': 'round_id'})
    rounds = BeautifulSoup(str(content))
    round_name = []
    round_link = []

    for line in rounds.findAll('option')[:2]:
        round_link.append(line['value'])
        round_name.append(line.text)

    return regular_table(round_link[0], season, country), regular_table(round_link[1], season, country)


def regular_table(suffix, season, country):
    url = 'https://int.soccerway.com/' + suffix
    table = pd.read_html(url,
                        index_col = 0,
                        header=0,
                        attrs = {'class':'leaguetable sortable table detailed-table'})[0]
    table['Year'] = season
    table['Country'] = country
    return table

def prepare_result_table(df):
    columns = ['Team', 'MP', 'W', 'D', 'L', 'F', 'A', 'D.1', 'P', 'Year', 'Country']
    df = df[columns]
    df.dropna(inplace=True)
    new_df = df[~df['Team'].str.contains("UEFA")]
    new_df_ = new_df[~new_df['Team'].str.contains("Corrections")]
    new_df__ = new_df_[~new_df_['Team'].str.contains("Relegation")]
    new_df__.reset_index(inplace=True, drop=True)
    columns = ['Team', 'Matches Played', 'Wins', 'Draws', 'Losses', 'Goals Scored', 'Goals Against', 'Goals balance', 'Points', 'year', 'Country']
    new_df__.columns = columns
    return new_df__


