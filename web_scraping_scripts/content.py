import sys
import cloudscraper
# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, SoupStrainer
import configparser
# from web_scraping_scripts.database import Database

config = configparser.ConfigParser()
config.read("config.ini")
# config.read("config_aimin.ini")



class WebContent:
    # RETRY_AMOUNT = int(config['Constant']['retry_attempts'])
    RETRY_AMOUNT = None

    def __init__(self, web_content=None, is_retry_maximum=False):
        self._web_content = web_content
        self._is_retry_maximum = is_retry_maximum
        self._driver = None
        self.connection_fail = []
    
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

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    # establish connection until it connects 
    def connect(self, url, amount = None):
        if not amount:
            amount = WebContent.RETRY_AMOUNT
        self.is_retry_maximum = False
        scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
        # print(f"Scraper: {scraper} and url: {url}")
        info = scraper.get(url)

        if info.status_code != 200:
            print(f"Error {info.status_code} reconnecting...")
            # print("retry: ", WebContent.RETRY_AMOUNT)
            amount -= 1
            
            if amount == 0:
                print("Number of retry reached maximum amount")
                self.connection_fail.append(url)
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

            print(soup.find('h3',class_='filter-name'))
            # print(len(self.web_content))
            # print(self.web_content)
      
    def selenium_connect_edgeprop(self, url):
        driver = webdriver.Chrome()
        self.driver = driver
        driver.get(url)
        # lists = EC.presence_of_element_located((By.XPATH, '//h3[@class="listing-name"]'))

        try:
            elements = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.no-listings')) 
                
            )
            print("No listing for this page")
            print(elements.text)

            self.web_content = None
            return
        except:
            pass

        try:
            elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-1tjb2q6'))
            )
            print("Connection established")

            soup = BeautifulSoup(driver.page_source, 'lxml')

            self.web_content = soup
            # print("soup is ", soup)
        except Exception as e:
            print(f"An error occured: {e}")
            self.connection_fail.append(url)

        # time.sleep(1)
        # self.web_content = driver.page_source

    def selenium_connect_iproperty(self, url):
        driver = webdriver.Chrome()
        self.driver = driver
        driver.get(url)
        # lists = EC.presence_of_element_located((By.XPATH, '//h3[@class="listing-name"]'))

        try:
            elements = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div/h2')) 
                
            )
            print("No listing for this page")
            print(elements.text)

            self.web_content = None
            return
        except:
            pass

        try:
            elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ListingsListstyle__ResultsContainer-TIuxE.hCgmPW'))
            )
            print("Connection established")

            soup = BeautifulSoup(driver.page_source, 'lxml')

            self.web_content = soup
            with open("test.html", "w", encoding='utf-8') as f:
                f.write(str(soup))
        except:
            print(f"Connection timeout!")
            self.connection_fail.append(url)

        # time.sleep(1)
        # self.web_content = driver.page_source



if __name__ == '__main__':
    a = WebContent()
    # a.connect("https://www.edgeprop.my/rent/malaysia/shop?keyword=Mid%20Valley&")
    a.selenium_connect("https://www.edgeprop.my/rent/malaysia/shop?keyword=Mid%20Valley&")
    # print(a.web_content)
    # print(a.web_content())
    # print(len(test))
    # testt = a.web_content.prettify()
    # t = testt.find('div',class_='filter-sort-mobile d-block d-lg-none')
    # print(t)

    # with open('test.html', 'w', encoding='utf-8') as f:
    #     f.write(testt)


    # find('div',class_='filter-sort-mobile d-block d-lg-none').text
    # print(testt)
    # database = Database()

    # database.extract_data(a.web_content, config['Constant']['max_displacement'])
    # database.get_all()