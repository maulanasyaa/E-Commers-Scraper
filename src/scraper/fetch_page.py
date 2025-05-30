from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def fetch_page(url: str, parser="lxml") -> BeautifulSoup:
    try:
        response = requests.get(url)
        print(response.status_code)
        # bs4
        soup = BeautifulSoup(response.text, parser)
        return soup
    except Exception as e:
        print(f"Error request: {e}")


def get_computer_page(url: str, parser="lxml"):
    # get computer page
    try:
        computer_page_url = fetch_page(url).select_one(
            "ul#side-menu li.nav-item:nth-of-type(2) a"
        )["href"]
        computer_page = requests.get(urljoin(url, computer_page_url))
        computer_parser = BeautifulSoup(computer_page.text, parser)
        return computer_parser
    except Exception as e:
        print(f"Error access computer page: {e}")
