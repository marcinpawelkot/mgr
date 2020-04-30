import pandas as pd

from helpers.utils import save_output_to_csv, read_input, cleanup_dataframe
from runner_base import RunnerBase
from scrapers.transfermarkt_detailed_team import *


class TransfermarktDetailedClubs(RunnerBase):
    URL_BASE = 'https://www.transfermarkt.com'

    def details_clubs_links(self):
        return list(read_input("teams_general")["Link"])

    def collect_details(self, page_content, link):
        club = basic_club_info(page_content, link)
        club.squad_size = get_squad_size(page_content)
        club.balance = balance_info(page_content)
        page_content = self.scrape_page(self.URL_BASE, link.replace('startseite', 'transferrekorde'))
        club.top_arrival = transfers_info(page_content)
        page_content = self.scrape_page(self.URL_BASE, link.replace('startseite', 'rekordabgaenge'))
        club.top_departure = transfers_info(page_content)
        return club

    def detailed_info_teams(self):
        links = self.details_clubs_links()
        detailed_top_tier_teams = []
        for link in links:
            page_content = self.scrape_page(self.URL_BASE, link)
            detailed_top_tier_teams.append(pd.DataFrame(self.collect_details(page_content, link).to_dict(), index=[0]))

        return cleanup_dataframe(pd.concat(detailed_top_tier_teams))

    def run(self):
        teams = self.detailed_info_teams()
        save_output_to_csv(output=teams, filename="teams_detailed")
