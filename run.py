from transfermarkt_teams_in_league import teams_list, teams_age, abroad_players, team_market_value, keep_top_tier_teams
from transfermarkt_detailed_team import Club, get_squad_size, balance_info, transfers_info, basic_club_info
from transfermarkt_leagues import league_links, top_tier_leagues_links
from soccerway import prepare_result_table, optimize_df, leagues_links_soccerway, seasons_in_league, rounds_table, regular_table
from uefa import uefa_country_rankings, similar_leagues
import pandas as pd

from uefa_cups_results import collect_uefa_ids, collect_table
from utils import prepare_dataframe, scrape_page
import tqdm
SEASON_START = 2010
SEASON_END = 2016
MINIMUM_SEASON = 6

URL_BASE = 'https://www.transfermarkt.com'
URL_UEFA = 'https://en.competitions.uefa.com/memberassociations/uefarankings/country/libraries//years/'
URL_COUNTRIES = 'https://www.transfermarkt.com/wettbewerbe/europa/wettbewerbe/'
URL_SOCCERWAY = 'https://int.soccerway.com/competitions/'
URL_SOCCERWAY_SEASON = 'https://int.soccerway.com/'
URL_UEFA_CLUBS = 'https://en.competitions.uefa.com/memberassociations/uefarankings/club/libraries//years/'
URL_UEFA_CUPS_RESULT = 'https://www.uefa.com/teamsandplayers/teams/club='


# UEFA RANKING - gitówa
uefa_associations = []
for season in range(SEASON_START, SEASON_END):
    page_content = scrape_page(URL_UEFA, str(season))
    uefa_associations.append(uefa_country_rankings(page_content, season))

uefa_ranking = prepare_dataframe(uefa_associations)
similar_leagues = similar_leagues(uefa_ranking, distance=1)

# Transfermarkt
page_content = scrape_page(URL_COUNTRIES, "")
all_leagues_links = league_links(page_content)

# zostawiamy ligi na transfermartkt podobne do polskiej
similar_leagues_links = all_leagues_links[all_leagues_links['Country'].isin(similar_leagues)].reset_index(drop=True)

# zbieramy linki tylko do najwyzszej klasy rozgrywkoej w danym kraju
similar_leagues_top_tier_links = []
for link in similar_leagues_links['Link']:
    page_content = scrape_page(URL_BASE, link)
    similar_leagues_top_tier_links.append(top_tier_leagues_links(page_content))
    
similar_leagues_links['TopTierLink'] = similar_leagues_top_tier_links

# zbieramy info ooglne klubach z tych lig
teams_in_league = []
for league_link, country in zip(similar_leagues_links['TopTierLink'], similar_leagues_links['Country']):
    for season in range(SEASON_START, SEASON_END):
        page_content = scrape_page(URL_BASE + league_link + '/plus/?saison_id=',
                                   str(season))
        teams, links = teams_list(page_content)
        age = teams_age(page_content)
        a_players = abroad_players(page_content)
        value, difference = team_market_value(page_content)
        year = season
        data = dict(Team=teams, Link=links, Age=age, AbroadPlayers=a_players, Value=value, Difference=difference,
                    Year=season, Country=country)
        teams_in_league.append(pd.DataFrame.from_dict(data))

top_tier_teams = keep_top_tier_teams(teams_in_league, MINIMUM_SEASON)

# zbieramy info detaliczne o  klubach z tych lig TUTAJ DZIAŁA BARDZO WOLNO!
#metoda basic club ninfor zbiera info o stadionie - pomyslec jeszcze
detailed_top_tier_teams = []
for link in tqdm.tqdm(top_tier_teams['Link']):
    page_content = scrape_page(URL_BASE, link)
    club = basic_club_info(page_content, link)
    club.squad_size = get_squad_size(page_content)
    club.balance = balance_info(page_content)
    page_content = scrape_page(URL_BASE, link.replace('startseite', 'transferrekorde'))
    club.top_arrival = transfers_info(page_content)
    page_content = scrape_page(URL_BASE, link.replace('startseite', 'rekordabgaenge'))
    club.top_departure = transfers_info(page_content)
    detailed_top_tier_teams.append(pd.DataFrame(club.to_dict(), index=[0]))

detailed_teams_df = prepare_dataframe(detailed_top_tier_teams)

#ŁACZYMY 1 raz
teams_full_info = pd.merge(top_tier_teams, detailed_teams_df, right_index=True, left_index=True)

##############################################################3
similar_leagues = teams_full_info['Country'].unique()
##################################################################
similar_leagues = ["Poland", "Croatia", "Belarus", "Czech Republic", "Cyprus"]

page_content = scrape_page(URL_SOCCERWAY)
all_leagues_links_soccerway = prepare_dataframe([leagues_links_soccerway(page_content)])
similar_leagues_links_soccerway = all_leagues_links_soccerway[all_leagues_links_soccerway['Country'].isin(similar_leagues)].reset_index(drop=True)

links_to_particular_seasons = []
for country, link in zip(similar_leagues_links_soccerway['Country'], similar_leagues_links_soccerway['Link']):
    page_content = scrape_page(URL_SOCCERWAY_SEASON, link)
    links_to_particular_seasons.append(seasons_in_league(page_content, country))
links_to_particular_seasons = prepare_dataframe(links_to_particular_seasons)

links_to_particular_seasons['SeasonYear'] = links_to_particular_seasons['Season'].str[:4].astype(int)

particular_seasons = links_to_particular_seasons[(links_to_particular_seasons['SeasonYear'] >= SEASON_START) & (links_to_particular_seasons['SeasonYear'] <= SEASON_END)]

dfs_regular = []
dfs_championship = []
dfs_relegation = []
for link, season, country in zip(particular_seasons['Link'], particular_seasons['SeasonYear'], particular_seasons['Country']):
    page_content = scrape_page('https://int.soccerway.com/', link)
    if page_content.findAll('select', {'name': 'round_id'}):
        championship_table = prepare_result_table(rounds_table(page_content,season, country)[0])
        relegation_table = prepare_result_table(rounds_table(page_content, season, country)[1])
        dfs_championship.append(championship_table)
        dfs_relegation.append(relegation_table)
    else:
        dfs_regular.append(prepare_result_table(regular_table(link, season, country)))


regulars = prepare_dataframe(dfs_regular)
champions = prepare_dataframe(dfs_championship)
relegations = prepare_dataframe(dfs_relegation)

season_results = pd.concat([regulars, champions, relegations])

season_results.to_csv("season_results.csv", encoding='utf=-8')


#ŁACZYMY 2 raz
teams_full_info_with_results = pd.read_csv('teams_full_info_with_results.csv', index_col=0, sep=';')
ids = []
for season in range(SEASON_START, SEASON_END):
    page_content = scrape_page(URL_UEFA_CLUBS, str(season))
    ids.append(prepare_dataframe(pd.DataFrame(collect_uefa_ids(page_content), columns = ['club_name', 'club_id']), concat=False))
ids = pd.concat(ids)
ids.drop_duplicates(inplace=True)
teams_full_info_with_results['Team_x']


#idss = ids[ids['club_name'].isin(pd.unique(teams_full_info_with_results['Team']))]
import difflib

def create_map_teams_names(teams, ids_list):
    matches = []
    for team in teams:
        match = difflib.get_close_matches(team, ids_list)
        if match:
            matches.append((team, match[0]))
        else:
            matches.append((team, ""))
    return dict(matches)

map_results_to_info = create_map_teams_names(teams_full_info_with_results['Team_x'], ids['club_name'])

european_cup = []
for club_id in ids['club_id']:
    try:
        european_cup.append(collect_table(URL_UEFA_CUPS_RESULT, club_id))
    except:
        pass
    
    


url = 'https://www.transfermarkt.com/europa-league-qualifikation/gesamtspielplan/pokalwettbewerb/ELQ/saison_id/2018'
def scrape_page(url, suffix=""):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url + suffix, headers=headers)
    return BeautifulSoup(response.text, "html.parser")


page_content = scrape_page(url)


table = str(page_content.findAll('div', {'class': 'large-8 columns'}))

for t in table:
    print(t)
table1 = pd.read_html(table)
#rozłozyc ten final na lata
final = prepare_dataframe(european_cup)
final['SeasonYear'] = final['Season'].str[:4].astype(int)
final['STAGE'] = final['Stage'] + final['Stage reached']
import numpy as np
final['Stage'] = final['Stage'].replace(np.nan, '', regex=True)
final['Stage reached'] = final['Stage reached'].replace(np.nan, '', regex=True)
final['STAGE'] = final['Stage'] + final['Stage reached']
final.drop(labels=['Club Profile','Info', 'Stage', 'Stage reached','Season'], axis=1, inplace=True)
final_ = pd.merge(final, ids, left_on='club_id',right_on='club_id')

result = pd.merge(final_, teams_full_info_with_results, left_on=['club_name', 'SeasonYear'],right_on=['Team','Year'])
result.to_csv('result.csv')