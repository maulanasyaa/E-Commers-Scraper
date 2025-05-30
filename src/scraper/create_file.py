import os

import pandas as pd

from .parse_laptop import parse_laptop
from .parse_tablet import parse_tablet


def create_file(url):
    # prepare path
    current_path = os.path.dirname(__file__)
    data_dir = os.path.join(current_path, "..", "..", "Data")
    csv_path = os.path.join(data_dir, "item.csv")
    json_path = os.path.join(data_dir, "item.json")

    # # get data
    try:
        df_laptop = pd.DataFrame(parse_laptop(url))
        df_tablet = pd.DataFrame(parse_tablet(url))

        df_combine = pd.concat([df_laptop, df_tablet])
        df_combine.to_csv(csv_path, index=False)
        df_combine.to_json(json_path, orient="records", indent=4)

        print("Creating file success!")
    except Exception as e:
        print(f"Error creating file: {e}")
