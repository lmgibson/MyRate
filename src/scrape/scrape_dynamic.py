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


def login_form_click():
    """
    Occasionally the locations of the buttons will break. This updates
    their locations and then clicks them, if it is broken.

    Returns: Nothing. Just clicks the button.
    """

    try:
        login_form[2].click()
    except:
        login_form = driver.find_elements_by_xpath(
            '//button[@class="tabControls__button"]')
        login_form[2].click()


def details_about_scrape():
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
    first_url = driver.current_url
    login_form = driver.find_elements_by_xpath(
        '//button[@class="tabControls__button"]')

    # First, checking if the site loaded. If it didn't the code will error out.
    # The reason for this is usually if the site doesn't load than user intervention
    # is required to reset by filling out a captcha.
    if len(login_form) == 0:
        return None

    time.sleep(2)  # Wait to click so everything can load.
    login_form_click()

    # Fix for when the website asks for a log-in. Works by checking if the URL has changed
    # and if it has changed it will simply page back. Otherwise it continues on by opening
    # the boxes.
    if driver.current_url != first_url:
        time.sleep(2)  # Wait for log-in prompt
        driver.back()  # Go back to main page
        time.sleep(1)  # Wait to scrape
        login_form = driver.find_elements_by_xpath(
            '//button[@class="tabControls__button"]')
    else:
        login_form_click()

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
    user_name = driver.find_elements_by_xpath(
        '//h3[@class="freelancerAvatar__screenName"]')
    user_detail = driver.find_elements_by_xpath('//div[@class="feedback"]')

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
            login_form[i].click()
            counter += 4

    time.sleep(2)

    # Pull elements and then HTML from the fourth menu (about).
    user_about = driver.find_elements_by_xpath('//div[@class="profile-about"]')
    about_html = []
    for i, val in enumerate(user_about):
        about_html.append(val.get_attribute('innerHTML'))

    # Return user names, user details HTML, and user about HTML
    return names, detail_html, about_html


def raw_to_soup(x):
    """
    Takes in a list of raw htmls and parses them with BeautifulSoup.

    Returns a list of cleaner HTMLs (soup objects)

    """
    soups = []
    for i, val in enumerate(x):
        soups.append(BeautifulSoup(val, 'html.parser'))

    return soups


def soup_urls_to_html_list(x):
    """
    Takes in a list of soups and extracts user htmls from them.

    Returns a list with user htmls

    """

    user_htmls = []
    for i, val in enumerate(x):
        user_htmls.append(val.a['href'])

    return user_htmls


def soup_details_to_html_list(x):
    """
    Takes in the list of details HTMLs and extracts the information from them.

    Returns a list with lists where the first element has a list containing the elements
    for the first user on the page, the second contains a list of elements for the second
    user details page, and so on.

    """
    values = []
    for i, val in enumerate(x):
        values.append(val.find_all('em'))

    def html_to_string(x): return x.string
    values_strings = []
    for i, val in enumerate(values):
        values_strings.append(list(map(html_to_string, val)))

        # Lots of empty details pages. This at least fill in an NA.
        if len(values_strings[i]) == 0:
            values_strings[i].append(["NA", "NA", "NA", "NA", "NA", "NA"])

    return values_strings


def soup_about_to_html_list(x):
    """
    Takes in the list of about HTMLs for the users on a given page. Extracts the
    information in the about section and returns a list the length of the number
    of users on the page

    Returns a list of user about information.
    """

    about_vals = []
    for i, val in enumerate(user_about_soup):
        try:
            tmp = val.find_all('pre')[0].text
        except:
            tmp = 'NA'
        about_vals.append(tmp)

    return about_vals


def combine_clean_data(names_list, details_list, about_list):
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
    for i, val in enumerate(details_list):
        val.insert(0, names_list[i])

    for i, val in enumerate(details_list):
        val.insert(len(val), about_list[i])

    return details_list


def combine_into_dataframe(x):
    """
    Convert the details_list returned from combine_clean_data into a pandas
    dataframe.
    """
    # First have to check the lengths of the lists in the list
    # For lists that are not the full length (missing data) I extend
    # it to be equal length. This makes putting it into the pandas data
    # frame easier.
    for i, val in enumerate(x):
        val.extend([float("NaN")] * (8 - len(val)))

    # Convert into dataframe
    df = pd.DataFrame(data=x, columns=["profile_url", "member_since", "earnings_pst_yr", "earnings_ever",
                                       "employers", "invoices_paid", "largest_employ", "bio"])

    return df


def pagination():
    """
    The website doesn't have a 'next' button to change the page. This creates
    a list that contains the current page numbers at the bottom of the page.
    I use this against the current page number to determine which element to click.
    """

    # Extracting elements containing page change buttons
    a = driver.find_element_by_xpath('//*[@id="ctl00_guB_ulpaginate"]')

    # Extracting the text in each one
    soup = BeautifulSoup(a.get_attribute('innerHTML'), 'html.parser')
    soup.find_all('a')

    # Saving results to list. Compare this against current page num.
    page_list = []
    for i, val in enumerate(soup):
        page_list.append(val.text)

    return page_list


# def add_table_to_db(dataframe, table_name):
#     """
#     Adds the data to a new table (details_table) in freelance_db.

#     """
#     # Try to figure out how to put these into a config file later.
#     dbname = 'freelance_db'
#     username = os.environ['USER']
#     pswd = os.environ['SQLPSWD']

#     # Connect to the database
#     engine = create_engine('postgresql://%s:%s@localhost/%s' %
#                            (username, pswd, dbname))
#     print('postgresql://%s:%s@localhost/%s' % (username, pswd, dbname))

#     # insert data into database from Python (proof of concept - this won't be useful for big data, of course)
#     # df is any pandas dataframe
#     dataframe.to_sql(table_name, engine, if_exists='replace')

#     print("Added data to %s" % (dbname))

print("Starting up webdriver . . .")

display = Display(visible=0, size=(800, 600))
display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.guru.com/d/freelancers/l/united-states/pg/1/")

pg_nums = range(1, 200)

print("Webdriver initiated. Beginning scrape procedure \n")

# Scraping
for j in range(0, 3):
    print("Page: ", (j + 1))

    raw_html = details_about_scrape()

    if len(raw_html[2]) != 20:
        print("Something went wrong. Need to refresh the page.")
        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        raw_html = details_about_scrape()

    user_urls_soup = raw_to_soup(raw_html[0])
    user_details_soup = raw_to_soup(raw_html[1])
    user_about_soup = raw_to_soup(raw_html[2])

    user_urls_clean = soup_urls_to_html_list(user_urls_soup)
    user_details_clean = soup_details_to_html_list(user_details_soup)
    user_about_clean = soup_about_to_html_list(user_about_soup)

    combined_data = combine_clean_data(
        user_urls_clean, user_details_clean, user_about_clean)

    if j == 0:
        # On first pass make the dataframe
        df_tmp = combine_into_dataframe(combined_data)
        df_tmp.fillna(value=np.nan, inplace=True)
    else:
        # For all other passes just merge into the dataframe
        tmp = combine_into_dataframe(combined_data)
        tmp.fillna(value=np.nan, inplace=True)
        df_tmp = pd.concat([df_tmp, tmp])

    print("Finished page " + str(j + 1))

    # Changing the page
    # First figuring out what page I'm on
    cur_page_num = int(pg_nums[j])
    goal_page_num = str(cur_page_num + 1)

    # Then make a list of all page listings at the bottom of the current page
    button_directory = pagination()
    go_to = button_directory.index(goal_page_num)

    # Create URL for the next page that I want to go to.
    xpath_click = '/html/body/form/main/main/section/div/div[2]/div[2]/ul/li[' + str(
        go_to + 1) + ']/a'
    driver.find_element_by_xpath(xpath_click).click()

driver.quit()
display.stop()

# Save results to csv
filename = "./freelancers_detail.csv"
df_tmp.to_csv(filename)

print("Successfully completed scrape. Returning a dataset with the following information: \n", df_tmp.info())
