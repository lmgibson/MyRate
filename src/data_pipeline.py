from datetime import date
# Scrape and Clean commands
from freelance_scrape import scrape as ss
from freelance_scrape import clean as cl
from freelance_scrape import importdb as dbimport

# Scraping Static Elements
scraper = ss.GuruScraper()
scraper.generate_urls(startPage=1, endPage=10)
scraper.html_extract()
scraper.freelancer_extraction()
scraper.data_extraction()

# Cleaning data
clean_class = cl.CleanData()
clean_class.merge_data()

print("Scrape and Clean complete")

# Insert into postgres db
today = date.today().strftime("%d%m%Y")
filename = "./data/processed/user_data_" + today + ".csv"
dbimport.insertUsers(filename)
dbimport.insertRates(filename)
dbimport.insertSkills(filename)

print("Upload complete!")
