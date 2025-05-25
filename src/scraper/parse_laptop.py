from bs4 import BeautifulSoup
from fetch_page import fetch_page


def parse_laptop(url, parser="lxml"):
    # get laptop page
    laptop_page_url = fetch_page(url).select_one(
        "div.wrapper div.container.test-site div.col-lg-3.sidebar div.navbar-light.sidebar div.sidebar-nav.navbar-collapse ul#side-menu li.nav-item a"
    )["href"]
    print(laptop_page_url)


parse_laptop("https://webscraper.io/test-sites/e-commerce/allinone")
