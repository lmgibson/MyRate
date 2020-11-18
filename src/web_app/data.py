import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
from airtable import Airtable


class DataAnalysis:

    def __init__(self):
        pass

    def loadDataFromAirtable(self):
        api_key = os.environ['AIRTABLE_API_KEY']
        base_key = os.environ['AIRTABLE_FREELANCE_BASE_KEY']
        table_name = 'freelancers'
        airtable = Airtable(base_key, table_name, api_key)

        self.data = pd.DataFrame.from_records(
            (r['fields'] for r in airtable.get_all()))

    def calculateOverallHourlyRate(self):
        return self.data.groupby(['date_accessed'])['hourly_rate'].mean()

    def calculateHourlyRateBySkill(self):
        self.filteredData = self.filterToMostRecentDate()
        self.filteredData.loc[:,
                              'skills_list'] = self.convertSkillsStringToList()
        self.filteredData = self.filteredData.explode('skills_list')
        results = self.filteredData.groupby(['skills_list'])[
            'hourly_rate'].agg(['mean', 'count'])
        results = results.sort_values(by=['count', 'mean'], ascending=False)
        del self.filteredData
        return results

    def convertSkillsStringToList(self):
        strippedSkillsList = self.filteredData['skills_list'].str.strip('][')
        splitSkillsList = strippedSkillsList.str.split(', ')
        return splitSkillsList

    def filterToMostRecentDate(self):
        mostRecentDate = self.data.date_accessed.max()
        return self.data.loc[self.data['date_accessed'] == mostRecentDate, :]

    def plotTrendsInAverageHourlyRate(self):
        plotData = self.data.groupby(['date_accessed'])['hourly_rate'].mean()
