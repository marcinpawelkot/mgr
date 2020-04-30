from helpers.utils import read_input, save_output_to_csv


def calculate_playoff_record(record, cup):
    record["Wins" + cup] = record["WinsAll" + cup] - record["Wins" + cup + "Q"]
    record["Draws" + cup] = record["DrawsAll" + cup] - record["Draws" + cup + "Q"]
    record["Losses" + cup] = record["LossesAll" + cup] - record["Losses" + cup + "Q"]


def calculate_matches_played(record, cup):
    record["MatchesPlayed" + cup] = record["Wins" + cup] + record["Draws" + cup] + record["Losses" + cup]
    return record


def run():
    teams_dl_uefa_qualifiers_record = read_input("teams_dl_uefa_qualifiers_record")

    calculate_playoff_record(teams_dl_uefa_qualifiers_record, "CL")
    calculate_playoff_record(teams_dl_uefa_qualifiers_record, "EL")

    calculate_matches_played(teams_dl_uefa_qualifiers_record, "CL")
    calculate_matches_played(teams_dl_uefa_qualifiers_record, "EL")
    calculate_matches_played(teams_dl_uefa_qualifiers_record, "CLQ")
    calculate_matches_played(teams_dl_uefa_qualifiers_record, "ELQ")

    # correct mistaken results - Celitc, Legia season CL qualifiers 2015
    teams_dl_uefa_qualifiers_record.loc[695:695, 'WinsCL'] = 0.0
    teams_dl_uefa_qualifiers_record.loc[695:695, 'LossesCL'] = 0.0

    teams_dl_uefa_qualifiers_record.loc[635:635, 'WinsCL'] = 0.0
    teams_dl_uefa_qualifiers_record.loc[635:635, 'LossesCL'] = 0.0

    cols_output = ['Country', 'Year', 'Team', 'Link', 'Value', 'Difference', 'Age',
                   'AbroadPlayers', 'StadiumCapacity', 'StadiumName', 'SquadSize',
                   'TopArrival', 'TopDeparture', 'IncomeValue', 'ExpenditureValues',
                   'OverallBalance', 'MatchesPlayedDL', 'WinsDL', 'DrawsDL', 'LossesDL',
                   'GoalsScored', 'GoalsAgainst', 'GoalsBalance', 'Points',
                   'Round', 'UefaId', 'TransfermarktId',
                   'CompetitionAllCL', 'StageAllCL',
                   'WinsAllCL', 'DrawsAllCL', 'LossesAllCL', 'MatchesPlayedAllCL',
                   'WinsCLQ', 'DrawsCLQ', 'LossesCLQ', 'MatchesPlayedCLQ',
                   'WinsCL', 'DrawsCL', 'LossesCL', 'MatchesPlayedCL',
                   'CompetitionAllEL', 'StageAllEL',
                   'WinsAllEL', 'DrawsAllEL', 'LossesAllEL', 'MatchesPlayedAllEL',
                   'WinsELQ', 'DrawsELQ', 'LossesELQ', 'MatchesPlayedELQ',
                   'WinsEL', 'DrawsEL', 'LossesEL', 'MatchesPlayedEL']

    save_output_to_csv(teams_dl_uefa_qualifiers_record[cols_output], "teams_full_record")
