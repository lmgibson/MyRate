# Reference: https://docs.streamlit.io/en/latest/getting_started.html
# Reference for hosting: https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3
# Importing Libraries
from airtable import Airtable
import streamlit as st  # creating web-app
import pandas as pd  # managing data
import numpy as np  # managing data for model
import os

################################################


# Accessing API
api_key = os.environ['AIRTABLE_API_KEY']
base_key = os.environ['AIRTABLE_FREELANCE_BASE_KEY']
table_name = 'freelancers'
airtable = Airtable(base_key, table_name, api_key)
dt = airtable.get_all(maxRecords=20)
df = pd.DataFrame.from_records((r['fields'] for r in dt))

# Setting up the Interactive Web-App
# Welcome Splash
st.markdown("**Hourly Rate Estimator:** Welcome! Enter your information below and I'll estimate what your hourly rate should be.")
