import pandas as pd
from bs4 import BeautifulSoup


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

    match_sheets = [sheet.get('href') for sheet in rounds.findAll('a', {'title': 'Match Sheet'})]

    if season == 2016 and len(results) < len(aways):  # missing record on site for EL qualifiers
        insert_at = 201
        results[insert_at:insert_at] = ["3:1"]
        match_sheets[insert_at:insert_at] = [""]

    return pd.DataFrame({"Home": homes,
                         "Away": aways,
                         "HomeId": transfermarkt_ids_homes,
                         "AwayId": transfermarkt_ids_aways,
                         "Result": results,
                         "Year": season,
                         "MatchSheet": match_sheets})


def first_game_result(page_content):
    first_game_result = page_content.findAll('a', {'title': 'Match report'})
    return first_game_result[0].text
