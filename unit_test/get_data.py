import logging
from datetime import datetime
import pandas as pd

logging.basicConfig(level=logging.DEBUG)


def load_config():
    from dotenv import load_dotenv
    load_dotenv()


def load_data(path=None):
    """Read data from a file activit.csv with path
        local: ../resources/data/activity.csv
        container: /opt/data/activit.csv
    """
    try:
        logging.info("{} - main.extract_data: {}".format(datetime.now(), "Loading data into DF....."))
        df_in = pd.read_csv(path)
        return df_in
    except Exception as error:
        logging.error("{} - main.extract_data: Exception error when load CSV file {}".format(datetime.now(), error))
        exit()


if __name__ == '__main__':
    text = "Noon"
    print(text)
