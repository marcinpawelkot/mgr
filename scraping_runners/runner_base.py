import requests
from bs4 import BeautifulSoup

from helpers.utils import read_list_from_csv, read_input


class RunnerBase:
    """
    Inherited by all runners.
    """
    SEASON_START = 2009
    SEASON_END = 2019
    MINIMUM_SEASON = 10

    def scrape_page(self, url, suffix=""):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url + suffix, headers=headers)
        return BeautifulSoup(response.text, "html.parser")

    def similar_leagues(self):
        return read_list_from_csv("similar_leagues")

    def similar_leagues_top_tier_links(self):
        return read_input("similar_leagues_top_tier_links")
