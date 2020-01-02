import requests
from bs4 import BeautifulSoup
import pandas as pd


def teams_list(page_content):
    teams = page_content.findAll('td', {'class': 'hauptlink no-border-links show-for-small show-for-pad'})
    teams_names = [t.text for t in teams]
    teams_links = [t.find('a').get('href') for t in teams]
    return teams_names, teams_links


def teams_age(page_content):
    teams_age = page_content.findAll('td', {'class': 'zentriert hide-for-small hide-for-pad'})
    return [t.text for t in teams_age][1:]


def abroad_players(page_content):
    teams_abroad = page_content.findAll('td', {'class': 'zentriert hide-for-pad hide-for-small'})
    return [t.text for t in teams_abroad][1:]


def team_market_value(page_content):
    teams_market_value = page_content.findAll('td', {'class': 'rechts show-for-small show-for-pad nowrap'})
    teams_market_value_single_difference = [t.text for t in teams_market_value][2:]
    teams_market_value_single = teams_market_value_single_difference[::2]
    teams_market_difference_value_single = teams_market_value_single_difference[1::2]
    return teams_market_value_single, teams_market_difference_value_single


def keep_top_tier_teams(teams_by_sesons, minimum_number_of_seasons):
    teams_by_season_df = pd.concat(teams_by_sesons).reset_index(drop=True)
    top_tier_teams = list(teams_by_season_df.groupby(['teams']).count()[
                              teams_by_season_df.groupby(['teams']).count() == minimum_number_of_seasons].dropna().index)
    return teams_by_season_df[teams_by_season_df['teams'].isin(top_tier_teams)].reset_index(drop=True)
