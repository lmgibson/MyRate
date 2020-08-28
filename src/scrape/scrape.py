# Packages for Scraping
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
import random

# Packages for cleaning Data
import re
import pandas as pd
import numpy as np
import time

# Packages for PostgreSQL Import
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

# Utilities
import os


# Functions
def extracting_jobs():
    """
    Extracts the job titles on the page

    Returns a clean list of job titles
    """
    job_box = driver.find_element_by_xpath(
        '//*[@id="serviceList"]')

    return job_box


def sel_obj_to_text(sel_ob):
    """
    Takes in a list of selenium objects and extracts text.

    Returns a list of clean text of equal length to input list
    """

    text_list = [x.get_attribute('innerText') for x in sel_ob]

    return text_list


def extracting_data():
    """
    Input selenium object that contains all jobs on a page

    Return dictionary with data
    """
    data = {}

    # Extracting job title
    job_titles_raw = job_box.find_elements_by_xpath(
        '//div/div[2]/div[1]/div[1]/h2/a')
    job_titles = sel_obj_to_text(job_titles_raw)
    data['job_titles'] = job_titles

    # Extracting Pricing String
    price_string_raw = job_box.find_elements_by_xpath(
        '//div/div[2]/div[1]/div[1]/div[2]')
    price_string = sel_obj_to_text(price_string_raw)

    if len(price_string) > 20:
        # It's picking up an empty box sometimes. Dropping that.
        price_string = price_string[1:]

    data['price_string'] = price_string

    # Extracting Main Category
    main_cat_raw = job_box.find_elements_by_xpath(
        '//div/div[2]/div[2]/div[1]/div/span/a[1]')
    main_cat = sel_obj_to_text(main_cat_raw)
    data['main_category'] = main_cat

    # Extracting Sub-Category - This can be missing
    sub_cat_raw = job_box.find_elements_by_xpath(
        '//div/div[2]/div[2]/div[1]/div/span/a[2]')
    sub_cat = sel_obj_to_text(sub_cat_raw)

    if len(sub_cat) < 20:
        try:
            index_to_fill = [i for i, x in enumerate(main_cat) if x == "Other"]
        except:
            print("No other in data")

        try:
            # Insert NA at location of Other in main_cat
            sub_cat.insert(index_to_fill, "NA")
        except:
            # If there are multiple do them one by one. This will do them in order.
            for i, val in enumerate(index_to_fill):
                sub_cat.insert(val, "NA")

    data['sub_category'] = sub_cat

    # Extracting Number of Quotes
    num_quotes_raw = job_box.find_elements_by_xpath(
        '//div/div[2]/div[1]/div[1]/div[1]')
    num_quotes = sel_obj_to_text(num_quotes_raw)

    if len(num_quotes) > 20:
        # Picks up some other junk text
        num_quotes = num_quotes[2:]

    data['num_quotes_str'] = num_quotes

    #print(len(job_titles), len(price_string), len(main_cat), len(sub_cat), len(num_quotes))
    df = pd.DataFrame(data)

    return df


def pagination():
    """
    The website doesn't have a 'next' button to change the page. This creates
    a list that contains the current page numbers at the bottom of the page.
    I use this against the current page number to determine which element to click.
    """
    # Extracting Page Button Locations
    pages_locations = driver.find_elements_by_xpath(
        '//*[@id="ctl00_guB_ulpaginate"]/li')

    # Extracting Text to match with page number
    pages_text = [x.get_attribute('innerText') for x in pages_locations]

    # Figuring out next page index
    next_page_index = pages_text.index(str(current_page)) + 2

    # Setting xpath that will need to be clicked
    xpath_to_click = '//*[@id="ctl00_guB_ulpaginate"]/li[' + \
        str(next_page_index) + ']/a'

    # Changing the page
    driver.find_element_by_xpath(xpath_to_click).click()


driver = webdriver.Firefox()
driver.get("https://www.guru.com/d/jobs/pg/1")

current_page = 1

for j in range(1, 100):
    if j % 20 == 0:

    job_box = extracting_jobs()

    if j == 0:
        data = extracting_data()
    else:
        tmp = extracting_data()
        data = pd.concat([data, tmp], axis=0)

    pagination()
    current_page += 1

driver.close()

# Exporting Data to CSV
filename = os.path.dirname(os.path.dirname(
    os.environ['PWD'])) + '/data/raw/job_data.csv'
data.to_csv(filename)
