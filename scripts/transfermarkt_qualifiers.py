import pandas as pd
from utils import scrape_page, prepare_dataframe
from bs4 import BeautifulSoup

URL_CL_QUALIFIERS = 'https://www.transfermarkt.com/uefa-champions-league-qualifying/startseite/pokalwettbewerb/CLQ?saison_id='
URL_EL_QUALIFIERS = 'https://www.transfermarkt.com/europa-league-qualifying/startseite/pokalwettbewerb/ELQ?saison_id='
SEASON_START = 2010
SEASON_END = 2016


def european_cup_qualifiers(page_content, season):
    rounds = BeautifulSoup(str(page_content.findAll('div', {'class': 'box pokalWettbewerbSpieltagsbox'})))

    homes = [home.text for home in rounds.findAll('td', {'class': 'verein-heim'})]
    aways = [away.text for away in rounds.findAll('td', {'class': 'verein-gast'})]
    results = [result.text for result in rounds.findAll('span', {'class': 'matchresult finished'})]

    transfermarkt_ids_homes = BeautifulSoup(str(rounds.findAll('td', {'class': 'verein-heim'})))
    transfermarkt_ids_homes = [id_.attrs['id'] for id_ in
                               transfermarkt_ids_homes.findAll('a', {'class': 'vereinprofil_tooltip'})]
    transfermarkt_ids_homes = transfermarkt_ids_homes[0::2]

    transfermarkt_ids_aways = BeautifulSoup(str(rounds.findAll('td', {'class': 'verein-gast'})))
    transfermarkt_ids_aways = [id_.attrs['id'] for id_ in
                               transfermarkt_ids_aways.findAll('a', {'class': 'vereinprofil_tooltip'})]
    transfermarkt_ids_aways = transfermarkt_ids_aways[0::2]

    return pd.DataFrame({"Home": homes,
                         "Away": aways,
                         "HomeId": transfermarkt_ids_homes,
                         "AwayId": transfermarkt_ids_aways,
                         "Result": results,
                         "Year": season})


cl_qualifiers, le_qualifiers = [], []

for season in range(SEASON_START, SEASON_END):
    page_content = scrape_page(URL_CL_QUALIFIERS, str(season))
    cl_qualifiers.append(european_cup_qualifiers(page_content, season))
    page_content = scrape_page(URL_EL_QUALIFIERS, str(season))
    le_qualifiers.append(european_cup_qualifiers(page_content, season))

cl_qualifiers_df = prepare_dataframe(cl_qualifiers)
le_qualifiers_df = prepare_dataframe(le_qualifiers)