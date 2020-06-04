# Reference: https://docs.streamlit.io/en/latest/getting_started.html
# Importing Libraries
import streamlit as st  # creating web-app
import psycopg2  # accessing data
import pandas as pd  # managing data
import numpy as np  # managing data for model
import pickle  # Importing serialized model for prediction


# Accessing Data (local)
#@st.cache  # Use this to prevent the data from being reloaded every single time

def get_analysis_data():
    dbname = "freelance_db"
    username = "Metaverse"
    pswd = "Arcifice91"

    con = None
    con = psycopg2.connect(database=dbname, user=username,
                           host='localhost', password=pswd)

    sql_query = """SELECT * FROM analysis_table;"""
    analysis_dt = pd.read_sql_query(sql_query, con)
    analysis_dt = analysis_dt
    return analysis_dt


try:
    data = get_analysis_data()
except:
    st.write("Error getting the data!")

# Importing model


def get_model():
    filename = '/Users/Metaverse/Desktop/Insight/projects/myrate/scripts/finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model


try:
    model = get_model()
except:
    st.write("There doesn't seem to be a model to use . . .")

# Web-app to predict hourly rate


def estimate_hourly_rate():
    user_data = data.drop(['hourly_rate', 'index'],
                          axis=1).iloc[0, 0:].tolist()
    user_data = np.array(user_data)
    pred = model.predict(user_data.reshape(1, -1))
    return pred


try:
    your_rate = estimate_hourly_rate()
    st.write(round(your_rate[0]))
except:
    st.write("Something broke . . .")

# Come up with 3-5 sentences and send it around
