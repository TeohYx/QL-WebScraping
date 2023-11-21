import os
import sys
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

url = 'https://www.edgeprop.my/rent/malaysia/all-residential?keyword=subang&'
driver.get(url)
# time.sleep(1)
# html = driver.page_source

# with open('test.html', 'w', encoding="utf-8") as f:
#     f.write(html)
#     f.close()

# print(html)s
# Set an explicit wait for a specific element to be present
try:
    # Wait up to 10 seconds for the presence of an element with the ID 'some_element_id'
    element = WebDriverWait(driver, 100).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3.listing-name'))
        # EC.presence_of_element_located((By.XPATH, '//div[@class="col-xs-12 col-sm-7  listing-description"]'))
    )
    # print(element)
    # element_text = driver.find_elements(By.CLASS_NAME, "listing-name")
    # If the element is found, print a message
    print("Element found!")
    # print(element_text)
    # element_text = element.text
    # for e in element_text:

        # print(e.text)
    # lists = driver.find_elements((By.XPATH, '//h3[@class="listing-name"]'))
    for list in element:
        print(list.text)
    # Continue with other actions if needed

except Exception as e:
    # Handle the exception or print an error message
    print(f"An error occurred: {e}")

# soup = BeautifulSoup(driver.page_source, features='lxml')
# content = soup.find('div', class_='imageWrapper').text
# print(cont)
# time.sleep(4)
# while True:

driver.close()
#     if keyboard.is_pressed("q"):
#         sys.exit()
#     pass
# driver.quit()