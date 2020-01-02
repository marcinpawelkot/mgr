import requests
from bs4 import BeautifulSoup
from typing import Dict
import pandas as pd


class Club:

    def __init__(
            self,
            name: str,
            stadium_capacity: int = None,
            stadium_name: str = None,
            squad: Dict = None,
            transfers: Dict = None,
    ):
        self.name = name
        self.stadium_capacity = stadium_capacity
        self.stadium_name = stadium_name
        self.squad = squad
        self.transfers = transfers

    def to_dict(self):
        return {
            'stadium_capacity': self.stadium_capacity,
            'stadium_name': self.stadium_name,
            'squad_size': self.squad['squad_size'],
            'average_age': self.squad['average_age'],
            'abroad_players': self.squad['abroad_players'],
            'national_players': self.squad['national_players'],
            'income_value': self.transfers['income_value'],
            'expenditure_values': self.transfers['expenditure_values'],
            'overall_balance': self.transfers['overall_balance'],
            'top_departure': self.transfers['top_departure'],
            'top_arrival': self.transfers['top_arrival'],
        }


def squad_info(page_content):
    data_contet = page_content.findAll('div', {'class': 'dataContent'})[0].findAll('span', {'class': 'dataValue'})
    lineup = page_content.findAll('td', {'class': 'rechts hauptlink'})
    squad_size = len(lineup)
    average_age = data_contet[1].string
    #abroad_players = data_contet[2].find('a').string
    national_players = data_contet[3].find('a').string
    return dict(squad_size=squad_size,
                average_age=average_age,
                abroad_players=5,
                national_players=national_players)


def transfers_info(page_content):
    income_value = page_content.findAll('td', {'class': 'greentext rechts'})[0].string
    expenditure_values = page_content.findAll('td', {'class': 'redtext rechts'})[0].string
    try:
        overall_balance = page_content.findAll('td', {'class': 'redtext rechts'})[1].string
    except:
        try:
            overall_balance = page_content.findAll('td', {'class': 'greentext rechts'})[1].string
        except:
            overall_balance = 0

    transfers = page_content.findAll('span', {'class': 'abloese'})
    return dict(income_value=income_value,
                expenditure_values=expenditure_values,
                overall_balance=overall_balance,
                top_departure=transfers[5].text,
                top_arrival=transfers[0].text)


def basic_club_info(page_content, club_name):
    basic_data = page_content.findAll('div', {'class': 'dataContent'})[0].findAll('span', {'class': 'dataValue'})
    stadium_name = basic_data[4].find('a').string
    stadium_capacity = basic_data[4].find('span').string
    return Club(club_name, stadium_name=stadium_name, stadium_capacity=stadium_capacity)


def prepare_dataframe(detailed_teams):
    df = pd.concat(detailed_teams)
    df.replace('^\s+', '', regex=True, inplace=True)
    df.replace('\s+$', '', regex=True, inplace=True)
    return df.reset_index(drop=True)
