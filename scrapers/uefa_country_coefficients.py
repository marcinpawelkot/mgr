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
