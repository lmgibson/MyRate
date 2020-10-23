import os
import pandas as pd
from airtable import Airtable
from datetime import date


class ImportData:

    def __init__(self):
        """
        Converts data to a dictionary that can be batch uploaded to an
        airtable database.
        """
        today = date.today().strftime("%d%m%Y")
        filename = "./data/processed/user_data_" + today + ".csv"
        df = pd.read_csv(filename)

        # Prepping Data for Upload
        df = df[['profile_url', 'date_accessed', 'hourly_rate']]
        df['profile_url'] = df['profile_url'].str.replace('/freelancers/', '')
        df['date_accessed'] = pd.to_datetime(
            df['date_accessed'], format='%d/%m/%Y')
        df['date_accessed'] = df['date_accessed'].astype(str)

        # Uploading Data
        api_key = os.environ['AIRTABLE_API_KEY']
        base_key = os.environ['AIRTABLE_FREELANCE_BASE_KEY']
        table_name = 'freelancers'
        airtable = Airtable(base_key, table_name, api_key)

        records = df.to_dict(orient='records')
        airtable.batch_insert(records)
