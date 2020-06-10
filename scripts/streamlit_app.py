# Reference: https://docs.streamlit.io/en/latest/getting_started.html
# Importing Libraries
import streamlit as st  # creating web-app
import pandas as pd  # managing data
import numpy as np  # managing data for model
import pickle  # Importing serialized model for prediction
from nltk.corpus import stopwords  # Cleaning text data

# Function to create input matrix


def model_input_cols():
    cols = ['num_skills', 'bio_length', 'bio_word_count', 'avg_word_length', 'num_stop',
            'Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
            'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Idaho', 'Illinois',
            'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
            'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
            'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
            'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
            'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
            'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
            'administrative & secretarial', 'business & finance', 'design & art', 'education & training',
            'engineering & architecture', 'legal', 'programming & development', 'sales & marketing',
            'writing & translation']
    col_dict = dict.fromkeys(cols, 0)

    return col_dict


# Functions to clean bio data


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


def num_stopwords(bio):
    stop = stopwords.words('english')

    try:
        res = len([x for x in bio.split() if x in stop])
    except:
        res = -1

    return res


# Function to upload model


def get_model():
    # Tries the location for the hosted server first. Then tries local.
    try:
        filename = '/home/ubuntu/MyRate/scripts/finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
    except:
        filename = '/Users/Metaverse/Desktop/Insight/projects/myrate/scripts/finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))

    return loaded_model


# Code to estimate hourly rate


def estimate_hourly_rate():
    # Now Updating Values
    cols['num_skills'] = 5
    cols['bio_length'] = bio_length
    cols['bio_word_count'] = bio_word_count
    cols['avg_word_length'] = bio_avg_word_length
    cols['num_stop'] = bio_num_stop

    # Updating
    cols[state] = 1
    for i, val in enumerate(skill_categories):
        cols[val.lower()] = 1

    example = np.array(list(cols.values()))
    pred = model.predict(example.reshape(1, -1))

    return pred


# Setting up the Interactive Web-App
# Welcome Splash
st.markdown("**Hourly Rate Estimator:** Welcome! Enter your information below and I'll estimate what your hourly rate should be.")

# State select box
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

# Category Select Box
skill_categories = st.multiselect(
    label='What types of services are you offering?',
    options=["Select one", 'Administrative & Secretarial',
             'Business & Finance', 'Design & Art',
             'Education & Training', 'Engineering & Architecture', 'Legal',
             'Programming & Development', 'Sales & Marketing', 'Writing & Translation']
)

# Bio Entry
bio = st.text_area(label="What is your background?",
                   value="Enter your bio here.")

# Analyzing user inputted data
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

# Creating input matrix
try:
    cols = model_input_cols()
except:
    st.write("I broke trying to create input dataframe")

# Importing Model
model = get_model()

# try:
#     model = get_model()
# except:
#     st.write("There doesn't seem to be a model to use . . .")

# Web-app to predict hourly rate


if st.button("Estimate Hourly Rate"):

    try:
        your_rate = estimate_hourly_rate()
        st.write("We recommend an hourly rate of", round(your_rate[0]), "$")
    except:
        st.write("Something Broke")

else:
    st.write("Put your inputs in above!")


# Come up with 3-5 sentences and send it around
