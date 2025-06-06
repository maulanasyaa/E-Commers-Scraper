import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .fetch_page import get_phone_page

# logger
logger = logging.getLogger(__name__)


def get_touch_page(url: str, parser="lxml") -> BeautifulSoup:
    try:
        touch_page_url = get_phone_page(url).select_one(
            "ul#side-menu li.nav-item:nth-of-type(3) ul.nav.nav-second-level li.nav-item a"
        )["href"]
        touch_page = requests.get(urljoin(url, touch_page_url))
        touch_page_parser = BeautifulSoup(touch_page.text, parser)
        return touch_page_parser
    except Exception as e:
        logger.error(f"Error access touch page: {e}")


def parse_touch(url: str, parser="lxml") -> list[dict]:
    data: list[dict] = []

    # get item
    all_touch = get_touch_page(url).select(
        "div.container.test-site div.row div.col-lg-9 div.row div.col-md-4.col-xl-4.col-lg-4"
    )

    for item in all_touch:
        try:
            item_url = item.select_one("a[itemprop='name']")["href"]
            item_page = requests.get(urljoin(url, item_url))
            item_parser = BeautifulSoup(item_page.text, parser)
        except Exception as e:
            logger.error(f"Error access item page: {e}")

        # extract data
        try:
            # name
            item_name = item_parser.select_one("h4[itemprop='name']").text.strip()
            # price
            item_price = (
                item_parser.select_one("span[itemprop='price']")
                .text.strip()
                .replace("$", "")
            )
            # memory
            item_memory = "-"
            # review
            item_review = item_parser.select_one(
                "span[itemprop='reviewCount']"
            ).text.strip()
            # rating
            item_rating = len(item_parser.select("span.ws-icon.ws-icon-star"))

            # add data
            if item_name and item_price and item_memory and item_review and item_rating:
                data.append(
                    {
                        "Name": item_name,
                        "Type": "Phone",
                        "Price": float(item_price),
                        "HDD": item_memory,
                        "Total_Review": item_review,
                        "Rating": int(item_rating),
                    }
                )
            else:
                logger.info("Data N/A")
        except Exception as e:
            logger.error(f"Error extract data: {e}")
            return None

    logger.info("Getting touch data success!")
    return data
