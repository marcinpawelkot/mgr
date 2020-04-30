import pandas as pd

from helpers.utils import save_output_to_csv
from runner_base import RunnerBase
from scrapers.transfermarkt_leagues import league_links, top_tier_leagues_links


class TransfermarktLeagues(RunnerBase):
    """
    Class to run scraping Transfermarkt leagues pages.
    """
    URL_TRANSFERMARKT = 'https://www.transfermarkt.com/wettbewerbe/europa/wettbewerbe/'
    URL_BASE_TRANSFERMARKT = 'https://www.transfermarkt.com'

    def similar_leagues_links(self):
        page_content = self.scrape_page(url=self.URL_TRANSFERMARKT)
        all_leagues_links = league_links(page_content)
        similar_leagues = self.similar_leagues()
        return all_leagues_links[all_leagues_links['Country'].isin(similar_leagues)].reset_index(drop=True)

    def similar_leagues_top_tier_links(self):
        similar_leagues_top_tier_links = []
        similar_leagues_links = self.similar_leagues_links()
        for link in similar_leagues_links["Link"]:
            page_content = self.scrape_page(self.URL_BASE_TRANSFERMARKT, link)
            similar_leagues_top_tier_links.append(top_tier_leagues_links(page_content))
        return pd.DataFrame(dict(Country=similar_leagues_links["Country"], Link=similar_leagues_top_tier_links))

    def run(self):
        similar_leagues_top_tier_links = self.similar_leagues_top_tier_links()
        save_output_to_csv(output=similar_leagues_top_tier_links, filename="similar_leagues_top_tier_links")
