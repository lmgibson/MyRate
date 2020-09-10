# Packages for Scraping
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
# from sqlalchemy import create_engine
# from sqlalchemy_utils import database_exists, create_database
# import psycopg2
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
        header = []
        content = []
        for i, user in enumerate(self.freelancer):
            header.append(user.div)
            content.append(user.div.next_sibling.next_sibling)

        self.header = header
        self.content = content

    def header_data_extract(self):
        """
        Extract data from the header for a given freelancer.

        Returns the following data in a dictionary:
            - profile url
            - city
            - state
            - country
        """
        profile_url = []
        city = []
        state = []
        country = []
        rating = []
        earnings = []

        for i, data in enumerate(self.header):
            # Extracting data
            profile_url.append(data.a['href'])

            city.append(data.find(
                'span', class_="freelancerAvatar__location--city").string.replace(',', ''))
            state.append(data.find(
                'span', class_="freelancerAvatar__location--state").string.replace(',', ''))
            country.append(data.find(
                'span', class_="freelancerAvatar__location--country").string)

            # The feedback section can be missing if a user has never received feedback.
            # This try/except clause prevents sets rating to NA if it is blank.
            try:
                rating.append(data.find(
                    'span', class_="freelancerAvatar__feedback").text)
            except:
                rating.append("NA")

            # Same thing goes for earnings. However, someone may have earnings but not feedback.
            # Therefore, they need to exist in separate try/except clauses.
            try:
                earnings.append(data.find(
                    'span', class_="freelancerAvatar__earnings").text)
            except:
                earnings.append("NA")

        # Saving into a dictionary. This will later be combined with the content dict.
        header_data = {"profile_url": profile_url, "city": city,
                       "state": state, "country": country, "rating": rating,
                       "earnings": earnings}

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

        rates = []
        user_descriptions = []
        skills_list = []

        for i, data in enumerate(self.content):
            # Extracting data from the soup HTML object
            rate = data.find_all('p')[0].string
            user_description = data.find(
                'h2', class_="serviceListing__title").get_text()

            # Skills is a LIST of up to five elements.
            skills = data.find_all(
                'a', class_="skillsList__skill skillsList__skill--hasHover")

            # Cleaning skills_list from messy html list to list of clean strings
            # The lambda lambda function is applying a function to each element in the list.
            # There may be a better way to do this? All in one line? List comprehension?
            def string_clean(skills): return skills.string
            skills_list_strings = list(map(string_clean, skills))

            # Cleaning rates
            p = re.compile(r'\d+')
            result = p.findall(rate)
            hourly_rate = int(result[0])  # First number is always hourly rate

            # Cleaning user description of indents and return

            user_description = user_description.replace('\t', '')
            user_description = user_description.replace('\r', '')
            user_description = user_description.replace('\n', '')

            # Appending results
            rates.append(hourly_rate)
            user_descriptions.append(user_description)
            skills_list.append(skills_list_strings)

        # Creating Dictionary. This will be combined with header.
        content_data = {"hourly_rate": hourly_rate, "skills_list": skills_list,
                        "user_description": user_descriptions}

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
            if i % 10 == 0:
                print('Progress: ' + str((i / self.totalpages) * 100) + '%...')
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
        for i, soup in enumerate(self.soup):
            # extracts the section that contains the freelancer data and their data
            users = soup.body.form.main.main.section.find_all('ul')[1]
            freelancers.append(users.find_all('div', class_="record__details"))
        self.freelancers = freelancers

    def data_extraction(self, path="data/raw/"):
        scraped_data = pd.DataFrame(columns=["profile_url", "city", "state", "country",
                                             "rating", "earnings", "hourly_rate", "skills_list",
                                             "user_description"])

        print("Extracting user data ...")
        for j, value in enumerate(self.freelancers):
            if j % 25 == 0:
                print('Progress: ' + str((j / self.totalpages) * 100) + '%...')

            freelancer = FreelanceScrape(value)

            freelancer.header_content_extraction()
            freelancer.header_data_extract()
            freelancer.content_data_extract()

            # # Extract two boxes of interest
            header = freelancer.header_dataframe
            content = freelancer.content_dataframe

            # # Combine into one dictionary
            header.update(content)
            data = pd.DataFrame(header)
            scraped_data = scraped_data.append(data, ignore_index=True)

        filename = "./" + path + "freelancers.csv"
        scraped_data.to_csv(filename)

        print("Static scrape completed.")
