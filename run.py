from transfermarkt_teams_in_league import teams_list, teams_age, abroad_players, team_market_value, keep_top_tier_teams
from transfermarkt_detailed_team import Club, squad_info, transfers_info, basic_club_info, prepare_dataframe
from transfermarkt_leagues import country_league_links, top_tier_league_link
from soccerway import optimize_df, leagues_links, seasons_in_league, rounds_table, regular_table
from uefa import uefa_country_rankings, similar_leagues
import pandas as pd
from bs4 import BeautifulSoup
import requests

SEASON_START = 2010
SEASON_END = 2016
MINIMUM_SEASON = 6

URL_BASE = 'https://www.transfermarkt.com'
URL_UEFA = 'https://en.competitions.uefa.com/memberassociations/uefarankings/country/libraries//years/'
URL_COUNTRIES = 'https://www.transfermarkt.com/wettbewerbe/europa/wettbewerbe/'
URL_SOCCERWAY = 'https://int.soccerway.com/competitions/'
URL_SOCCERWAY_SEASON = 'https://int.soccerway.com/'


def scrape_page(url, suffix=""):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url + suffix, headers=headers)
    return BeautifulSoup(response.text, "html.parser")

# UEFA RANKING
uefa = []
for season in range(SEASON_START, SEASON_END):
    page_content = scrape_page(URL_UEFA, str(season))
    uefa.append(uefa_country_rankings(page_content, season))

uefa_ranking = prepare_dataframe(uefa)
similar_leagues = similar_leagues(uefa_ranking, distance=2)

#Transfermarkt
page_content = scrape_page(URL_COUNTRIES, "")
country_league_link = country_league_links(page_content)

#zostawiamy ligi na transfermatk podobne do polskiej
countries = country_league_link[country_league_link['country'].isin(similar_leagues)].reset_index(drop=True)

#zbieramy do nich linki
leagues = []
for link in countries['link']:
    page_content = scrape_page(URL_BASE, link)
    leagues.append(top_tier_league_link(page_content))

#zbieramy info ooglne klubach z tych lig
teams_in_league = []
for league_link in leagues:
    for season in range(SEASON_START, SEASON_END):
        page_content = scrape_page(URL_BASE + league_link + '/plus/?saison_id=', str(season))# TUTAJ POPRAWIV TEN LINK PO KTORYM ON CHIDZI
        teams, links = teams_list(page_content)
        age = teams_age(page_content)
        a_players = abroad_players(page_content)
        value, difference = team_market_value(page_content)
        year = season
        data = dict(teams=teams, links=links, age=age, a_players=a_players, value=value, difference=difference, year=season)
        teams_in_league.append(pd.DataFrame.from_dict(data))

top_tier_teams = keep_top_tier_teams(teams_in_league, MINIMUM_SEASON)

#zbieramy info detaliczne o  klubach z tych lig
detailed_top_tier_teams = []
for link in top_tier_teams['links']:
    page_content = scrape_page(URL_BASE, link)
    club = basic_club_info(page_content, link)
    club.transfers = transfers_info(page_content)
    club.squad = squad_info(page_content)
    detailed_top_tier_teams.append(pd.DataFrame(club.to_dict(), index=[0]))

detailed_teams_df = prepare_dataframe(detailed_top_tier_teams)

#zbieramy wszystkie ligi z soccerway
page_content = scrape_page(URL_SOCCERWAY)
all_leagues= prepare_dataframe([leagues_links(page_content)])

similar_leagues = pd.read_csv(r'similar leagues.csv')
similar_leagues = similar_leagues['0'].values
#PODMIENIĆ POTEM NAZWY KOLUMN PONIZEJ
leagues = all_leagues[all_leagues['link'].isin(similar_leagues)].reset_index(drop=True)

links_to_particular_seasons = []
for link in leagues['country']:
    page_content = scrape_page(URL_SOCCERWAY_SEASON, link)
    links_to_particular_seasons.append(seasons_in_league(page_content))
links_to_particular_seasons = pd.concat(links_to_particular_seasons)

dfs_regular = []
dfs_rounds = []
for link in links_to_particular_seasons['link']:
     page_content = scrape_page('https://int.soccerway.com/', link)
     if  page_content.findAll('select', {'name': 'round_id'}):
         dfs_rounds.append(rounds_table(page_content))
     else:
         dfs_regular.append(regular_table(link))