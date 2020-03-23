import pandas as pd

teams = pd.read_csv("teams_full_info.csv", index_col=0, sep="|")
season_results = pd.read_csv("season_results.csv", index_col=0, sep="|")
season_results.sort_values(by=['Team', 'Year', 'MatchesPlayed'], inplace=True)
season_results = season_results.drop_duplicates(subset=['Team', 'Year'], keep='last')

#SCREPOWAC BOK STRONY!
season_results[['MatchesPlayed', 'Wins', 'Draws', 'Losses']] = season_results[['MatchesPlayed', 'Wins', 'Draws', 'Losses']].add_suffix('_DL')

cols = ['MatchesPlayed', 'Wins', 'Draws', 'Losses']
cols_dl = ['MatchesPlayed_DL', 'Wins_DL', 'Draws_DL', 'Losses_DL']

season_results.rename(columns = dict(zip(cols, cols_dl)), inplace=True)

ids = []
for season in range(SEASON_START, SEASON_END):
    page_content = scrape_page(URL_UEFA_CLUBS, str(season))
    ids.append(
        prepare_dataframe(pd.DataFrame(collect_uefa_ids(page_content), columns=['Team', 'UefaId']), concat=False))
ids = pd.concat(ids).drop_duplicates()

uefa_results_manually, teams_uefa_ids = match_teams(teams, ids)

teams_uefa = pd.merge(teams_uefa_ids, ids, how= 'left', left_on=['Team'], right_on=['Team'], suffixes=('', '_CL'))

european_cup = []
for club_id in pd.unique(teams_uefa['UefaId']):
    try:
        european_cup.append(collect_table(URL_UEFA_CUPS_RESULT, club_id))
    except:
        pass

uefa_results = prepare_uefa_results(prepare_dataframe(european_cup))
cl_results = uefa_results[uefa_results['Competition'] == 'UEFA Champions League']
cols = ['MatchesPlayed', 'Wins', 'Draws', 'Losses']
cols_cl = ['MatchesPlayed_CL', 'Wins_CL', 'Draws_CL', 'Losses_CL']
cl_results.rename(columns = dict(zip(cols, cols_cl)), inplace=True)

el_results = uefa_results[uefa_results['Competition'] == 'UEFA Europa League']
cols = ['MatchesPlayed', 'Wins', 'Draws', 'Losses']
cols_el = ['MatchesPlayed_EL', 'Wins_EL', 'Draws_EL', 'Losses_EL']
el_results.rename(columns = dict(zip(cols, cols_el)), inplace=True)

teams_ = pd.merge(teams_uefa, cl_results, how= 'left', left_on=['UefaId', 'Year'], right_on=['UefaId', 'Year']).merge(el_results,  how= 'left', left_on=['UefaId', 'Year'], right_on=['UefaId', 'Year'], suffixes=('', '_EL'))

teams_.dropna(axis=0, subset=['Team'] , inplace=True)

season_results_manually, teams_results = match_teams(teams_, season_results)
teams_full_info = pd.merge(teams_results, season_results, left_on=['Team', 'Year'], right_on=['Team', 'Year'])

teams = teams_full_info.drop_duplicates(subset=['Team', 'Year'], keep='first')


teams.to_csv("teams.csv", encoding='utf-8-sig', sep="|")