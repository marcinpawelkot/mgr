import pandas as pd

from runner_base import RunnerBase
from scrapers.transfermarkt_general_team import *
from utils.utils import save_output_to_csv


class TransfermarktClubs(RunnerBase):
    URL_BASE = 'https://www.transfermarkt.com'

    def collect_data_season_league(self, page_content, season, country):
        teams, links = teams_list(page_content)
        age = teams_age(page_content)
        a_players = abroad_players(page_content)
        value, difference = team_market_value(page_content)
        return pd.DataFrame.from_dict(dict(Country=country, Year=season, Team=teams, Link=links, Value=value,
                                           Difference=difference, Age=age, AbroadPlayers=a_players))

    def keep_top_tier_teams(self, teams_per_season_league, minimum_number_of_seasons):
        top_tier_teams = list(teams_per_season_league.groupby(['Team']).count()[
                                  teams_per_season_league.groupby(
                                      ['Team']).count() == minimum_number_of_seasons].dropna().index)
        return teams_per_season_league[teams_per_season_league['Team'].isin(top_tier_teams)].reset_index(drop=True)

    def collect_teams(self):
        similar_leagues_top_tier_links = self.similar_leagues_top_tier_links()

        teams_per_season_league = []
        for row in similar_leagues_top_tier_links.itertuples():
            for season in range(self.SEASON_START, self.SEASON_END):
                page_content = self.scrape_page(self.URL_BASE + row.Link + '/plus/?saison_id=', str(season))
                teams_per_season_league.append(self.collect_data_season_league(page_content, season, row.Country))

        return pd.concat(teams_per_season_league).reset_index(drop=True)

    def run(self):
        teams = self.keep_top_tier_teams(teams_per_season_league=self.collect_teams(),
                                         minimum_number_of_seasons=self.MINIMUM_SEASON)
        save_output_to_csv(output=teams, filename="teams_general")
