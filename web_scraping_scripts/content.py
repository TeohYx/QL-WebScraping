import sys
import cloudscraper
from bs4 import BeautifulSoup
import configparser
# from web_scraping_scripts.database import Database

config = configparser.ConfigParser()
config.read("config.ini")
# config.read("config_aimin.ini")

RETRY_AMOUNT = int(config['Constant']['retry_attempts'])

class WebContent:
    def __init__(self, web_content=None, is_retry_maximum=False):
        self._web_content = web_content
        self._is_retry_maximum = is_retry_maximum
    
    def __str__(self):
        pass

    @property
    def web_content(self):
        return self._web_content
    
    @web_content.setter
    def web_content(self, web_content):
        self._web_content = web_content

    @property
    def is_retry_maximum(self):
        return self._is_retry_maximum

    @is_retry_maximum.setter
    def is_retry_maximum(self, is_retry_maximum):
        self._is_retry_maximum = is_retry_maximum

    # establish connection until it connects 
    def connect(self, url, amount=RETRY_AMOUNT):
        self.is_retry_maximum = False
        scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

        # print(f"Scraper: {scraper} and url: {url}")
        info = scraper.get(url)

        if info.status_code != 200:
            print(f"Error {info.status_code} reconnecting...")
            amount -= 1
            
            if amount == 0:
                print("Number of retry reached maximum amount")
                self.is_retry_maximum = True
                return
            else: 
                return self.connect(url, amount)
        else:
            print("connection established!\n")
            # ds.set_web_content(info)
            # print(ds.get_web_content())
            soup = BeautifulSoup(info.text, 'lxml')
            self.web_content = soup 
            # print(self.web_content)
      

if __name__ == '__main__':
    a = WebContent()
    a.connect(config['Link']['base_url_iproperty'])

    # database = Database()

    # database.extract_data(a.web_content, config['Constant']['max_displacement'])
    # database.get_all()