import numpy as np
import pandas as pd

from utils.utils import read_input, save_output_to_csv

CSV_FILES_PATH = "../csv/"
SEASON_START = 2009
SEASON_END = 2019


def prepare_for_record(df):
    df = df.reindex(columns=df.columns.tolist() + ["WinHome", "WinAway", "LossesHome", "LossesAway", "Draw"])
    df[["HomeGoals", "AwayGoals"]] = df["Result"].str.split(n=2, pat=":", expand=True)

    df.loc[df['Result'].str.contains('pens'), 'HomeGoals'] = '0'
    df.loc[df['Result'].str.contains('pens'), 'AwayGoals'] = '0'

    df["HomeGoals"] = df["HomeGoals"].str.extract('(\d+)', expand=False).astype(int)
    df["AwayGoals"] = df["AwayGoals"].str.extract('(\d+)', expand=False).astype(int)

    df.replace(np.nan, 0, inplace=True)
    return df


def fill_results(df):
    df['Draw'][df["HomeGoals"] == df["AwayGoals"]] = 1

    df['WinHome'][df["HomeGoals"] > df["AwayGoals"]] = 1
    df["LossesAway"][df["HomeGoals"] > df["AwayGoals"]] = 1

    df['WinAway'][df["HomeGoals"] < df["AwayGoals"]] = 1
    df["LossesHome"][df["HomeGoals"] < df["AwayGoals"]] = 1

    return df


def calculate_record(df, season):
    home = df.groupby("HomeId")[["Draw", "WinHome", "LossesHome"]].sum()
    away = df.groupby("AwayId")[["Draw", "LossesAway", "WinAway"]].sum()
    record = pd.merge(home, away, right_index=True, left_index=True, suffixes=["Home", "Away"])

    record["Wins"] = record["WinHome"] + record['WinAway']
    record["Draws"] = record["DrawHome"] + record["DrawAway"]
    record["Losses"] = record["LossesAway"] + record["LossesHome"]

    record.reset_index(inplace=True, drop=False)
    record["Year"] = season
    record = record.rename(columns={record.columns[0]: "Id"})
    return record[["Id", "Wins", "Draws", "Losses", "Year"]]


cl_qualifiers_raw = read_input("cl_qualifiers")
el_qualifiers_raw = read_input("el_qualifiers")

cl_qualifiers, el_qualifiers = [], []
for season in range(SEASON_START, SEASON_END):
    cl_single_season = cl_qualifiers_raw[cl_qualifiers_raw["Year"] == season].copy()
    el_single_season = el_qualifiers_raw[el_qualifiers_raw["Year"] == season].copy()

    cl_qualifiers.append(
        calculate_record(fill_results(prepare_for_record(cl_single_season)), season)
    )
    el_qualifiers.append(
        calculate_record(fill_results(prepare_for_record(el_single_season)), season)
    )

cl_qualifiers_record = pd.concat(cl_qualifiers)
el_qualifiers_record = pd.concat(el_qualifiers)

save_output_to_csv(cl_qualifiers_record, "cl_qualifiers_aggregated")
save_output_to_csv(el_qualifiers_record, "el_qualifiers_aggregated")
