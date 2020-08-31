# Packages for Scraping
from bs4 import BeautifulSoup
import requests
import random

# Packages for cleaning Data
import re
import pandas as pd
import numpy as np
import time

# Packages for PostgreSQL Import
# from sqlalchemy import create_engine
# from sqlalchemy_utils import database_exists, create_database
# import psycopg2
import os


# Functions
def html_extract(x):
    """
    Extracts and cleans the html from a website (x)

    Returns soup object from beautiful soup
    """
    source = requests.get(x).text
    soup = BeautifulSoup(source, 'html.parser')

    return soup


def freelancer_extraction(x):
    """
    Extracts freelancer information from a soup object returned by html_extract(X)

    Returns a list of freelancers.
    """

    # extracts the section that contains the freelancer data
    a = x.body.form.main.main.section.find_all('ul')[1]

    # Create a list where each element is a freelancer.
    # The element has a number of different tags for each data point.
    b = a.find_all('div', class_="record__details")

    return b


def header_content_extraction(x):
    """
    Extract header and content tags for a given freelancer (x).

    Returns a header and content object.
        header: contains un-processed information on name, url, location
        content: contains un-processed information on skills, rate, description
    """
    header = x.div
    content = x.div.next_sibling.next_sibling

    return header, content


def header_data_extract(x):
    """
    Extract data from the header for a given freelancer.

    Returns the following data in a dictionary:
        - profile url
        - city
        - state
        - country
    """

    # Extracting data
    profile_url = x.a['href']

    city = x.find('span', class_="freelancerAvatar__location--city").string
    state = x.find('span', class_="freelancerAvatar__location--state").string
    country = x.find(
        'span', class_="freelancerAvatar__location--country").string

    # The feedback section can be missing if a user has never received feedback.
    # This try/except clause prevents sets rating to NA if it is blank.
    try:
        rating = x.find('span', class_="freelancerAvatar__feedback").text
    except:
        rating = "NA"

    # Same thing goes for earnings. However, someone may have earnings but not feedback.
    # Therefore, they need to exist in separate try/except clauses.
    try:
        earnings = x.find('span', class_="freelancerAvatar__earnings").text
    except:
        earnings = "NA"

    # Clearning commas off city and state
    city = city.replace(',', '')
    state = state.replace(',', '')

    # Saving into a dictionary. This will later be combined with the content dict.
    header = {"profile_url": profile_url, "city": city,
              "state": state, "country": country, "rating": rating,
              "earnings": earnings}

    return header


def content_data_extract(x):
    """
    Extracting data from the content
    x is the content tag for a given freelancer

    Returns the following data in a dictionary:
        - Rates
        - User Header Description
        - Skills list
    """

    # Extracting data from the soup HTML object
    rates = x.find_all('p')[0].string
    user_description_short = x.find(
        'h2', class_="serviceListing__title").get_text()

    # Skills is a LIST of up to five elements.
    skills_list = x.find_all(
        'a', class_="skillsList__skill skillsList__skill--hasHover")

    # Cleaning skills_list from messy html list to list of clean strings
    # The lambda lambda function is applying a function to each element in the list.
    # There may be a better way to do this? All in one line? List comprehension?
    def string_clean(skills_list): return skills_list.string
    skills_list_strings = list(map(string_clean, skills_list))

    # Cleaning rates
    p = re.compile(r'\d+')
    result = p.findall(rates)
    hourly_rate = int(result[0])  # First number is always hourly rate

    # Cleaning user description of indents and return
    user_description_short = user_description_short.replace('\t', '')
    user_description_short = user_description_short.replace('\r', '')
    user_description_short = user_description_short.replace('\n', '')

    # Creating Dictionary. This will be combined with header.
    content = {"hourly_rate": hourly_rate, "skills_list": skills_list_strings,
               "user_description": user_description_short}

    return content


def add_table_to_db(dataframe, table_name):
    """
    Adds the data to a new table (details_table) in freelance_db.
    inputs:
        - dataframe: data you want to save to the databse
        - table_name: The name you want to give the data in the database.

    Doesn't return anything other than a message of completion.
    """
    dbname = "freelance_db"
    username = os.environ['USER']
    pswd = os.environ['SQLPSWD']

    # Connect to the database and save data to it
    engine = create_engine('postgresql://%s:%s@localhost/%s' %
                           (username, pswd, dbname))
    dataframe.to_sql(table_name, engine, if_exists='replace')

    print("Added data to %s" % (dbname))


def urls_to_scrape():
    """
    This creates a list of urls which can be iterated over and scraped.
    """
    html_core = "https://www.guru.com/d/freelancers/l/united-states/pg/"
    pg_nums = list(map(str, list(range(1, 947))))
    tmp = [s + "/" for s in pg_nums]
    htmls = [html_core + s for s in tmp]

    return htmls


def scrape_static(strtPage=0, endPage=100):
    """
    Putting it all together.
    This function uses all of the above functions to scrape the data.
    The results are dumped into a csv that is saved at myrate/data/raw
    """

    htmls = urls_to_scrape()

    # Initializing empty dataframe to save results into
    df = pd.DataFrame(columns=["profile_url", "city", "state", "country",
                               "rating", "earnings", "hourly_rate", "skills_list",
                               "user_description"])

    # Looping over each URL and applying the functions, defined above,
    # In the order they are written.
    for k, page in enumerate(htmls[strtPage:endPage]):

        soup = html_extract(page)
        freelancers = freelancer_extraction(soup)  # Clean HTML

        if k % 25 == 0:
            print('Progress: ' + str(k / 100) + '%...')

        for j, value in enumerate(freelancers):
            header_content = header_content_extraction(
                value)  # Extract two boxes of interest

            results = header_data_extract(
                header_content[0])  # Extract header data
            content = content_data_extract(
                header_content[1])  # Extract content data
            results.update(content)  # Combine into one dictionary
            results = pd.DataFrame(results)
            df = df.append(results)

    # Save to CSV
    # filename = os.environ['PWD'] + "/data/raw/freelancers.csv"
    filename = "./freelancers.csv"
    df.to_csv(filename)

    print("Completed scraping static elements of freelancer information.")


scrape_static(0, 5)
