import pandas as pd

CSV_FILES_PATH = "../csv/"
SEASON_START = 2009
SEASON_END = 2019


def read_input(filename, header=0):
    return pd.read_csv(CSV_FILES_PATH + filename + ".csv", sep="|", header=header)


def save_output_to_csv(output, filename):
    output.to_csv(CSV_FILES_PATH + filename + ".csv", sep="|", index=False)


def calculate_playoff_record(record, cup):
    record["Wins" + cup] = record["AllWins" + cup] - record["Wins" + cup + "Q"]
    record["Draws" + cup] = record["AllDraws" + cup] - record["Draws" + cup + "Q"]
    record["Losses" + cup] = record["AllLosses" + cup] - record["Losses" + cup + "Q"]
    return record


def calculate_matches_played(record, cup):
    record["MatchesPlayed" + cup] = record["Wins" + cup] + record["Draws" + cup] + record["Losses" + cup]
    return record

cl_qualifiers = read_input("cl_qualifiers")
el_qualifiers = read_input("el_qualifiers")
