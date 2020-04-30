from helpers.utils import cleanup_dataframe, save_output_to_csv
from runner_base import RunnerBase
from scrapers.soccerway import *


class Soccerway(RunnerBase):
    URL_SOCCERWAY = 'https://int.soccerway.com/competitions/'
    URL_SOCCERWAY_SEASON = 'https://int.soccerway.com/'

    def check_empty(self, dfs):
        if dfs:
            return [cleanup_dataframe(pd.concat(dfs))]
        else:
            return []

    def similar_leagues_results_links(self):
        page_content = self.scrape_page(self.URL_SOCCERWAY)
        all_leagues_links = cleanup_dataframe(pd.concat([leagues_links_soccerway(page_content)]))
        return all_leagues_links[
            all_leagues_links['Country'].isin(self.similar_leagues())].reset_index(drop=True)

    def collect_links_particular_seasons(self):
        links_to_particular_seasons = []
        similar_leagues_links = self.similar_leagues_results_links()
        for row in similar_leagues_links.itertuples():
            page_content = self.scrape_page(self.URL_SOCCERWAY_SEASON, row.Link)
            links_to_particular_seasons.append(seasons_in_league(page_content, row.Country))

        return cleanup_dataframe(pd.concat(links_to_particular_seasons))

    def relevant_seasons(self):
        all_seasons = self.collect_links_particular_seasons()
        return all_seasons[(all_seasons['Season'].str[:4].astype(int) >= self.SEASON_START) & (
                all_seasons['Season'].str[:4].astype(int) < self.SEASON_END)]

    def collect_leagues_results(self):
        seasons = self.relevant_seasons()

        dfs_championship, dfs_relegation, dfs_regular, dfs_helpers = [], [], [], []
        for row in seasons.itertuples():
            content = self.scrape_page(self.URL_SOCCERWAY_SEASON, row.Link)
            links_to_rounds = rounds_links(content)
            try:
                if 'Championship Round' in links_to_rounds:
                    championship = result_table(links_to_rounds["Championship Round"])
                    self.add_table_metadata(championship, row.Season[:4], row.Country, "Championship")

                    relegation = result_table(links_to_rounds["Relegation Round"])
                    self.add_table_metadata(relegation, row.Season[:4], row.Country, "Relegation")

                    dfs_championship.append(championship)
                    dfs_relegation.append(relegation)
                else:
                    regular = result_table(row.Link)
                    self.add_table_metadata(regular, row.Season[:4], row.Country, "Regular")

                    dfs_regular.append(regular)
            except:
                helper = result_table(row.Link)
                self.add_table_metadata(helper, row.Season[:4], row.Country, "Helper")

                dfs_helpers.append(helper)

        regulars = self.check_empty(dfs_regular)
        champions = self.check_empty(dfs_championship)
        relegations = self.check_empty(dfs_relegation)
        helpers = self.check_empty(dfs_helpers)

        return self.prepare_result_table(pd.concat(regulars + champions + relegations + helpers))

    def add_table_metadata(self, table, season, country, round_):
        table['Year'] = season
        table['Country'] = country
        table['Round'] = round_

    def prepare_result_table(self, df):
        columns_to_keep = ['Team', 'MP', 'W', 'D', 'L', 'F', 'A', 'D.1', 'P', 'Year', 'Country', 'Round']
        df = df[columns_to_keep]
        columns = ['Team', 'MatchesPlayedDL', 'WinsDL', 'DrawsDL', 'LossesDL', 'GoalsScored', 'GoalsAgainst',
                   'GoalsBalance', 'Points', 'Year', 'Country', 'Round']
        df.columns = columns
        df.dropna(inplace=True)
        df = df[~df.Team.str.contains('|'.join(["UEFA", "Corrections", "Relegation"]))]
        df.reset_index(inplace=True, drop=True)
        return df

    def run(self):
        season_results = self.collect_leagues_results()
        save_output_to_csv(output=season_results, filename="season_results")
