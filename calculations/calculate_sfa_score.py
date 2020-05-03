import numpy as np
import pandas as pd

from helpers.utils import read_input, save_output_to_csv, cleanup_dataframe

# TODO Validate data completness - missing qualifiers games for EL 2014 season


DL_WEIGHT = 1
CLQ_WEIGHT = 3
ELQ_WEIGHT = 3
EL_WEIGHT = 4
CL_WEIGHT = 5


def calculate_weight(df, my_uefa):
    df_ranks = []
    for year in my_uefa["Year"].unique():
        df = my_uefa[my_uefa["Year"] == year]
        df['Weight'] = [(x_i - min(df["Points"])) / (max(df["Points"]) - min(df["Points"])) for x_i in df["Points"]]
        df_ranks.append(df)
    return cleanup_dataframe(pd.concat(df_ranks))


def calculate_score_for_single_cup(teams, cup):
    if cup == "DL":
        teams["Score" + cup] = teams["Weight"] * (
                (3 * teams["Wins" + cup] + 1 * teams["Draws" + cup]) / (teams["MatchesPlayed" + cup] * 3))
    else:
        teams["Score" + cup] = (3 * teams["Wins" + cup] + 1 * teams["Draws" + cup]) / (teams["MatchesPlayed" + cup] * 3)


def calculate_score(teams):
    teams["Score"] = DL_WEIGHT * teams["ScoreDL"] \
                     + EL_WEIGHT * teams["ScoreEL"] \
                     + ELQ_WEIGHT * teams["ScoreELQ"] \
                     + CLQ_WEIGHT * teams["ScoreCLQ"] \
                     + CL_WEIGHT * teams["ScoreCL"]


def run():
    teams_full_record = cleanup_dataframe(read_input("teams_full_record"))
    my_uefa = read_input("uefa_ranking")

    weight = calculate_weight(teams_full_record, my_uefa)

    teams_full_record = teams_full_record.merge(weight,
                                                how="left",
                                                left_on=["Country", "Year"],
                                                right_on=["Country", "Year"])

    calculate_score_for_single_cup(teams_full_record, "EL")
    calculate_score_for_single_cup(teams_full_record, "CL")
    calculate_score_for_single_cup(teams_full_record, "ELQ")
    calculate_score_for_single_cup(teams_full_record, "CLQ")
    calculate_score_for_single_cup(teams_full_record, "DL")

    teams_full_record.replace(np.nan, 0, inplace=True)

    calculate_score(teams_full_record)

    save_output_to_csv(teams_full_record, "teams_score")
