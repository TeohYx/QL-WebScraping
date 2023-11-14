import csv

class Test:
    def __init__(self, w):
        self.w = w

    @property
    def _w(self):
        return self.w

# b = []

# b.append(Test(3))
# b.append(Test(4))

# for index in range(len(b)):
#     print(b[index]._w)

# print(b)
# location = []
# with open('FMStore.csv', 'r') as f:
#     reader = csv.reader(f, delimiter=",")
#     for row in reader:
#         location.append(row[6])
    
# print(location[1].split(',')[0])

# import sys
# import cloudscraper
# from bs4 import BeautifulSoup

# scraper = cloudscraper.create_scraper()
# info = scraper.get("https://www.propertyguru.com.my/property-for-rent/7?freetext=Mid+Valley&market=COMMERCIAL&property_type_code%5B0%5D=RTLSP&property_type_code%5B1%5D=SHOP&property_type_code%5B2%5D=SHOPO")
# if info.status_code != 200:
#     print(f"Error {info.status_code} reconnecting...")
#     amount -= 1
#     return self.connect(url, amount)
# else:
# print("connection established!")
# ds.set_web_content(info)
# print(ds.get_web_content())


# soup = BeautifulSoup(info.text, 'lxml')      
# print(soup)  
# print("next can? ", soup.find_all(class_="pagination-next disabled")) 

# if soup.find_all(class_="pagination-next disabled"):
#     print("HI")
# else:
#     print("nohi")
# import subprocess

# command = "dir"
# print("hhaah")
# output = subprocess.check_output(command, shell=True, text=True)


# f = open("terminal.txt")
# print(output)
# import configparser
# config = configparser.ConfigParser()
# config.read('config.ini')
# config.sections()
# # [print(conf) for conf in config['File']]
# print(config.options(config.sections()[1])[1])
# url = config['Link']['geoapify_url_first'] + "Majestic Maxim Jalan 9/142, Taman Len Seng, Batu 9, Cheras, Kuala Lumpur" + config['Link']['geoapify_url_last']
# print(url)
# print(config)
# print(config.sections())

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# for i in a:


# b=[]
b = [i for i in a if (i%2)-1 == 0]
print(b)