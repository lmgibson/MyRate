import os
import pandas as pd
from airtable import Airtable
from datetime import date
import json


class ImportData:

    def __init__(self):
        """
        Converts data to a dictionary that can be batch uploaded to an
        airtable database.
        """
        # Loading data into python
        today = date.today().strftime("%d%m%Y")
        filename = "./data/processed/user_data_" + today + ".json"
        with open(filename) as f:
            records = json.load(f)

        # Uploading Data
        api_key = os.environ['AIRTABLE_API_KEY']
        base_key = os.environ['AIRTABLE_FREELANCE_BASE_KEY']
        table_name = 'freelancers'
        airtable = Airtable(base_key, table_name, api_key)

        airtable.batch_insert(records)
