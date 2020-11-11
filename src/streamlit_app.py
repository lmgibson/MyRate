from airtable import Airtable
import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import date


def loadDatafromAirtable():
    api_key = os.environ['AIRTABLE_API_KEY']
    base_key = os.environ['AIRTABLE_FREELANCE_BASE_KEY']
    table_name = 'freelancers'
    airtable = Airtable(base_key, table_name, api_key)
    return pd.DataFrame.from_records(
        (r['fields'] for r in airtable.get_all()))


def calculateOverallHourlyRate():
    return pandasData.groupby(['date_accessed'])['hourly_rate'].mean()


def convertSkillsStringToList():
    strippedSkillsList = pandasData['skills_list'].str.strip('][')
    splitSkillsList = strippedSkillsList.str.split(', ')
    return splitSkillsList


def filterPandasDataToMostRecentDate():
    today = date.today()
    return pandasData[(pandasData['date_accessed'] == str(today))]


def calculateHourlyRatebySkill():
    pandasData = filterPandasDataToMostRecentDate()
    pandasData['skills_list'] = convertSkillsStringToList()
    print(pandasData)
    explodedPandasData = pandasData.explode('skills_list')
    print(explodedPandasData)
    results = explodedPandasData.groupby(['skills_list'])[
        'hourly_rate'].agg(['mean', 'count'])
    print(results)
    return results.sort_values(by=['count', 'mean'], ascending=False)


st.title("Freelance Hourly Rate Trends")
st.markdown(
    "Welcome! This app provides data and trends of freelancer hourly rates.")
st.markdown(
    "## Trends in overall average hourly rate"
)
pandasData = loadDatafromAirtable()
st.write(calculateOverallHourlyRate())

hourlyRatesBySkill = calculateHourlyRatebySkill()
col1, col2 = st.beta_columns(2)
col1.markdown("## Most popular skills")
col1.write(hourlyRatesBySkill.head(5))
col2.markdown("## Least popular skills")
col2.write(hourlyRatesBySkill.tail(5))

st.markdown("## Average hourly rate by skill category")
st.write(hourlyRatesBySkill)
