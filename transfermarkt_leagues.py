from bs4 import BeautifulSoup
import requests
import pandas as pd

def country_league_links(page_content):
    leagues = page_content.findAll('area', {'shape': 'rect'})
    countries= []
    links = []
    for league in leagues:
        countries.append(league['title'])
        links.append(league['href'])
    return pd.DataFrame(dict(country = countries, link = links))



def top_tier_league_link(page_content):
    all_levels = page_content.findAll('table', {'class': 'inline-table'})[0]
    return all_levels.find_all(href=True)[1].get('href')
