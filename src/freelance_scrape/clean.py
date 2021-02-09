# Cleaning Strings
import re
from datetime import datetime

# Utilities
import os

# Packages for Data Management
import pandas as pd
import numpy as np
from datetime import date


class CleanData:
    def __init__(self):

        # Importing Data and cleaning
        user_data = pd.read_csv("./data/raw/freelancers.csv")
        user_data.drop([user_data.columns[0], 'city', 'country', 'state',
                        'earnings', 'user_description'], axis=1, inplace=True)

        today = date.today().strftime("%d/%m/%Y")
        user_data['date_accessed'] = today

        user_data = user_data[['profile_url',
                               'date_accessed', 'hourly_rate', 'skills_list']]
        user_data['profile_url'] = user_data['profile_url'].str.replace(
            '/freelancers/', '')
        user_data['date_accessed'] = pd.to_datetime(
            user_data['date_accessed'], format='%d/%m/%Y')
        user_data['date_accessed'] = user_data['date_accessed'].astype(str)

        # Processed data to CSV
        today = date.today().strftime("%d%m%Y")
        filename = "./data/processed/user_data_" + today + ".csv"
        user_data.to_csv(filename)

        # Processed data to JSON
        filename = "./data/processed/user_data_" + today + ".json"
        user_data.to_json(path_or_buf=filename, orient='records')

    # def merge_data(self):
    #     today = date.today().strftime("%d%m%Y")
    #     clean_data = pd.read_csv("./data/cleaned/user_data.csv")
    #     new_data = pd.read_csv("./data/processed/user_data_" + today + ".csv")

    #     merged_data = clean_data.append(new_data, ignore_index=True)

    #     filename = "./data/cleaned/user_data.csv"
    #     merged_data.to_csv(filename)
