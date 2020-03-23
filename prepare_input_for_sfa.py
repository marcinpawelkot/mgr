import pandas as pd
import numpy as np
teams = pd.read_csv("teams.csv", index_col=0, sep="|")


repl_dict = {'[kK]': '*1e3', '[mM]': '*1e6', '[bB]': '*1e9', }
cols = [teams.TopArrival, teams.TopDeparture, teams.IncomeValue, teams.ExpenditureValues, teams.OverallBalance]

teams['TopArrival'] = teams['TopArrival'].str.replace("Free transfer", "0")
teams['TopDeparture'] = teams['TopDeparture'].str.replace("Free transfer", "0")
teams = teams.replace("?", "0")


teams.TopArrival = (teams.TopArrival.replace(r'[km]+$', '', regex=True).astype(float) * teams.TopArrival.str.extract(r'[\d\.]+([km]+)', expand=False).fillna(1).replace(['k','m'], [10**3, 10**6]).astype(int))
teams.TopDeparture = (teams.TopDeparture.replace(r'[km]+$', '', regex=True).astype(float) * teams.TopDeparture.str.extract(r'[\d\.]+([km]+)', expand=False).fillna(1).replace(['k','m'], [10**3, 10**6]).astype(int))
teams.IncomeValue = (teams.IncomeValue.replace(r'[km]+$', '', regex=True).astype(float) * teams.IncomeValue.str.extract(r'[\d\.]+([km]+)', expand=False).fillna(1).replace(['k','m'], [10**3, 10**6]).astype(int))
teams.ExpenditureValues = (teams.ExpenditureValues.replace(r'[km]+$', '', regex=True).astype(float) * teams.ExpenditureValues.str.extract(r'[\d\.]+([km]+)', expand=False).fillna(1).replace(['k','m'], [10**3, 10**6]).astype(int))
teams.OverallBalance = (teams.OverallBalance.replace(r'[km]+$', '', regex=True).astype(float) * teams.OverallBalance.str.extract(r'[\d\.]+([km]+)', expand=False).fillna(1).replace(['k','m'], [10**3, 10**6]).astype(int))
teams.Value = (teams.Value.replace(r'[km]+$', '', regex=True).astype(float) * teams.Value.str.extract(r'[\d\.]+([km]+)', expand=False).fillna(1).replace(['k','m'], [10**3, 10**6]).astype(int))
teams.Difference = (teams.Difference.replace(r'[km]+$', '', regex=True).astype(float) * teams.Difference.str.extract(r'[\d\.]+([km]+)', expand=False).fillna(1).replace(['k','m'], [10**3, 10**6]).astype(int))

teams.replace(np.nan, 0, inplace=True)

teams["MaxPoints_DL"] = teams["MatchesPlayed_DL"] * 3
teams["Score"] = teams["Points"] / teams["MaxPoints_DL"]

teams.to_csv("teams_with_score.csv", encoding='utf-8-sig', sep="|", index=False)

teams = pd.read_csv("teams_with_score.csv", index_col=None, sep="|")
teams.to_csv("teams_with_score.csv", encoding='utf-8', sep="|", index=False)

