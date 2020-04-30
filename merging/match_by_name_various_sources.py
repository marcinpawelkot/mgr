import difflib

import pandas as pd

from helpers.utils import read_input, save_output_to_csv

manual_map_season_result = {
    "Aalborg BK": "AaB",
    "AEL Limassol": "AEL",
    "APOEL Nicosia": "APOEL",
    "FK Qabala": "Qəbələ",
    "Odense BK": "OB",
    "Olympiacos": "Olympiakos Piraeus",
    "PAOK Salonika": "PAOK",
    "PFC Beroe Stara Zagora": "Beroe",
    "Red Star": "Crvena Zvezda",
    "Soligorsk": "Shakhtyor",

}

# teams not matched or miss matched function, keys - transfermarkt, values - uefa
manual_map_uefa = {
    "Qəbələ": "Gabala SC",
    "BATE": "FC BATE Borisov",
    "Istra 1961": "Istra 1961",
    "Slovácko": "Slovácko",
    "HJK": "HJK Helsinki",
    "Tobol": "FC Tobol Kostanay",
    "Korona Kielce": "Korona Kielce",
    "Lechia Gdańsk": "Lechia Gdańsk",
    "Kilmarnock": "Kilmarnock"
}


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
    teams_to_pair = keep_unique_teams(teams_to_pair)
    possible_matches = keep_unique_teams(possible_matches)
    teams_matches = {}

    for country in pd.unique(teams_to_pair["Country"]):
        teams = teams_to_pair[teams_to_pair["Country"] == country]
        possible_match = possible_matches[possible_matches["Country"] == country]
        teams_matches.update(find_closest_name_match(teams['Team'], possible_match['Team'], cutoff=cutoff))

    matched = {k: v for k, v in teams_matches.items() if v is not ""}
    to_match_manually = {k: v for k, v in teams_matches.items() if v is ""}

    return to_match_manually, matched


def teams_with_incomplete_season(df):
    na_free = df.dropna()
    only_na = df[~df.index.isin(na_free.index)]
    return only_na["Team"]


def merge_transfermarkt_soccerway(transfermarkt, soccerway):
    season_results_manually, season_match = match_teams(transfermarkt, soccerway, 0.4)
    season_match.update(manual_map_season_result)
    transfermarkt['Team'] = transfermarkt['Team'].map(season_match)
    return pd.merge(transfermarkt, soccerway, how="left", left_on=["Team", "Year"],
                    right_on=["Team", "Year"], suffixes=('', '_y'))


def keep_complete(transfermarkt_soccerway):
    teams_incomplete = teams_with_incomplete_season(transfermarkt_soccerway)
    teams_complete = transfermarkt_soccerway[~transfermarkt_soccerway.Team.isin(teams_incomplete)]
    return teams_incomplete, teams_complete


def rename_qualifiers_cols(df, cup):
    cols_init = ['Competition', 'Stage', 'MatchesPlayed', 'Wins', 'Draws', 'Losses']
    cols_final = [col + cup for col in cols_init]
    df.rename(columns=dict(zip(cols_init, cols_final)), inplace=True)
    return df[['UefaId', 'Year'] + cols_final]


def run():
    transfermarkt = read_input("teams")
    soccerway = read_input("season_results")
    uefa = read_input("european_cups_record")

    transfermarkt_soccerway = merge_transfermarkt_soccerway(transfermarkt, soccerway)
    _, teams_complete = keep_complete(transfermarkt_soccerway)

    uefa_results_manually, uefa_match = match_teams(teams_complete, uefa, 0.5)
    uefa_match.update(manual_map_uefa)
    teams_complete['Team'] = teams_complete['Team'].map(uefa_match)

    uefa_ids = uefa[['Team', 'Country', 'UefaId']].drop_duplicates()
    teams_with_uefa_id = pd.merge(teams_complete, uefa_ids[["UefaId", "Team"]], how="left", left_on=["Team"],
                                  right_on=["Team"])

    el_results = uefa[uefa['Competition'] == 'UEFA Europa League']
    el_results = rename_qualifiers_cols(el_results, "AllEL")

    cl_results = uefa[uefa['Competition'] == 'UEFA Champions League']
    cl_results = rename_qualifiers_cols(cl_results, "AllCL")

    teams_dl_uefa_record = pd.merge(teams_with_uefa_id, cl_results,
                                    how='left',
                                    left_on=['UefaId', 'Year'],
                                    right_on=['UefaId', 'Year']).merge(el_results,
                                                                       how='left',
                                                                       left_on=['UefaId', 'Year'],
                                                                       right_on=['UefaId', 'Year'])

    save_output_to_csv(teams_dl_uefa_record, "teams_dl_uefa_record")
