# Scrape commands
import scrape_static as ss
import scrape_dynamic_oop as sd

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

# Scraping Static Elements
scraper = ss.GuruScraper()
scraper.generate_urls(startPage=1, endPage=100)
scraper.html_extract()
scraper.freelancer_extraction()
scraper.data_extraction("data/raw/")


# Scraping Dynamic Elements
# scraper = GuruDynamicScrape(pgEnd=2)
# i = 1

# while scraper.pgCur <= scraper.pgEnd:
#     print("Scraping page:", scraper.pgCur)
#     scraper.details_about_scrape()
#     print(scraper.names)
#     # scraper.detail_scrape_check()
#     # scraper.raw_to_soup()
#     # scraper.soups_to_html()
#     # scraper.combine_clean_data()
#     # scraper.combine_into_dataframe()
#     # scraper.pagination()
#     # print("Finished scraping page:", (scraper.pgCur - 1), "\n")
#     i += 1
# scraper.close()
