import logging
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

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


# Data transformation step
def transform_data(df):
    logging.info("{} - main.transform_data: ".format(datetime.now(), "Transforming data as business requirement..."))
    #print(df)
    # deduplicate in active date
    
    #format datetime column "active_date"
    df['active_date'] = pd.to_datetime(df['active_date'])
    #Sort DF by active_date
    df.sort_values(by=['user_id', 'active_date'], inplace=True)
    
    #df['top_workspace'] = df.groupby('user_id')['workspace_id']
    #add max_activity column
    df['max_activity'] = df.groupby('user_id')['total_activity'].transform('max')
    #create df_maxworkspace
    df_maxworkspace = df.loc[df['total_activity'] == df['max_activity'], ['user_id','workspace_id']].drop_duplicates(subset=['user_id', 'workspace_id'])
    ## create df_longest_streak
    # create streak group
    df = df.drop_duplicates(subset=['user_id', 'active_date'])
    df['date_diff'] = df.groupby('user_id')['active_date'].diff()
    df['streak'] = (df['date_diff'] > pd.Timedelta(days=1)).cumsum()
    logging.info("{} - main.transform_data: {}".format(datetime.now() , "display df before ingestion........."))
    #count active date in same group streak
    max_streaks = df.groupby(['user_id', 'streak'])['active_date'].count()
    df_longest_streak = max_streaks.groupby('user_id').max().reset_index()

    #Combination
    df_merge = df_maxworkspace.merge(df_longest_streak, left_on='user_id', right_on='user_id')
    df_final = df_merge.rename(columns={"workspace_id": "top_workspace", "active_date": "longest_streak"})
    logging.info("{} - main.transform_data: {}".format(datetime.now(), "Done"))
    return df_final
    


def db_connect(hostname='localhost',
                port=5432,
                username='postgres',
                password=None,
                database=None):
    conn_string = f'postgresql://{username}:{password}@{hostname}:{port}/{database}'
    db = create_engine(conn_string)
    conn = db.connect()
    return conn


def sink_data(df, conn, table='user_activity'):
    logging.info("{} - main.data_ingestion: {}".format(datetime.now(), "Importing data into DB..."))
    df.to_sql(table, con=conn, if_exists='replace', index=False)
    conn.close()


def etl(config):
    import os
    path = config['source']
    #path = "resources/data/activity.csv"
    database = config['database']
    table = config['table']
    HOSTNAME = os.getenv('DB_HOSTNAME')
    PORT = int(os.getenv('DB_PORT'))
    USERNAME = os.getenv('DB_USERNAME')
    conn = db_connect(
            hostname=HOSTNAME,
            port=PORT,
            username=USERNAME,
            database=database
        )
    # Steps to process data
    logging.info("{} - main.etl: {}".format(datetime.now(), "Start to process data"))
    df_raw = load_data(path)
    df_trans = transform_data(df_raw)
    sink_data(df_trans, conn, table)
    logging.info("{} - main.etl: {}".format(datetime.now(), "End job"))


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, default="/opt/data/activity.csv")
    parser.add_argument("-d", "--database", type=str, default="warehouse")
    parser.add_argument("-t", "--table", type=str, default="user_activity")
    args = parser.parse_args()

    args_output = {
        "source": args.source,
        "database": args.database,
        "table": args.table
    }
    logging.info("{} - main.parse_args: {}".format(datetime.now(), args_output))
    return args_output

if __name__ == '__main__':
    load_config()
    config = parse_args()
    etl(config)
