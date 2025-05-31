import logging
import os

import pandas as pd

# logger
logger = logging.getLogger(__name__)


def create_file(laptop_data, tablet_data):
    # prepare path
    current_path = os.path.dirname(__file__)
    data_dir = os.path.join(current_path, "..", "..", "Data")
    csv_path = os.path.join(data_dir, "item.csv")
    json_path = os.path.join(data_dir, "item.json")

    # get data
    try:
        df_laptop = pd.DataFrame(laptop_data)
        df_tablet = pd.DataFrame(tablet_data)

        df_combine = pd.concat([df_laptop, df_tablet])
        df_combine.to_csv(csv_path, index=False)
        df_combine.to_json(json_path, orient="records", indent=4)

        logger.info("Creating file success!")
    except Exception as e:
        logger.error(f"Error creating file: {e}")
