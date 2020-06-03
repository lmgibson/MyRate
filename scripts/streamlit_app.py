# Reference: https://docs.streamlit.io/en/latest/getting_started.html
# Importing Libraries
import streamlit as st  # creating web-app
import psycopg2  # accessing data
import pandas as pd  # managing data
import time


# Accessing Data (local)
#@st.cache  # Use this to prevent the data from being reloaded every single time
def get_analysis_data():
    dbname = "freelance_db"
    username = "Metaverse"
    pswd = "Arcifice91"

    con = None
    con = psycopg2.connect(database=dbname, user=username,
                           host='localhost', password=pswd)

    # Extract freelance_db as fl_table, don't bring Punjab obs
    sql_query = """SELECT * FROM analysis_table;"""
    analysis_dt = pd.read_sql_query(sql_query, con)
    analysis_dt = analysis_dt
    return analysis_dt


try:
    data = get_analysis_data()
except:
    st.write("Error getting the data!")

# Super simple web-app
st.write("What region do you live in?")

region = st.selectbox(
    "Choose your region", list(
        ['Midwest', "Northeast", "South", "Other", "West"])
)

try:
    your_hourly_rate = round(data[data[region] == 1].hourly_rate.mean(), 2)
    st.write("Your recommended hourly rate ($): ", your_hourly_rate)
except:
    st.write("Please select a region above")
