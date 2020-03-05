import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_page(url, suffix=""):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url + suffix, headers=headers)
    return BeautifulSoup(response.text, "html.parser")

url = 'https://en.competitions.uefa.com/memberassociations/uefarankings/club/libraries//years/2020/'

page_content = scrape_page(url)
body = page_content.findAll('tbody')

for t in body:
    print(t)