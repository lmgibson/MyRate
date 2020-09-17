# Scrape and Clean commands
from scrape import scrape_static as ss
from scrape import scrape_dynamic_oop as sd
from data_cleaning import clean as cl

# Scraping Libraries
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import random

# Utility
import time

# Data Management
import re
import pandas as pd
import numpy as np
import os
from datetime import date

# # Scraping Static Elements
# scraper = ss.GuruScraper()
# scraper.generate_urls(startPage=1, endPage=50)
# scraper.html_extract()
# scraper.freelancer_extraction()
# scraper.data_extraction()


# # Scraping Dynamic Elements
# scraper = sd.GuruDynamicScrape(pgEnd=50)
# i = 1

# while scraper.pgCur <= scraper.pgEnd:
#     print("Scraping page:", scraper.pgCur)
#     scraper.details_about_scrape()
#     scraper.detail_scrape_check()
#     scraper.raw_to_soup()
#     scraper.soups_to_html()
#     scraper.combine_clean_data()
#     scraper.combine_into_dataframe()
#     scraper.pagination()
#     print("Finished scraping page:", (scraper.pgCur - 1), "\n")
#     i += 1
# scraper.close()

# Cleaning data
clean_class = cl.CleanData()
clean_class.merge_data()

print("Scrape and Clean complete")
