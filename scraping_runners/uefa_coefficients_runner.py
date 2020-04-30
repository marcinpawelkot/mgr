import pandas as pd

from helpers.utils import cleanup_dataframe, save_output_to_csv, save_list_to_csv
from runner_base import RunnerBase
from scrapers.uefa_country_coefficients import uefa_country_rankings


class UefaCoefficients(RunnerBase):
    """
    Class to run scraping UEFA coefficients page.
    """
    _URL_UEFA = 'https://en.competitions.uefa.com/memberassociations/uefarankings/country/libraries//years/'
    _SIMILAR_LEAGUES_RANKING_RANGE = 5

    def keep_similar_leagues(self, uefa_ranking):
        polish_league_ranking = uefa_ranking.loc[uefa_ranking['Country'] == 'Poland'].index
        leagues_rankings = []
        for ranking in polish_league_ranking:
            leagues_rankings.append(list(
                range(ranking - self._SIMILAR_LEAGUES_RANKING_RANGE, ranking + self._SIMILAR_LEAGUES_RANKING_RANGE)))
        flat_rankings = [ranking for season_rankings in leagues_rankings for ranking in season_rankings]
        similar_leagues = uefa_ranking.loc[flat_rankings, 'Country'].unique()
        return uefa_ranking[uefa_ranking['Country'].isin(similar_leagues)]

    def run_uefa_coeff(self):
        uefa_rankings = []
        for season_ranking in range(self.SEASON_START, self.SEASON_END + 1):
            page_content = self.scrape_page(url=self._URL_UEFA, suffix=str(season_ranking))
            uefa_rankings.append(uefa_country_rankings(page_content, season_ranking))
        uefa_ranking_all_seasons = cleanup_dataframe(pd.concat(uefa_rankings))
        uefa_ranking_similar_leagues = self.keep_similar_leagues(uefa_ranking_all_seasons)
        similar_leagues = pd.unique(uefa_ranking_similar_leagues["Country"])
        return uefa_ranking_similar_leagues, similar_leagues

    def run(self):
        uefa_ranking_similar_leagues, similar_leagues = self.run_uefa_coeff()
        save_output_to_csv(output=uefa_ranking_similar_leagues, filename="uefa_ranking")
        save_list_to_csv(output=similar_leagues, filename="similar_leagues")
