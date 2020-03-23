import difflib

import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_page(url, suffix=""):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url + suffix, headers=headers)
    return BeautifulSoup(response.text, "html.parser")


def prepare_dataframe(dfs, concat=True):
    if concat:
        df = pd.concat(dfs)
    else:
        df = dfs

    df.replace('^\s+', '', regex=True, inplace=True)
    df.replace('\s+$', '', regex=True, inplace=True)
    return df.reset_index(drop=True)


def find_closest_name_match(teams_info, teams_result):
    matches = []
    for team in teams_info:
        match = difflib.get_close_matches(team, teams_result, 1, cutoff=0.53)
        if match:
            matches.append((team, match[0]))
        else:
            matches.append((team, ""))
    return dict(matches)


def keep_unique_teams(teams):
    return pd.DataFrame(pd.unique(teams['Team']), columns=['Team'])


def match_teams(df1, df2):
    """df1 jest krotsze"""
    teams_info = keep_unique_teams(df1)
    teams_result = keep_unique_teams(df2)

    teams_matches = find_closest_name_match(teams_info['Team'], teams_result['Team'])

    matched = {k: v for k, v in teams_matches.items() if v is not ""}
    to_match_manually = {k: v for k, v in teams_matches.items() if v is ""}

    df1['Team'] = df1['Team'].map(matched)

    return to_match_manually, df1
