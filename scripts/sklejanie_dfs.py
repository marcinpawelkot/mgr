import pandas as pd
import difflib

teams_full_info = pd.read_csv('teams_full_info.csv', index_col=0)
season_results = pd.read_csv('season_results.csv', index_col=0)

def find_closest_name_match(teams_info, teams_result):
    matches = []
    for team in teams_info:
        match = difflib.get_close_matches(team, teams_result)
        if match:
            matches.append((team, match[0]))
        else:
            matches.append((team, ""))
    return dict(matches)

def keep_unique_teams(teams):
    return pd.DataFrame(pd.unique(teams['Team']), columns=['Team'])


teams_info = keep_unique_teams(teams_full_info)
teams_result = keep_unique_teams(season_results)

teams_matches = find_closest_name_match(teams_info['Team'], teams_result['Team'])

def create_map_teams_names(info, results):
    matches = []
    for team in info['info_key']:
        match = difflib.get_close_matches(team, list(result['results_key']))
        if match:
            matches.append((team, match[0]))
        else:
            matches.append((team, ""))
    return dict(matches)

map_results_to_info = create_map_teams_names(teams_full_info, season_results)

teams_full_info['info_key'] = teams_full_info['info_key'].map(map_results_to_info)

teams_full_info_with_results = pd.merge(teams_full_info, season_results, 
                                        how="left",
                                        left_on=['info_key', 'Year'],
                                        right_on=['results_key', 'year'])
teams_full_info_with_results.to_csv("teams_full_info_with_results.csv")


def fuzzy_merge(df_1, df_2, key1, key2, threshold=0, limit=2):
    """
    df_1 is the left table to join
    df_2 is the right table to join
    key1 is the key column of the left table
    key2 is the key column of the right table
    threshold is how close the matches should be to return a match, based on Levenshtein distance
    limit is the amount of matches that will get returned, these are sorted high to low
    """
    s = df_2[key2].tolist()

    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m

    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2

    return df_1

def merge_teams_names(teams_info_list, teams_results_list, key1, key2):
    df = fuzzy_merge(teams_info_list, teams_results_list, key1, key2, threshold=80)
    df['matches'].dropna(inplace=True)
    return df

key1 = 'info_key'
key2 = 'results_key'

merged_teams_names = merge_teams_names(info, result, key1, key2)


teams_full_info_with_results['Wins'].dropna(inplace=True)
teams_full_info_with_results.to_csv('teams_full_info_with_results.csv')




