import pandas as pd
import tqdm
import numpy as np

from scripts.soccerway import prepare_result_table, leagues_links_soccerway, seasons_in_league, rounds_table, \
    regular_table
from scripts.transfermarkt_detailed_team import get_squad_size, balance_info, transfers_info, basic_club_info
from scripts.transfermarkt_leagues import league_links, top_tier_leagues_links
from scripts.transfermarkt_teams_in_league import teams_list, teams_age, abroad_players, team_market_value, \
    keep_top_tier_teams
from scripts.uefa import uefa_country_rankings, keep_similar_leagues
from scripts.uefa_cups_results import prepare_uefa_results, collect_uefa_ids, collect_table
from scripts.utils import prepare_dataframe, scrape_page, match_teams

SEASON_START = 2009
SEASON_END = 2019
MINIMUM_SEASON = 10


URL_BASE = 'https://www.transfermarkt.com'
URL_UEFA = 'https://en.competitions.uefa.com/memberassociations/uefarankings/country/libraries//years/'
URL_COUNTRIES = 'https://www.transfermarkt.com/wettbewerbe/europa/wettbewerbe/'
URL_SOCCERWAY = 'https://int.soccerway.com/competitions/'
URL_SOCCERWAY_SEASON = 'https://int.soccerway.com/'
URL_UEFA_CLUBS = 'https://en.competitions.uefa.com/memberassociations/uefarankings/club/libraries//years/'
URL_UEFA_CUPS_RESULT = 'https://www.uefa.com/teamsandplayers/teams/club='

# #Ranking UEFA
# uefa_associations = []
# for season in range(SEASON_START, SEASON_END+1):
#     page_content = scrape_page(URL_UEFA, str(season))
#     uefa_associations.append(uefa_country_rankings(page_content, season))
#
# uefa_ranking = prepare_dataframe(uefa_associations)
# similar_leagues = keep_similar_leagues(uefa_ranking, distance=5)
#
# # Transfermarkt
# page_content = scrape_page(URL_COUNTRIES, "")
# all_leagues_links = league_links(page_content)
#
# # zostawiamy ligi na transfermartkt podobne do polskiej
# similar_leagues_links = all_leagues_links[all_leagues_links['Country'].isin(similar_leagues)].reset_index(drop=True)
# #pd.DataFrame(similar_leagues_links).to_csv("similar_leagues_links.csv", sep="|")
#
# # zbieramy linki tylko do najwyzszej klasy rozgrywkoej w danym kraju
# similar_leagues_top_tier_links = []
# for link in similar_leagues_links['Link']:
#     page_content = scrape_page(URL_BASE, link)
#     similar_leagues_top_tier_links.append(top_tier_leagues_links(page_content))
#
# similar_leagues_links['TopTierLink'] = similar_leagues_top_tier_links
#
# # zbieramy info ooglne klubach z tych lig
# teams_in_league = []
# for league_link, country in tqdm.tqdm(zip(similar_leagues_links['TopTierLink'], similar_leagues_links['Country'])):
#     for season in range(SEASON_START, SEASON_END):
#         page_content = scrape_page(URL_BASE + league_link + '/plus/?saison_id=',
#                                    str(season))
#         teams, links = teams_list(page_content)
#         age = teams_age(page_content)
#         a_players = abroad_players(page_content)
#         value, difference = team_market_value(page_content)
#         year = season
#         data = dict(Team=teams, Link=links, Age=age, AbroadPlayers=a_players, Value=value, Difference=difference,
#                     Year=season, Country=country)
#         teams_in_league.append(pd.DataFrame.from_dict(data))
#
# top_tier_teams = keep_top_tier_teams(teams_in_league, MINIMUM_SEASON)
# #pd.DataFrame(top_tier_teams).to_csv("top_tier_teams.csv", encoding='', sep="|")
#
# # zbieramy info detaliczne o  klubach z tych lig TUTAJ DZIAŁA BARDZO WOLNO!
# # metoda basic club ninfor zbiera info o stadionie - pomyslec jeszcze
# detailed_top_tier_teams = []
# for link in tqdm.tqdm(top_tier_teams['Link']):
#     page_content = scrape_page(URL_BASE, link)
#     club = basic_club_info(page_content, link)
#     club.squad_size = get_squad_size(page_content)
#     club.balance = balance_info(page_content)
#     page_content = scrape_page(URL_BASE, link.replace('startseite', 'transferrekorde'))
#     club.top_arrival = transfers_info(page_content)
#     page_content = scrape_page(URL_BASE, link.replace('startseite', 'rekordabgaenge'))
#     club.top_departure = transfers_info(page_content)
#     detailed_top_tier_teams.append(pd.DataFrame(club.to_dict(), index=[0]))
#
# detailed_teams_df = prepare_dataframe(detailed_top_tier_teams)
# teams_full_info = pd.merge(top_tier_teams, detailed_teams_df, right_index=True, left_index=True)

##################################################################################################
teams_full_info = pd.read_csv("teams_full_info.csv", index_col=0, sep="|")
##################################################################################################
similar_leagues = teams_full_info['Country'].unique()
page_content = scrape_page(URL_SOCCERWAY)
all_leagues_links_soccerway = prepare_dataframe([leagues_links_soccerway(page_content)])
similar_leagues_links_soccerway = all_leagues_links_soccerway[
    all_leagues_links_soccerway['Country'].isin(similar_leagues)].reset_index(drop=True)

links_to_particular_seasons = []
for country, link in zip(similar_leagues_links_soccerway['Country'], similar_leagues_links_soccerway['Link']):
    page_content = scrape_page(URL_SOCCERWAY_SEASON, link)
    links_to_particular_seasons.append(seasons_in_league(page_content, country))
links_to_particular_seasons = prepare_dataframe(links_to_particular_seasons)

links_to_particular_seasons['SeasonYear'] = links_to_particular_seasons['Season'].str[:4].astype(int)

particular_seasons = links_to_particular_seasons[(links_to_particular_seasons['SeasonYear'] >= SEASON_START) & (
            links_to_particular_seasons['SeasonYear'] < SEASON_END)]

# dfs_regular = []
# dfs_championship = []
# dfs_relegation = []
# empty = []
# for link, season, country in zip(particular_seasons['Link'], particular_seasons['SeasonYear'],
#                                 particular_seasons['Country']):
#    try:
#        page_content = scrape_page('https://int.soccerway.com/', link)
#        if page_content.findAll('select', {'name': 'round_id'}):
#            championship_table = prepare_result_table(rounds_table(page_content, season, country, "ChampionshipRound")[0])
#            relegation_table = prepare_result_table(rounds_table(page_content, season, country,  "RelegationRound")[1])
#            dfs_championship.append(championship_table)
#            dfs_relegation.append(relegation_table)
#        else:
#            dfs_regular.append(prepare_result_table(regular_table(link, season, country, "Regular")))
#    except:
#        dfs_regular.append(prepare_result_table(regular_table(link, season, country, "Regular")))
#        empty.append((link, season, country))


dfs_regular, dfs_championship, dfs_relegation, empty = [], [], [], []
for _, link, country, season in particular_seasons.itertuples(index=False):
    content = scrape_page('https://int.soccerway.com/', link)
    links_to_rounds = rounds_table(content)
    try:
        if 'Championship Round' in links_to_rounds:
            championship_table = prepare_result_table(regular_table(links_to_rounds["Championship Round"], 
                                                                    season, 
                                                                    country, 
                                                                    "Championship Round"))
            relegation_table = prepare_result_table(regular_table(links_to_rounds["Relegation Round"],
                                                                  season,
                                                                  country,
                                                                  "Relegation Round"))
            dfs_championship.append(championship_table)
            dfs_relegation.append(relegation_table)
        else:
            regular_table_ = prepare_result_table(regular_table(link,
                                                                season, 
                                                                country, 
                                                                "Regular Season"))
            dfs_regular.append(regular_table_)
    except:
        championship_table = prepare_result_table(regular_table(links_to_rounds["Championship Round"], 
                                                        season, 
                                                        country, 
                                                        "Championship Round"))
        empty.append((link, country, season))

        
regulars = prepare_dataframe(dfs_regular)
champions = prepare_dataframe(dfs_championship)
relegations = prepare_dataframe(dfs_relegation)

for link, country, season in empty:
    championship_table = prepare_result_table(regular_table(link, 
                                                            season, 
                                                            country, 
                                                            "Championship Round"))
    dfs_championship.append(championship_table)


season_results = pd.concat([regulars, champions, relegations])
##################################################################################################
season_results.to_csv("season_results.csv", encoding='utf-8-sig', sep="|")


ids = []
for season in range(SEASON_START, SEASON_END):
    page_content = scrape_page(URL_UEFA_CLUBS, str(season))
    ids.append(
        prepare_dataframe(pd.DataFrame(collect_uefa_ids(page_content), columns=['Team', 'UefaId']), concat=False))
ids = pd.concat(ids).drop_duplicates()

uefa_results_manually, teams_full_info_seasons_results_new_names = match_teams(teams_full_info_seasons_results, ids)

teams_full_info_seasons_uefa_results = pd.merge(teams_full_info_seasons_results_new_names, ids, left_on=['Team'], right_on=['Team'])

european_cup = []
for club_id in pd.unique(teams_full_info_seasons_uefa_results['UefaId']):
    try:
        european_cup.append(collect_table(URL_UEFA_CUPS_RESULT, club_id))
    except:
        pass
    
uefa_results = prepare_dataframe(european_cup)

uefa_results = prepare_uefa_results(prepare_dataframe(european_cup))

cl_results = uefa_results[uefa_results['Competition'] == 'UEFA Champions League']
el_results = uefa_results[uefa_results['Competition'] == 'UEFA Europa League']

teams_full_info_seasons_uefa_results_ = pd.merge(teams_full_info_seasons_uefa_results, cl_results, how= 'left', left_on=['UefaId', 'Year'], right_on=['UefaId', 'Year'], suffixes=('', '_CL'))
teams_full_info_seasons_uefa_results__ = pd.merge(teams_full_info_seasons_uefa_results_, el_results,  how= 'left', left_on=['UefaId', 'Year'], right_on=['UefaId', 'Year'], suffixes=('', '_EL'))



teams_full_info_seasons_uefa_results__.to_csv('check.csv')