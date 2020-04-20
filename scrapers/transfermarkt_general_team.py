def teams_list(page_content):
    teams = page_content.findAll('td', {'class': 'hauptlink no-border-links show-for-small show-for-pad'})
    teams_names = [t.text for t in teams]
    teams_links = [t.find('a').get('href') for t in teams]
    return teams_names, teams_links


def teams_age(page_content):
    teams_age = page_content.findAll('td', {'class': 'zentriert hide-for-small hide-for-pad'})
    return [t.text for t in teams_age][1:]


def abroad_players(page_content):
    teams_abroad = page_content.findAll('td', {'class': 'zentriert hide-for-pad hide-for-small'})
    return [t.text for t in teams_abroad][1:]


def team_market_value(page_content):
    teams_market_value = page_content.findAll('td', {'class': 'rechts show-for-small show-for-pad nowrap'})
    teams_market_value_single_difference = [t.text for t in teams_market_value][2:]
    teams_market_value_single = teams_market_value_single_difference[::2]
    teams_market_difference_value_single = teams_market_value_single_difference[1::2]
    return teams_market_value_single, teams_market_difference_value_single
