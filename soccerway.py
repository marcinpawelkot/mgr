import pandas as pd
from bs4 import BeautifulSoup
import requests

def optimize_df(df):
    df.reset_index(inplace=True, drop=True)
    df.drop(df.columns[[0, 11, 12]], axis=1, inplace=True)
    df.drop(df.index[[16, 17]], inplace=True)


def leagues_links(page_content): #tutaj zbieramy linki do poszczegolnych lig
    countries = []
    links = []
    countries_table = page_content.findAll('div', {'class': 'row'})
    for t in countries_table:
        links.append(t.find('a').get('href'))
        countries.append(t.find('a').text)
    return pd.DataFrame(dict(country=countries, link=links))

def seasons_in_league(content):
    countries_league = content.findAll('select', {'name': 'season_id'})
    leagues = BeautifulSoup(str(countries_league))
    seasons = []
    links= []
    for line in leagues.findAll('option'):
        links.append(line['value'])
        seasons.append(line.text)
    return pd.DataFrame(dict(season=seasons, link=links))

def rounds_table(content):
    content = content.findAll('select', {'name': 'round_id'})
    rounds = BeautifulSoup(str(content))
    round_name = []
    round_link = []

    for line in rounds.findAll('option')[:2]:
        round_link.append(line['value'])
        round_name.append(line.text)

    return regular_table(round_link[0]), regular_table(round_link[1])


def regular_table(suffix):
    url = 'https://int.soccerway.com/' + suffix
    return pd.read_html(url,
                        index_col = 0,
                        header=0,
                        attrs = {'class':'leaguetable sortable table detailed-table'})[0]

#
# page_content = scrape_page(url)
# df = prepare_dataframe([leagues_links(page_content)])
# # w df trzymamy linki do wszystkich lig
#
# #na razie sztucznie przedchodzimy do polskiej ligii
# # tutaj logika
# url2 = 'https://int.soccerway.com/national/poland/a155/'
# page_content = scrape_page(url2)
#
# #tutaj zbieramy linki do sezonow!
# df2 = seasons_in_league(page_content)
#
# dfs_regular = []
# dfs_rounds = []
# for link in df2['link']:
#     page_content = scrape_page('https://int.soccerway.com/', link)
#     if  page_content.findAll('select', {'name': 'round_id'}):
#         dfs_rounds.append(rounds_table(page_content))
#     else:
#         dfs_regular.append(regular_table(link))


