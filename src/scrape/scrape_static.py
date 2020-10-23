# # Packages for Scraping
from bs4 import BeautifulSoup
import requests
import random

# Packages for cleaning Data
import re
import pandas as pd
import numpy as np
import time
import itertools

# Packages for PostgreSQL Import
import os


class FreelanceScrape:

    def __init__(self, freelancer):
        self.freelancer = freelancer

    def header_content_extraction(self):
        """
        Extract header and content tags for a given freelancer.
        Input is a list of freelancers

        Returns a list of a header and content of freelancers.
            header: contains un-processed information on name, url, location
            content: contains un-processed information on skills, rate, description
        """
        self.header = self.freelancer.div
        self.content = self.freelancer.div.next_sibling.next_sibling

    def header_data_extract(self):
        """
        Extract data from the header for a given freelancer.

        Returns the following data in a dictionary:
            - profile url
            - city
            - state
            - country
        """
        profile_url = self.header.a['href']
        city = self.header.find(
            'span', class_="freelancerAvatar__location--city").string.replace(',', '')
        state = self.header.find(
            'span', class_="freelancerAvatar__location--state").string.replace(',', '')
        country = self.header.find(
            'span', class_="freelancerAvatar__location--country").string
        try:
            earnings = self.header.find(
                'span', class_="earnings__amount").text
        except:
            earnings = "NA"

        # Saving into a dictionary. This will later be combined with the content dict.
        header_data = {"profile_url": profile_url, "city": city,
                       "state": state, "country": country, "earnings": earnings}

        self.header_dataframe = header_data

    def content_data_extract(self):
        """
        Extracting data from the content
        x is the content tag for a given freelancer

        Returns the following data in a dictionary:
            - Rates
            - User Header Description
            - Skills list
        """

        rate = self.content.find('p', class_="serviceListing__rates").string
        user_description = self.content.find(
            'h2', class_="serviceListing__title").get_text()
        skills = self.content.find_all(
            'a', class_="skillsList__skill skillsList__skill--hasHover")

        # Cleaning skills_list from messy html list to list of clean strings
        # The lambda lambda function is applying a function to each element in the list.
        # There may be a better way to do this? All in one line? List comprehension?
        def string_clean(skills): return skills.string
        skills = list(map(string_clean, skills))

        # Cleaning rates
        p = re.compile(r'\d+')
        result = p.findall(rate)
        rate = int(result[0])  # First number is always hourly rate

        # Cleaning user description of indents and return
        user_description = user_description.replace('\t', '')
        user_description = user_description.replace('\r', '')
        user_description = user_description.replace('\n', '')

        # Creating Dictionary. This will be combined with header.
        content_data = {"hourly_rate": rate, "skills_list": skills,
                        "user_description": user_description}

        self.content_dataframe = content_data


class GuruScraper:

    def __init__(self):
        pass

    def generate_urls(self, startPage=1, endPage=100):
        """
        This creates a list of urls which can be iterated over and scraped.
        """
        html_core = "https://www.guru.com/d/freelancers/l/united-states/pg/"
        pg_nums = list(map(str, list(range(startPage, endPage))))
        tmp = [s + "/" for s in pg_nums]
        htmls = [html_core + s for s in tmp]

        self.htmls = htmls
        self.totalpages = endPage

    def html_extract(self):
        """
        Extracts and cleans the html from a website (x)

        Returns soup object from beautiful soup
        """

        print("Extracting html data ... \n")
        soups = []
        for i, url in enumerate(self.htmls):
            if i % 2 == 0:
                print('Progress: ' + str((i / self.totalpages) * 100) + '% ...')
            source = requests.get(url).text
            soups.append(BeautifulSoup(source, 'html.parser'))
        self.soup = soups
        print("Extracted all htmls. \n")

    def freelancer_extraction(self):
        """
        Extracts freelancer information from a soup object returned by html_extract.

        Returns a list of lists where each sub-list is a page of freelancers
        """

        freelancers = []
        for i, soup_data in enumerate(self.soup):
            # extracts the section that contains the freelancer data and their data
            users = soup_data.body.form.main.main.section.find_all('ul')[1]
            freelancers.append(users.find_all('div', class_="record__details"))

        # Flattening freelancers from list of lists to list
        flat_list = []
        for sublist in freelancers:
            for item in sublist:
                flat_list.append(item)
        print(len(flat_list))
        self.freelancers = flat_list

    def data_extraction(self, path="data/raw/"):
        scraped_data = []

        print("Extracting user data ...")
        for j, value in enumerate(self.freelancers):
            if j % 20 == 0:
                print('Progress: ' + str((j / len(self.freelancers)) * 100) + '%...')

            freelancer = FreelanceScrape(value)

            freelancer.header_content_extraction()
            freelancer.header_data_extract()
            freelancer.content_data_extract()

            # # Extract two boxes of interest
            header = freelancer.header_dataframe
            content = freelancer.content_dataframe

            # # Combine into one dictionary
            header.update(content)
            scraped_data.append(header)

        dt = pd.DataFrame(scraped_data)
        filename = "./" + path + "freelancers.csv"
        dt.to_csv(filename)

        print("Static scrape completed.")
