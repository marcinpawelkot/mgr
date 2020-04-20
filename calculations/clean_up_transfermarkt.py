import pandas as pd

CSV_FILES_PATH = "../csv/"
SEASON_START = 2009
SEASON_END = 2019


def read_input(filename, header=0):
    return pd.read_csv(CSV_FILES_PATH + filename + ".csv", sep="|", header=header)


def save_output_to_csv(output, filename):
    output.to_csv(CSV_FILES_PATH + filename + ".csv", sep="|", index=False)


def change_transfers_to_numerical(teams):
    teams['TopArrival'] = teams['TopArrival'].str.replace("Free transfer", "0")
    teams['TopDeparture'] = teams['TopDeparture'].str.replace("Free transfer", "0")


def change_age_to_numerical(teams):
    teams["Age"] = teams["Age"].str.replace(",", ".")
    teams["Age"] = pd.to_numeric(teams["Age"])


def convert_units(teams):
    repl_dict = {'[kK]': '*1e3', '[mM]': '*1e6', '[bB]': '*1e9', }
    columns = ["TopArrival", "TopDeparture", "IncomeValue", "ExpenditureValues", "OverallBalance", "Difference"]

    for col in columns:
        teams[col] = teams[col].str.replace("€", "")
        teams[col] = teams[col].replace("?", "0")
        teams[col] = teams[col].replace(repl_dict, regex=True).map(pd.eval).astype(int)

    return teams


teams_general = read_input("teams_general")
teams_detailed = read_input("teams_detailed")

teams = pd.merge(teams_general, teams_detailed, left_index=True, right_index=True)

change_transfers_to_numerical(teams)
change_age_to_numerical(teams)
teams = convert_units(teams)

save_output_to_csv(teams, "teams")