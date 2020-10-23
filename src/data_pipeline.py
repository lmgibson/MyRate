# Scrape and Clean commands
from scrape import scrape_static as ss
# from scrape import scrape_dynamic_oop as sd
from data_cleaning import clean as cl
from upload_data import convert_to_json as up

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

# Upload data to airtable databse
up.ImportData()

print("Upload complete!")
