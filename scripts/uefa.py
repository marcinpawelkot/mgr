import pandas as pd


def uefa_country_rankings(page_content, season):
    countries_table = page_content.findAll('span', {'class': 'team-name visible-md visible-lg'})
    countries = [country.text for country in countries_table]
    points_table = page_content.findAll('td', {'class': 'table_member-points'})
    points = [point.text for point in points_table]
    clubs_table = page_content.findAll('td', {'class': 'table_member-clubs'})
    clubs = [club.text for club in clubs_table]
    return pd.DataFrame(dict(Country=countries, 
                             Points=points, 
                             Clubs=clubs, 
                             Year=season, 
                             Position=list(range(1, len(countries) + 1))))


def similar_leagues(uefa_ranking, distance):
    polish_league_position = uefa_ranking.loc[uefa_ranking['Country'] == 'Poland'].index
    leagues_indices = []
    for position in polish_league_position:
        leagues_indices.append(list(range(position - distance, position + distance)))
    flat_list = [item for sublist in leagues_indices for item in sublist]
    return uefa_ranking.loc[flat_list, 'Country'].unique()
