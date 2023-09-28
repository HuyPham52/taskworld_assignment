
import unittest
from get_data import load_data
from postgre_connector import LoadDataFromPostgreSQL
import pandas as pd


class TestScenario(unittest.TestCase):
    
    def test_top_workspace(self):
        user_id = '59c1507a3136e2776dbe00c9'
        df = load_data("resources/data/activity.csv")
        source_value = df[df['user_id'] == user_id].groupby('user_id').max().iloc[0]['workspace_id']
        target_value = LoadDataFromPostgreSQL().extract_data_from_postgre(user_id=user_id).get('top_workspace')[0]
        self.assertEqual(source_value, target_value)

    def test_longest_streak(self):
        user_id = '59c1507a3136e2776dbe00c9'
        df = load_data("resources/data/activity.csv")
        source_df = df[df['user_id'] == user_id]
        source_df['active_date'] = pd.to_datetime(source_df['active_date'])
        source_df = source_df.sort_values(by=['user_id', 'active_date']).drop_duplicates(subset=['user_id', 'active_date'])
        source_df['date_diff'] = source_df.groupby('user_id')['active_date'].diff()
        source_df['streak'] = (source_df['date_diff'] > pd.Timedelta(days=1)).cumsum()
        df_count_date = source_df.groupby(['user_id', 'streak'])['active_date'].count()
        source_value = df_count_date.groupby('user_id').max().reset_index().iloc[0]['active_date']
        target_value = LoadDataFromPostgreSQL().extract_data_from_postgre(user_id=user_id).get('longest_streak')[0]
        self.assertEqual(source_value, target_value)


if __name__ == '__main__':
    unittest.main(verbosity=2)