from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .fetch_page import get_computer_page


def get_tablet_page(url: str, parser="lxml"):
    try:
        tablet_page_url = get_computer_page(url).select_one(
            "ul#side-menu li.nav-item:nth-of-type(2) ul.nav.nav-second-level li.nav-item:nth-of-type(2) a"
        )["href"]
        tablet_page = requests.get(urljoin(url, tablet_page_url))
        tablet_page_parser = BeautifulSoup(tablet_page.text, parser)
        return tablet_page_parser
    except Exception as e:
        print(f"Error get tablet page: {e}")


def parse_tablet(url, parser="lxml") -> list[dict]:
    data: list[dict] = []

    # get item
    all_tablet = get_tablet_page(url).select(
        "div.container.test-site div.row div.col-lg-9 div.row div.col-md-4.col-xl-4.col-lg-4"
    )

    for item in all_tablet:
        try:
            item_url = item.select_one('a[itemprop= "name"]')["href"]
            item_page = requests.get(urljoin(url, item_url))
            item_parser = BeautifulSoup(item_page.text, parser)
        except Exception as e:
            print(f"Error access item page: {e}")

        # extract data
        try:
            # name
            item_name = item_parser.select_one('h4[itemprop="name"]').text.strip()

            # price
            item_price = (
                item_parser.select_one('span[itemprop="price"]')
                .text.replace("$", "")
                .strip()
            )

            # memory
            item_memory = []
            memory_list = item_parser.select_one("div.swatches")
            memory_option = memory_list.find_all("button")
            for index in memory_option:
                index = index.text
                item_memory.append(index)

            # review
            item_review = item_parser.select_one('span[itemprop="reviewCount"]').text

            # rating
            item_rating = len(item_parser.select("span.ws-icon.ws-icon-star"))

            # add data
            if item_name and item_price and item_memory and item_review and item_rating:
                data.append(
                    {
                        "Name": item_name,
                        "Type": "Tablet",
                        "Price": float(item_price),
                        "HDD": item_memory,
                        "Total_Review": int(item_review),
                        "Rating": item_rating,
                    }
                )

            else:
                print("Data N/A.")
        except Exception as e:
            print(f"Error extract data: {e}")
            return None

    print("Getting tablet data success!")
    return data


parse_tablet("https://webscraper.io/test-sites/e-commerce/allinone")
