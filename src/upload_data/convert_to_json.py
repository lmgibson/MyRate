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

        # Uploading Data
        api_key = os.environ['AIRTABLE_API_KEY']
        base_key = os.environ['AIRTABLE_FREELANCE_BASE_KEY']
        table_name = 'freelancers'
        airtable = Airtable(base_key, table_name, api_key)

        records = df.to_dict(orient='records')
        airtable.batch_insert(records)
