from web_scraping_scripts.location import Location

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Database:
    def __init__(self):
        self._name = []
        self._address = []
        self._description = []
        self._size = []
        self._price = []
        self._psf = []
        self._displacement = []
        self._reference = []
        self.num_of_listings = 0
        self._number_of_listing = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name.append(name)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address.append(address)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description.append(description)

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._size.append(size)
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price.append(price)

    @property
    def psf(self):
        return self._psf

    @psf.setter
    def psf(self, psf):
        self._psf.append(psf)

    @property
    def displacement(self):
        return self._displacement

    @displacement.setter
    def displacement(self, displacement):
        self._displacement.append(displacement)
    
    @property
    def reference(self):
        return self._reference
    
    @reference.setter
    def reference(self, reference):
        self._reference.append(reference)
        
    # @property
    # def number_of_listing(self):
    #     return self._number_of_listing
    
    # @number_of_listing.setter
    # def number_of_listing(self, number_of_listing):
    #     self._number_of_listing = number_of_listing

    def get_all(self):
        # print(f"Start printing {len(self.name)}")
        for i in range(len(self.name)):
            print("\n")
            print(f"Name is {self.name[i]}")
            print(f"Address is {self.address[i]}")
            print(f"Description is {self.description[i]}")
            print(f"Size is {self.size[i]}")
            print(f"Price is {self.price[i]}")
            print(f"Psf is {self.psf[i]}")
            print(f"Displacement is {self.displacement[i]}")
            print(f"Reference is {self.reference[i]}")

        print(f"Number of listing for this location so far is {len(self.name)}")

    def get_current(self):
        # print(f"Start printing {len(self.name)}")
        print(f"Name is {self.name[-1]}, Address is {self.address[-1]}, Description is {self.description[-1]}, Size is {self.size[-1]}, Price is {self.price[-1]}, Psf is {self.psf[-1]}, Displacement is {self.displacement[-1]}, Reference is {self.reference[-1]}")

        print(f"Number of listing for this location so far is {len(self.name)}")

    # Scraping data from given url into class variables 
    def extract_data(self, web_content, max_displacement, base_url, fm_coordinate=None):
        num_of_listings = 0
        print("Start storing")

        listing = web_content.find_all('div', class_='css-1tjb2q6')
        # print(listing)
        if not listing:
            print("There are no listings available")
            return True     

        for index, list in enumerate(listing):
            # print(list)
            try:
                address = list.find('div', class_ ='listing-address').text    
                num_of_listings += 1
            except AttributeError as e:
                print(f"AttributeError: {e} for address")    
                address = None        

            distance = Location.distance_calculator(fm_coordinate, address) 

            if distance > max_displacement:
                print(f"Distance is larger than {max_displacement} and will not be included")
                continue

            
            self.address = address
            print(self.address)
            try:
                self.displacement = distance
                print(self.displacement)
            except AttributeError as e:
                print(f"AttributeError: {e} for displacement")
                self.displacement = None

            try:
                self.name = list.find('h3', class_='listing-name').text
                print(self.name)
            except AttributeError as e:
                print(f"AttributeError: {e} for name")
                self.name = None

            try:
                self.price = list.find('div', class_= 'listing-price').div.span.text.replace(",", "").strip()
                print(self.price)
            except AttributeError as e:
                print(f"AttributeError: {e} for price")
                self.price = None

            try:
                property_type = web_content.find('div', 'dd-toggle-output').text
                # print(property_type)
                property_type2 = list.find('span', class_='listing-address-style').text
                # print(property_type2)
                self.description = property_type + " / " + property_type2
                print(self.description)
            except AttributeError as e:
                print(f"AttributeError: {e} for description")    
                self.description = None                        

            try:
                reference = list.find("a", class_='text-decoration-none')['href']
                self.reference = base_url[:-1] + reference
                print(self.reference)
            except AttributeError as e:
                print(f"AttributeError: {e} for reference")  
                self.reference = None    

            try:
                self.size = list.find('div', class_='listing-address-style').span.text.split()[0].replace(",", "")
                # self.size = list.find('div', class_='listing-address-style')
                print(f"size is {self.size}")
            except AttributeError as e:
                print(f"AttributeError: {e} for size")     
                self.size = None
            except IndexError as e:
                print(f"IndexError: {e} for size")
                self.size = None

            try:      
                self.psf = list.find('span', class_='psf').text.split()[1]
                print(f"psf is {self.psf}")
            except AttributeError as e:
                print(f"AttributeError: {e} for psf")     
                self.psf = None
            except IndexError as e:
                print(f"IndexError: {e} for psf")
                self.psf = None
        
        self.num_of_listings = num_of_listings
        # print(self.name())
        return
    
