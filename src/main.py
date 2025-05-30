import os
import time

from dotenv import load_dotenv

from scraper.create_file import create_file
from scraper.parse_laptop import parse_laptop
from scraper.parse_tablet import parse_tablet

# get main url
load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def main(url):
    try:
        print("Getting data..")
        parse_laptop(url)
        time.sleep(3)
        parse_tablet(url)
        time.sleep(3)

        print("Creating file..")
        create_file(url)
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main(BASE_URL)
