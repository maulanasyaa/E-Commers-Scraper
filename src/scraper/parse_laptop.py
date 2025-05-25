import traceback
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from fetch_page import fetch_page


def parse_laptop(url: str, parser="lxml") -> list[dict]:
    data: list[dict] = []

    # get computer page
    try:
        computer_page_url = fetch_page(url).select_one(
            "ul#side-menu li.nav-item:nth-of-type(2) a"
        )["href"]
        computer_page = requests.get(urljoin(url, computer_page_url))
        computer_parser = BeautifulSoup(computer_page.text, parser)
    except Exception as e:
        print(f"Error access computer page: {e}")

    # get laptop page
    try:
        laptop_page_url = computer_parser.select_one(
            "ul#side-menu li.nav-item:nth-of-type(2) ul.nav.nav-second-level li.nav-item a"
        )["href"]
        laptop_page = requests.get(urljoin(url, laptop_page_url))
        laptop_parser = BeautifulSoup(laptop_page.text, parser)
    except Exception as e:
        print(f"Error access laptop page: {e}")

    # get item
    all_laptop = laptop_parser.select(
        "div.container.test-site div.row div.col-lg-9 div.row div.col-md-4.col-xl-4.col-lg-4"
    )

    for item in all_laptop:
        try:
            item_url = item.select_one(
                "div.card.thumbnail div.product-wrapper.card-body div.caption h4 a"
            )["href"]
            item_page = requests.get(urljoin(url, item_url))
            item_parser = BeautifulSoup(item_page.text, parser)
        except Exception as e:
            print(f"Error access item page: {e}")

        # extract data
        try:
            # name
            item_name = item_parser.select_one('h4[itemprop ="name"]').text.strip()

            # price
            item_price = (
                item_parser.select_one('span[itemprop="price"]')
                .text.strip()
                .replace("$", "")
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
                        "Price": item_price,
                        "HDD": item_memory,
                        "Total_Review": item_review,
                        "Rating": item_rating,
                    }
                )
            else:
                print("Data N/A.")

        except Exception as e:
            print(f"Error extract data: {e}")
            print("Detail traceback error:")
            traceback.print_exc()
            return None

    return data
