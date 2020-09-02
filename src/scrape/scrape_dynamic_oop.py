# Scraping Libraries
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Utility
import time

# Data Management
import pandas as pd
import numpy as np
import os

class GuruDynamicScrape:

    def __init__(self, pgStart=1, pgEnd=3):
        print("Starting up webdriver . . .")

        # display = Display(visible=0, size=(800, 600))
        # display.start()

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument("--headless")

        # driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.Firefox()
        driver.get("https://www.guru.com/d/freelancers/l/united-states/pg/1/")

        self.pgCur = pgStart
        self.pgEnd = pgEnd
        self.driver = driver

        print("Webdriver initiated. Beginning scrape procedure \n")

    def login_form_click(self):
        """
        Occasionally the locations of the buttons will break. This updates
        their locations and then clicks them, if it is broken.

        Returns: Nothing. Just clicks the button.
        """

        try:
            login_form[2].click()
        except:
            login_form = self.driver.find_elements_by_xpath(
                '//button[@class="tabControls__button"]')
            login_form[2].click()

    def details_about_scrape(self):
        """
        Purpose:
            - Uses selenium to scrape additional information contained in a sub-menu
            - Clicks the first box, guru throws up a log-in, goes back, opens all the boxes
              and then finishes by extracting all the html from each box.

        Inputs:
            - This takes in a single URL (string) and extracts the HTML for the sub-menus.

        Returns:
            - user_names: profile_url names to identify each user, cleaned string.
            - detail_html: detailed information on their activity on the website, html code.
            - about_html: Bio information, html code.
        """

        first_url = self.driver.current_url
        login_form = self.driver.find_elements_by_xpath(
            '//button[@class="tabControls__button"]')

        # First, checking if the site loaded. If it didn't the code will error out.
        # The reason for this is usually if the site doesn't load than user intervention
        # is required to reset by filling out a captcha.
        if len(login_form) == 0:
            return None

        time.sleep(2)  # Wait to click so everything can load.
        self.login_form_click()

        # Fix for when the website asks for a log-in. Works by checking if the URL has changed
        # and if it has changed it will simply page back. Otherwise it continues on by opening
        # the boxes.
        if self.driver.current_url != first_url:
            time.sleep(2)  # Wait for log-in prompt
            self.driver.back()  # Go back to main page
            time.sleep(1)  # Wait to scrape
            login_form = self.driver.find_elements_by_xpath(
                '//button[@class="tabControls__button"]')
        else:
            self.login_form_click()

        # Every user has 4 buttons. This clicks the 3rd button for each user and opens
        # the sub-menu.
        counter = 2
        for i, val in enumerate(login_form):
            # loop one
            if i == counter:
                login_form[i].click()
                counter += 4

        # Pull elements in the now opened detail boxes
        # Extracts the user_name (for reference and later merging)
        # and extract the locations of the HTML contained within the opened menu.
        user_name = self.driver.find_elements_by_xpath(
            '//h3[@class="freelancerAvatar__screenName"]')
        user_detail = self.driver.find_elements_by_xpath(
            '//div[@class="feedback"]')

        # Extract text from the names and HTML from the details
        # Each is a list of length equal to the number of users on the page
        names = []
        for i, val in enumerate(user_name):
            names.append(val.get_attribute('innerHTML'))

        detail_html = []
        for i, val in enumerate(user_detail):
            detail_html.append(val.get_attribute('innerHTML'))

        # Now we go back and get the information in the fourth button (about) menu.
        counter = 3
        for i, val in enumerate(login_form):
            if i == counter:
                # This gets around the stale form error. However, I think there may be a better way
                # that involves ignoring the error (selenium exception library).
                # See: https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
                try:
                    login_form[i].click()
                    counter += 4
                except:
                    login_form = self.driver.find_elements_by_xpath(
                        '//button[@class="tabControls__button"]')
                    login_form[i].click()
                    counter += 4

        time.sleep(2)

        # Pull elements and then HTML from the fourth menu (about).
        user_about = self.driver.find_elements_by_xpath(
            '//div[@class="profile-about"]')
        about_html = []
        for i, val in enumerate(user_about):
            about_html.append(val.get_attribute('innerHTML'))

        # Return user names, user details HTML, and user about HTML
        self.names = names
        self.detail_html = detail_html
        self.about_html = about_html

        return names, detail_html, about_html

    def detail_scrape_check(self):
        if len(self.about_html) != 20:
            print("Something went wrong. Need to refresh the page.")
            time.sleep(1)
            driver.refresh()
            time.sleep(1)
            self.details_about_scrape()

    def raw_to_soup(self):
        """
        Takes in a list of raw htmls and parses them with BeautifulSoup.

        Returns a list of cleaner HTMLs (soup objects)

        """
        soups_names = []
        soups_details = []
        soups_about = []

        # Check if len of soups is the same
        for i in range(0, len(self.names)):
            soups_names.append(BeautifulSoup(self.names[i], 'html.parser'))
            soups_details.append(BeautifulSoup(
                self.detail_html[i], 'html.parser'))
            soups_about.append(BeautifulSoup(
                self.about_html[i], 'html.parser'))

        self.soup_names = soups_names
        self.soup_details = soups_details
        self.soup_about = soups_about

    def soups_to_html(self):
        # User HTML
        user_htmls = []
        for i, val in enumerate(self.soup_names):
            user_htmls.append(val.a['href'])

        # Details
        values = []
        for i, val in enumerate(self.soup_details):
            values.append(val.find_all('em'))

        def html_to_string(x): return x.string
        values_strings = []
        for i, val in enumerate(values):
            values_strings.append(list(map(html_to_string, val)))

            # Lots of empty details pages. This at least fill in an NA.
            if len(values_strings[i]) == 0:
                values_strings[i].append(["NA", "NA", "NA", "NA", "NA", "NA"])

        # About
        about_vals = []
        for i, val in enumerate(self.soup_about):
            try:
                tmp = val.find_all('pre')[0].text
            except:
                tmp = 'NA'
            about_vals.append(tmp)

        self.user_html = user_htmls
        self.detail_html = values_strings
        self.about_html = about_vals

    def combine_clean_data(self):
        """
        Combines the names and details into a single list of lists.
        Dealing with them separately is difficult to follow so I want to combine them ASAP

        Input:
            - names_list: List of profile names (for identification and merging)
            - details_list: List of lists where nested list is data for a given user
            - about_list: List of bios.

        Returns single list of lists. Where the len of the list is = the number of users, and
        the length of the nested list is equal to the number of data columns.
        """

        for i, val in enumerate(self.detail_html):
            val.insert(0, self.user_html[i])

        for i, val in enumerate(self.detail_html):
            val.insert(len(val), self.about_html[i])

        self.data = self.detail_html

    def combine_into_dataframe(self):
        """
        Convert the details_list returned from combine_clean_data into a pandas
        dataframe.
        """
        # First have to check the lengths of the lists in the list
        # For lists that are not the full length (missing data) I extend
        # it to be equal length. This makes putting it into the pandas data
        # frame easier.
        for i, val in enumerate(self.data):
            val.extend([float("NaN")] * (8 - len(val)))

        # Convert into dataframe
        df = pd.DataFrame(data=self.data, columns=["profile_url", "member_since", "earnings_pst_yr", "earnings_ever",
                                                   "employers", "invoices_paid", "largest_employ", "bio"])

        self.pandas_data = df

    def pagination(self):
        """
        The website doesn't have a 'next' button to change the page. This creates
        a list that contains the current page numbers at the bottom of the page.
        I use this against the current page number to determine which element to click.
        """
        goal_page_num = str(self.pgCur + 1)

        # Extracting elements containing page change buttons
        pgChangeButtons = self.driver.find_element_by_xpath(
            '//*[@id="ctl00_guB_ulpaginate"]')

        # Extracting the text in each one
        buttonSoup = BeautifulSoup(pgChangeButtons.get_attribute(
            'innerHTML'), 'html.parser')
        buttonSoup.find_all('a')

        # Saving results to list. Compare this against current page num.
        page_list = []
        for i, val in enumerate(buttonSoup):
            page_list.append(val.text)

        go_to = page_list.index(goal_page_num)

        # Create URL for the next page that I want to go to.
        pageClickPath = '/html/body/form/main/main/section/div/div[2]/div[2]/ul/li[' + str(
            go_to + 1) + ']/a'
        self.driver.find_element_by_xpath(pageClickPath).click()
        self.pgCur += 1

    def close(self):
        self.driver.quit()
        # display.stop()

        # Save results to csv
        filename = "./data/raw/freelancers_detail.csv"
        self.pandas_data.to_csv(filename)

        print("Successfully completed dynamic data scrape.")
