import numpy as np

from helpers.utils import cleanup_dataframe, save_output_to_csv
from runner_base import RunnerBase
from scrapers.uefa_european_cups import *


class UefaEuropeanCups(RunnerBase):
    """
    Class to run scraping UEFA coefficients page.
    """
    _URL_UEFA_CLUBS_TABLE = 'https://en.competitions.uefa.com/memberassociations/uefarankings/club/libraries//years/'
    _URL_UEFA_CUPS_RESULT = 'https://www.uefa.com/teamsandplayers/teams/club='
    _SIMILAR_LEAGUES_RANKING_RANGE = 5

    def collect_uefa_clubs_ids(self):
        ids = []
        for season in range(self.SEASON_START, self.SEASON_END):
            page_content = self.scrape_page(self._URL_UEFA_CLUBS_TABLE, str(season))
            ids.append(uefa_ids(page_content))
        ids = pd.concat(ids).drop_duplicates()
        return cleanup_dataframe(ids)

    def collect_european_cups_record(self):
        european_cup, empty = [], []
        clubs_ids = self.collect_uefa_clubs_ids()
        for club_id in clubs_ids["UefaId"]:
            try:
                european_cup.append(results_table(self._URL_UEFA_CUPS_RESULT, club_id))
            except:
                empty.append(club_id)

        missing_uefa_ids = clubs_ids[clubs_ids['Team'].isin(empty)].reset_index(drop=True)
        save_output_to_csv(missing_uefa_ids, "missing_uefa_ids")
        european_cup = pd.concat(european_cup)
        european_cup = european_cup.merge(clubs_ids, how="left", left_on="UefaId", right_on="UefaId")
        return european_cup

    def relevant_seasons(self, all_seasons):
        all_seasons = all_seasons[all_seasons["Competition"].isin(["UEFA Europa League", "UEFA Champions League"])]
        return all_seasons[(all_seasons['Season'].str[:4].astype(int) >= self.SEASON_START) & (
                all_seasons['Season'].str[:4].astype(int) < self.SEASON_END)]

    def map_countries_codes_to_full_names(self, european_cups_record):
        countries_map = countries_codes()
        european_cups_record['Country'] = european_cups_record['CountryCode'].map(countries_map)
        return european_cups_record[european_cups_record['Country'].isin(self.similar_leagues())]

    def format_european_cups_record(self, european_cups_record):
        european_cups_record = european_cups_record.replace(np.nan, '', regex=True)
        european_cups_record = self.relevant_seasons(european_cups_record)
        european_cups_record = self.map_countries_codes_to_full_names(european_cups_record)
        european_cups_record['Year'] = european_cups_record['Season'].str[:4].astype(int)
        european_cups_record['Stage'] = european_cups_record['Stage'] + european_cups_record['Stage reached']
        european_cups_record.rename(columns={"P": "MatchesPlayed", "W": "Wins", "D": "Draws", "L": "Losses"},
                                    inplace=True)
        return european_cups_record[
            ["Country", "Team", 'Year', 'UefaId', 'Competition', 'Stage', 'MatchesPlayed', 'Wins', 'Draws',
             'Losses']]

    def run(self):
        european_cups_record = self.format_european_cups_record(self.collect_european_cups_record())
        save_output_to_csv(output=european_cups_record, filename="european_cups_record")
