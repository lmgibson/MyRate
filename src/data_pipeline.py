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
dbimport.insertUsers()
dbimport.insertRates()
dbimport.insertSkills()

print("Upload complete!")
