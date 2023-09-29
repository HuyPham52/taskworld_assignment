import os
import sqlalchemy
import logging
import pandas as pd


class LoadDataFromPostgreSQL:

    def load_config():
        from dotenv import load_dotenv
        load_dotenv()

    def __init__(self):
        
        self.host = os.getenv('DB_HOSTNAME')
        self.database = 'warehouse'
        self.user = os.getenv('DB_USERNAME')
        self.password = ''

    def innit_postgresql_connection_engine(self):
        engine = sqlalchemy.create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(
                self.user, self.password, self.host, 5432, self.database))
        return engine

    def get_df_from_postgresql_server(self, query):
        engine = self.innit_postgresql_connection_engine()
        df_result = pd.DataFrame()
        try:
            df_result = pd.read_sql(query,engine)
            logging.info(f"------ Get {df_result.shape[0]} rows from Server ------")
            return df_result
        except Exception as err:
            logging.error(f"Error when execute query on Server, error: {err}")
            raise

    def extract_data_from_postgre(self, target_table_name='public.user_activity', user_id=None):
        query = f"SELECT * FROM {target_table_name} WHERE user_id = '%s'" % user_id
        #print(query)
        input_df = self.get_df_from_postgresql_server(query)
        return input_df

    def main(self, target_table_name):
        input_df = self.extract_data_from_postgre(target_table_name=target_table_name)
        return input_df

if __name__ == '__main__':
    obj = LoadDataFromPostgreSQL()
    obj.main(target_table_name='public.user_activity')
