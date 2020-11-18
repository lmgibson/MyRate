import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
        data = self.data.copy()
        data = self.filterToMostRecentDate(data)
        data.loc[:,
                 'skills_list'] = self.convertSkillsStringToList(data)
        data = data.explode('skills_list')
        data['skills_list'] = data['skills_list'].str.strip("'")
        results = data.groupby(['skills_list'])[
            'hourly_rate'].agg(['mean', 'count'])
        results = results.sort_values(by=['count', 'mean'], ascending=False)
        del data
        return results

    def convertSkillsStringToList(self, data):
        strippedSkillsList = data['skills_list'].str.strip('][')
        splitSkillsList = strippedSkillsList.str.split(', ')
        return splitSkillsList

    def filterToMostRecentDate(self, data):
        mostRecentDate = data.date_accessed.max()
        return data.loc[data['date_accessed'] == mostRecentDate, :]

    def plotTrendsInAverageHourlyRate(self):
        plotData = self.data.copy()
        plotData.loc[:, ['skills_list']
                     ] = self.convertSkillsStringToList(self.data)
        plotData = plotData.explode('skills_list')
        plotData = plotData.groupby(['date_accessed', 'skills_list'])[
            'hourly_rate'].agg(['mean']).reset_index(level=1)
        plotData['skills_list'] = plotData['skills_list'].str.strip("'")
        plotData = plotData.loc[plotData['skills_list'].isin(
            ["Angular", "CSS", "App Development"]), :]
        plotData = plotData.reset_index().pivot(index='date_accessed',
                                                columns='skills_list',
                                                values='mean')

        return plotData
