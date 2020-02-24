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
            balance: Dict = None,
            squad_size: int =None,
            top_arrival=None,
            top_departure=None,

    ):
        self.name = name
        self.stadium_capacity = stadium_capacity
        self.stadium_name = stadium_name
        self.squad_size = squad_size
        self.balance = balance
        self.top_departure = top_departure
        self.top_arrival = top_arrival

    def to_dict(self):
        return {
            'stadium_capacity': self.stadium_capacity,
            'stadium_name': self.stadium_name,
            'squad_size': self.squad_size,
            'top_arrival': self.top_arrival,
            'top_departure': self.top_departure,
            'income_value': self.balance['income_value'],
            'expenditure_values': self.balance['expenditure_values'],
            'overall_balance': self.balance['overall_balance'],
        }


def get_squad_size(page_content):
    lineup = page_content.findAll('td', {'class': 'rechts hauptlink'})
    return len(lineup)


def balance_info(page_content):
    income_value = page_content.findAll('td', {'class': 'greentext rechts'})[0].string
    expenditure_values = page_content.findAll('td', {'class': 'redtext rechts'})[0].string
    try:
        overall_balance = page_content.findAll('td', {'class': 'redtext rechts'})[1].string
    except:
        try:
            overall_balance = page_content.findAll('td', {'class': 'greentext rechts'})[1].string
        except:
            overall_balance = 0

    return dict(income_value=income_value,
                expenditure_values=expenditure_values,
                overall_balance=overall_balance)


def transfers_info(page_content):
    top = page_content.findAll('td', {'class': 'rechts hauptlink'})[0].string
    return top


def basic_club_info(page_content, club_name):
    basic_data = page_content.findAll('div', {'class': 'dataContent'})[0].findAll('span', {'class': 'dataValue'})
    stadium_name = basic_data[4].find('a').string
    stadium_capacity = basic_data[4].find('span').string
    return Club(club_name, stadium_name=stadium_name, stadium_capacity=stadium_capacity)

