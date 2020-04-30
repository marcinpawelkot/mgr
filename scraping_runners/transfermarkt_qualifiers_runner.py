import pandas as pd

from helpers.utils import cleanup_dataframe, save_output_to_csv
from runner_base import RunnerBase
from scrapers.transfermarkt_qualifiers import european_cup_qualifiers, first_game_result


class TransfermarktQualifiers(RunnerBase):
    URL_CL_QUALIFIERS = 'https://www.transfermarkt.com/uefa-champions-league-qualifying/startseite/pokalwettbewerb/CLQ?saison_id='
    URL_EL_QUALIFIERS = 'https://www.transfermarkt.com/europa-league-qualifying/startseite/pokalwettbewerb/ELQ?saison_id='
    URL_BASE = 'https://www.transfermarkt.com'

    def qualifiers_results(self, cup):
        qualifiers = []
        for season in range(self.SEASON_START, self.SEASON_END + 1):
            page_content = self.scrape_page(cup, str(season))
            qualifiers.append(european_cup_qualifiers(page_content, season))

        return pd.concat(qualifiers)

    def get_first_game_result(self, qualifiers):
        games_with_penalties = qualifiers['Result'].str.contains('pens')
        first_game = []
        for link in qualifiers.loc[games_with_penalties, "MatchSheet"]:
            page_content = self.scrape_page(self.URL_BASE, link)
            first_game.append(first_game_result(page_content))
        qualifiers["FirstGame"] = ""
        qualifiers.loc[games_with_penalties, "FirstGame"] = first_game
        return qualifiers
        

    def run(self):
        cl_qualifiers = cleanup_dataframe(self.qualifiers_results(self.URL_CL_QUALIFIERS))
        el_qualifiers = cleanup_dataframe(self.qualifiers_results(self.URL_EL_QUALIFIERS))

        cl_qualifiers = self.get_first_game_result(cl_qualifiers)
        el_qualifiers = self.get_first_game_result(el_qualifiers)

        save_output_to_csv(output=cl_qualifiers, filename="cl_qualifiers")
        save_output_to_csv(output=el_qualifiers, filename="el_qualifiers")
