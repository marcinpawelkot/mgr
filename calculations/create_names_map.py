import pandas as pd
import difflib
import pycountry

CSV_FILES_PATH = "./csv/"

def read_input(filename, header=0):
    return pd.read_csv(CSV_FILES_PATH + filename + ".csv", sep="|", header=header)

def save_output_to_csv(output, filename):
    output.to_csv(CSV_FILES_PATH + filename + ".csv", sep="|", index=False, encoding='utf-8-sig')

def find_closest_name_match(teams, pairs, cutoff):
    matches = []
    for team in teams:
        match = difflib.get_close_matches(team, pairs, 1, cutoff=cutoff)
        if match:
            matches.append((team, match[0]))
        else:
            matches.append((team, ""))
    return dict(matches)


def keep_unique_teams(teams):
    return teams.drop_duplicates(subset=["Team", "Country"])[["Team", "Country"]]


def match_teams(teams_to_pair, possible_matches, cutoff):
    """df1 jest krotsze"""
    teams_to_pair = keep_unique_teams(teams_to_pair)
    possible_matches = keep_unique_teams(possible_matches)
    teams_matches = {}

    for country in pd.unique(teams_to_pair["Country"]):
        teams = teams_to_pair[teams_to_pair["Country"]==country]
        possible_match = possible_matches[possible_matches["Country"]==country]
        teams_matches.update(find_closest_name_match(teams['Team'], possible_match['Team'], cutoff=cutoff))
        
    matched = {k: v for k, v in teams_matches.items() if v is not ""}
    to_match_manually = {k: v for k, v in teams_matches.items() if v is ""}

    return to_match_manually, matched

def countries_codes():
    url = 'https://en.wikipedia.org/wiki/List_of_FIFA_country_codes'
    table = pd.concat(pd.read_html(url)[:4])
    return dict(zip(table['Code'],table['Country']))

def read_list_from_csv(filename):
    with open(CSV_FILES_PATH + filename + ".csv") as f:
        my_list = f.read().splitlines()
    return my_list    

def cleanup_dataframe(df):
    df.replace('^\s+', '', regex=True, inplace=True)
    df.replace('\s+$', '', regex=True, inplace=True)
    return df.reset_index(drop=True)
    
similar_leagues = read_list_from_csv("similar_leagues")

transfermarkt = read_input("teams")
soccerway = read_input("season_results")
uefa = read_input("european_cups_record")


season_results_manually, season_match = match_teams(transfermarkt, soccerway, 0.4)

manual_map_season_result = {
 "Aalborg BK":"AaB",
 "AEL Limassol":"AEL",
 "APOEL Nicosia":"APOEL",
 "FK Qabala":"Qəbələ",
 "Odense BK":"OB",
 "Olympiacos":"Olympiakos Piraeus",
 "PAOK Salonika":"PAOK",
 "PFC Beroe Stara Zagora":"Beroe",
 "Red Star":"Crvena Zvezda",
 "Soligorsk":"Shakhtyor",

}

season_match.update(manual_map_season_result)
transfermarkt['Team'] = transfermarkt['Team'].map(season_match)

teams_with_dl_results = pd.merge(transfermarkt, soccerway,how="left", left_on = ["Team", "Year"], right_on=["Team", "Year"])

countries_map = countries_codes()

uefa['Country'] = uefa['CountryCode'].map(countries_map)
uefa_teams = cleanup_dataframe(uefa[uefa['Country'].isin(similar_leagues)].drop_duplicates(subset=["Team"])[["Team", "Country"]])

save_output_to_csv(uefa_teams.sort_values(by=["Country", "Team"]), "uefa_teams_names")
save_output_to_csv(transfermarkt.drop_duplicates(subset=["Team"])[["Country", "Team"]].sort_values(by=["Country", "Team"]), "transfermarkt_teams_names")

uefa_results_manually, uefa_match = match_teams(uefa_teams, transfermarkt, 0.5)
uefa_match.update(uefa_results_manually)
save_output_to_csv(pd.DataFrame(uefa_match.items()), "to_compare")

manual_map_uefa={
"Slovácko":"Slovácko",
"Silkeborg":"Silkeborg",
"OB	Odense":"BK",
"Lechia Gdańsk":"Lechia Gdańsk",
"Korona Kielce":"Korona Kielce",
"Kilmarnock":"Kilmarnock",
"Istra 1961":"Istra 1961",
"Hapoel Haifa":"Hapoel Haifa",
"Beroe":"PFC Beroe Stara Zagora",
"AE Paphos":"AE Paphos"}