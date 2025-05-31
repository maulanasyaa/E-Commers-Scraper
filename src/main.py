import logging
import os
import time

from dotenv import load_dotenv

from scraper.create_file import create_file
from scraper.parse_laptop import parse_laptop
from scraper.parse_tablet import parse_tablet

# logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# get main url
load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def main(url: str):
    try:
        logging.info("Scraping progress started..")
        laptop_data = parse_laptop(url)
        time.sleep(3)
        tablet_data = parse_tablet(url)
        time.sleep(3)

        logging.info("Data collection complete. Creating files...")
        create_file(laptop_data, tablet_data)
    except Exception as e:
        logging.error(f"Error in main process: {e}", exc_info=True)


if __name__ == "__main__":
    if BASE_URL:
        main(BASE_URL)
    else:
        logging.error("BASE_URL not found. Please set it in your .env file.")
