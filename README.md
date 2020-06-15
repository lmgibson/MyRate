# MyRate -  A tool to help freelancers determine their hourly rate

![alt text](https://github.com/lmgibson/MyRate/blob/master/readme/product_photo.png?raw=true)

## Welcome

MyRate is a tool to help new freelancers determine how to set their hourly rate. Sites such as Upwork
and Guru don't provide guidelines for setting an hourly rate. As a result, new freelancers have to
spend time sifting through lists of freelancers to find individuals similar to them in order to determine
their hourly rate. MyRate automates this process to improve the accuracy with which freelancers set their
hourly rate (compared to hourly rates in the market) and saves the freelancer time.

## How to Use

You can use this tool by going to the [MyRate web app](http://54.153.93.21:8501/), entering your information, and immediately have your
hourly rate estimate.

In the future we hope to expand the tool to make suggestions for how you can improve your profile, compared
to high earning freelancers on your platform.

## How this project is organized

The project consists of four folders: data, notebooks, projectname, and scripts.

### Data

Data contains any raw/processed/cleaned data that is used to build the tool. Most of the data
is put on a SQL database and is not included in the Data folder. What is there are supplemental data files
such as city-level information.

### Notebooks

This folder is the core of the project because it contains several notebooks that are used to scrape data,
conduct EDA, and model the hourly rate.

1. Scrape Data:
    - scraping_data.ipynb: Scrapes the data that is easily accessed via static HTML
    - selenium_scraping.ipynb: Scrapes the data only available in interactive modules
    - freelance_skill_categories_scrape.ipynb: Scrapes the category - sub-category - skills data.
2. Explore Data:
    - myrate_eda.ipynb: EDA evaluating the relationships between the scraped data and hourly rate. This notebook
    also creates several new features using user bios (text data), dates (member duration), and skills (dimension reduction).
3. Modeling:
    - model_training.ipynb: Trains a random forest regression model.

### ProjectName

This is a work in progress folder. Ideally, it will contain project specific functions and global variables.

### Scripts

This folder has the script used to create the web-app (streamlit_app.py) and the exported, trained, model (finalized_model.sav)
