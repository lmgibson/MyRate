# Reference: https://docs.streamlit.io/en/latest/getting_started.html
# Importing Libraries
import streamlit as st  # creating web-app
import pandas as pd  # managing data
import numpy as np  # managing data for model
import pickle  # Importing serialized model for prediction
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords  # Cleaning text data
import os
import xgboost as xgb

# Function to create input matrix


def model_input_cols():
    cols = ['num_skills', 'bio_length', 'bio_word_count', 'avg_word_length', 'num_stop',
            'administrative & secretarial', 'business & finance', 'design & art', 'education & training',
            'engineering & architecture', 'legal', 'programming & development', 'sales & marketing',
            'writing & translation', 'Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
            'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
            'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
            'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
            'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico',
            'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
            'Washington', 'West Virginia', 'Wisconsin']

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
    model_xgboost = xgb.Booster({'nthread': 4})  # init model

    try:
        filename = '/home/ubuntu/MyRate/scripts/model_xgb.sav'
        model_xgboost = pickle.load(open(filename, 'rb'))
    except:
        filename = '/Users/Metaverse/Desktop/Insight/projects/myrate/scripts/model_xgb.sav'
        model_xgboost = pickle.load(open(filename, 'rb'))

    return model_xgboost

# Functions to Create Word2Vec Embedding from example bio
# This creates embedding values for a single user.
# It works by looping over every word, estimating it's value, and adding it to the feature vector
# For words not in the vocabulary it will return a vector of zeros.
# After this process we get a matrix that is n_words x 50.
# Finally, we collapse this array along the rows by taking the mean to obtain a single
# 1x50 embedding vector that can be fed into the model.

def average_word_vectors(words, model, vocabulary, num_features):

    feature_vector = np.zeros((num_features,), dtype="float64")
    nwords = 0.

    for word in words:
        if word in vocabulary:
            nwords = nwords + 1.
            feature_vector = np.add(feature_vector, model[word])

    if nwords:
        feature_vector = np.divide(feature_vector, nwords)

    return feature_vector


def averaged_word_vectorizer(corpus, model, num_features):
    vocabulary = set(model.wv.index2word)
    features = [average_word_vectors(tokenized_sentence, model, vocabulary, num_features)
                for tokenized_sentence in corpus]

    return np.mean(pd.DataFrame(np.array(features)), axis=0)


def get_word_embedding():
    # Loading Model
    filename = '/home/ubuntu/MyRate/scripts/model_w2v.sav'
    model_w2v = pickle.load(open(filename, 'rb'))

    tokenized_corpus = word_tokenize(bio)
    embeddings = averaged_word_vectorizer(corpus=tokenized_corpus, model=model_w2v,
                                          num_features=50)

    embeddings.index = [str(x) for x in list(embeddings.index)]
    embeddings = pd.DataFrame(embeddings).iloc[:, 0].to_dict()

    return embeddings


# Code to estimate hourly rate
def create_input_array():
    # Updating Bio Related Features
    cols['num_skills'] = 5
    cols['bio_length'] = bio_length
    cols['bio_word_count'] = bio_word_count
    cols['avg_word_length'] = bio_avg_word_length
    cols['num_stop'] = bio_num_stop
    cols.update(w2v_embedding)

    # Updating Location Feature
    cols[state] = 1
    for i, val in enumerate(skill_categories):
        cols[val.lower()] = 1

    return pd.DataFrame(cols, index=[0])


def estimate_hourly_rate():
    # Predicting
    pred = model.predict(xgb.DMatrix(cols.values))

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

# Extracting Embedding
w2v_embedding = get_word_embedding()


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

# Creating Dataset to Predict On
cols = create_input_array()

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
