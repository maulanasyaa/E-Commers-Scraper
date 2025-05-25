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
