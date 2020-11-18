import streamlit as st
from web_app import data

st.set_option('deprecation.showPyplotGlobalUse', False)


data = data.DataAnalysis()
data.loadDataFromAirtable()
overallHourlyRates = data.calculateOverallHourlyRate()
hourlyRatesBySkill = data.calculateHourlyRateBySkill()
plotData = data.plotTrendsInAverageHourlyRate()

st.title("Freelance Hourly Rate Trends")
st.markdown(
    "Welcome! This app provides data and trends of freelancer hourly rates.")
st.markdown(
    "## Trends in overall average hourly rate"
)

st.line_chart(data=overallHourlyRates)
st.write(plt)

col1, col2 = st.beta_columns(2)
col1.markdown("## Most popular skills")
col1.write(hourlyRatesBySkill.head(5))
col2.markdown("## Least popular skills")
col2.write(hourlyRatesBySkill.tail(5))

st.markdown("## Average hourly rate by skill category")
st.write(hourlyRatesBySkill)
