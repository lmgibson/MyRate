# Reference: https://docs.streamlit.io/en/latest/getting_started.html
# Importing Libraries
import streamlit as st  # creating web-app
import psycopg2  # accessing data
import pandas as pd  # managing data
import numpy as np  # managing data for model
import pickle  # Importing serialized model for prediction
from nltk.corpus import stopwords


# Accessing Example Data (local)
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
    analysis_dt = analysis_dt.drop(
        ['hourly_rate', 'has_rating', 'index', 'rating', 'months_active'], axis=1)

    return analysis_dt.columns


try:
    data_cols = get_analysis_data()
except:
    st.write("Error getting the data!")

# Welcome
st.markdown("**Hourly Rate Estimator:** Welcome! Enter your information below and I'll estimate what your hourly rate should be.")

# State Entry
state = st.selectbox(
    label="What state do you live in?",
    options=['Select a State', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
             'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Idaho',
             'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
             'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
             'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
             'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
             'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
             'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina',
             'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
             'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
)

skill_categories = st.selectbox(
    label='What types of services are you offering?',
    options=["Select one", 'Administrative & Secretarial',
             'Business & Finance', 'Design & Art',
             'Education & Training', 'Engineering & Architecture', 'Legal',
             'Programming & Development', 'Sales & Marketing', 'Writing & Translation']
)

# Bio Entry
bio = st.text_area(label="What is your background?",
                   value="Enter your bio here.")

# Analyzing bio


def clean_bio(bio):
    try:
        cleaned_bio = ''.join(s for s in bio if ord(s) > 31 and ord(s) < 126)
    except:
        cleaned_bio = "NaN"
    return cleaned_bio


def avg_word_ln(bio):
    try:
        words = bio.split()
        res = (sum(len(word) for word in words) / len(words))
    except:
        res = 0
    return res

# Number of stop words


def num_stopwords(bio):
    stop = stopwords.words('english')

    try:
        res = len([x for x in bio.split() if x in stop])
    except:
        res = -1

    return res


bio_clean = clean_bio(bio)
bio_length = len(bio_clean)
bio_avg_word_length = avg_word_ln(bio_clean)
bio_num_stop = num_stopwords(bio_clean)
bio_word_count = len(str(bio_clean).split(" "))


# Hacky way to create empty space
st.text("")
st.text("")

st.text("")
st.text("")

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
    # Creating dictionary
    cols = dict.fromkeys(list(data_cols))

    # Now Updating Values
    cols['num_skills'] = 5
    cols['bio_length'] = bio_length
    cols['bio_word_count'] = bio_word_count
    cols['avg_word_length'] = bio_avg_word_length
    cols['num_stop'] = bio_num_stop
    cols['Alabama'] = 0
    cols['Arizona'] = 0
    cols['Arkansas'] = 0
    cols['California'] = 0
    cols['Colorado'] = 0
    cols['Connecticut'] = 0
    cols['Delaware'] = 0
    cols['District of Columbia'] = 0
    cols['Florida'] = 0
    cols['Georgia'] = 0
    cols['Idaho'] = 0
    cols['Illinois'] = 0
    cols['Indiana'] = 0
    cols['Iowa'] = 0
    cols['Kansas'] = 0
    cols['Kentucky'] = 0
    cols['Louisiana'] = 0
    cols['Maine'] = 0
    cols['Maryland'] = 0
    cols['Massachusetts'] = 0
    cols['Michigan'] = 0
    cols['Minnesota'] = 0
    cols['Mississippi'] = 0
    cols['Missouri'] = 0
    cols['Montana'] = 0
    cols['Nebraska'] = 0
    cols['Nevada'] = 0
    cols['New Hampshire'] = 0
    cols['New Jersey'] = 0
    cols['New Mexico'] = 0
    cols['New York'] = 0
    cols['North Carolina'] = 0
    cols['North Dakota'] = 0
    cols['Ohio'] = 0
    cols['Oklahoma'] = 0
    cols['Oregon'] = 0
    cols['Pennsylvania'] = 0
    cols['Puerto Rico'] = 0
    cols['Rhode Island'] = 0
    cols['South Carolina'] = 0
    cols['South Dakota'] = 0
    cols['Tennessee'] = 0
    cols['Texas'] = 0
    cols['Utah'] = 0
    cols['Vermont'] = 0
    cols['Virginia'] = 0
    cols['Washington'] = 0
    cols['West Virginia'] = 0
    cols['Wisconsin'] = 0
    cols['Wyoming'] = 0
    cols['administrative & secretarial'] = 0
    cols['business & finance'] = 0
    cols['design & art'] = 0
    cols['education & training'] = 0
    cols['engineering & architecture'] = 0
    cols['legal'] = 0
    cols['programming & development'] = 0
    cols['sales & marketing'] = 0
    cols['writing & translation'] = 0

    # Updating
    cols[state] = 1
    cols[skill_categories.lower()] = 1

    example = np.array(list(cols.values()))
    pred = model.predict(example.reshape(1, -1))
    return pred


if st.button("Estimate Hourly Rate"):

    try:
        your_rate = estimate_hourly_rate()
        st.write("We recommend an hourly rate of", round(your_rate[0]), "$")
    except:
        st.write("Something Broke")

else:
    st.write("Put your inputs in above!")


# Come up with 3-5 sentences and send it around
