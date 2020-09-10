# Cleaning Strings
import re
from datetime import datetime

# Utilities
import os

# Packages for Data Management
import pandas as pd
import numpy as np


class CleanData:
    def __init__(self):

        # Importing Data and cleaning
        static = pd.read_csv("./data/raw/freelancers.csv")
        dynamic = pd.read_csv("./data/raw/freelancers_detail.csv")

        static.drop([static.columns[0], 'user_description', 'earnings',
                     'city', 'rating'], axis=1, inplace=True)
        dynamic.drop([dynamic.columns[0], 'employers', 'invoices_paid',
                      'largest_employ'], axis=1, inplace=True)

        # Merging
        user_data = static.merge(dynamic, how="inner", on="profile_url")

        # Creating key features

        def date_convert(member_since):
            try:
                tmp = datetime.strptime(member_since, '%b, %Y')
            except:
                tmp = 'NaN'
            return tmp

        def years_active(date):
            cur_year = datetime.now().year
            try:
                yrs_active = cur_year - date.year
            except:
                yrs_active = 'NaN'

            return yrs_active

        def months_active(date):
            cur_year = datetime.now().year
            cur_month = datetime.now().month

            try:
                mnths_active = (cur_year - date.year) * \
                    12 + (cur_month - date.month)
            except:
                mnths_active = 'NaN'

            return mnths_active

        user_data.member_since = user_data.member_since.str.strip()
        user_data['start_date'] = user_data.member_since.apply(date_convert)
        user_data['years_active'] = user_data.start_date.apply(years_active)
        user_data['months_active'] = user_data.start_date.apply(months_active)

        # Processed data
        filename = "./data/processed/user_data.csv"
        user_data.to_csv(filename)


CleanData()
