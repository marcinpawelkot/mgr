from scripts.soccerway import prepare_result_table, leagues_links_soccerway, seasons_in_league, rounds_table, \
    regular_table
from scripts.transfermarkt_detailed_team import get_squad_size, balance_info, transfers_info, basic_club_info
from scripts.transfermarkt_leagues import league_links, top_tier_leagues_links
from scripts.transfermarkt_teams_in_league import teams_list, teams_age, abroad_players, team_market_value, \
    keep_top_tier_teams
from scripts.uefa import uefa_country_rankings, keep_similar_leagues
from scripts.uefa_cups_results import collect_uefa_ids, collect_table
from scripts.utils import prepare_dataframe, scrape_page, match_teams