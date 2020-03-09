import pandas as pd
import difflib

teams_full_info = pd.read_csv(r'C:\Users\marcin.kot1\Desktop\mgr\master\csv\teams_full_info.csv', index_col=0)
season_results = pd.read_csv(r'C:\Users\marcin.kot1\Desktop\mgr\master\csv\season_results.csv', index_col=0)

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
    teams_info = keep_unique_teams(df1)
    teams_result = keep_unique_teams(df2)

    teams_matches = find_closest_name_match(teams_info['Team'], teams_result['Team'])

    matched = {k: v for k, v in teams_matches.items() if v is not ""}
    to_match_manually = {k: v for k, v in teams_matches.items() if v is ""}

    teams_full_info['Team'] = teams_full_info['Team'].map(matched)

    teams_full_info_with_results = pd.merge(teams_full_info, season_results,
                                        how="left",
                                        left_on=['Team', 'Year'],
                                        right_on=['Team', 'year'])

    return to_match_manually, teams_full_info_with_results

