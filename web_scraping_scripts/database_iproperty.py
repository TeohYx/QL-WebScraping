from web_scraping_scripts.location import Location

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Database:
    def __init__(self):
        self._name = []
        # [[[a, b, c], [a, b, c], [a, b, c]],
        # [[a, b, c], [a, b, c], [a, b, c]],
        # [[a, b, c], [a, b, c], [a, b, c]]]
        self._address = []
        self._description = []
        self._size = []
        self._price = []
        self._psf = []
        self._displacement = []
        self._reference = []
        # [[1, 2, 3],
        # [1, 2, 3],
        # [1, 2, 3]]
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
        # num_of_listings = 0
        print("Start storing")

        listing = web_content.find_all('li', class_='ListingsListstyle__ListingListItemWrapper-hjHtwj')
        self.num_of_listings += len(listing)
        # print(listing)
        if not listing:
            print("There are no listings available")
            return True     

        for index, list in enumerate(listing):
            # print(list)
            # ADDRESS
            try:
                address1 = list.find('div', class_="FeaturedCardstyle__AddressWrapper-hTnZXH").text
                # print(address1)
            except AttributeError as e:
                # print(f"AttributeError: {e} for address")    
                address1 = None    

            try:
                address2 = list.find('div', class_="BasicCardstyle__AddressWrapper-jUpzVZ").text
                # print(address2)
            except AttributeError as e:
                # print(f"AttributeError: {e} for address")    
                address2 = None    

            if address1 is None and address2 is None:
                print("Address not found")
                # Return used because if the address is NOne then the whole information is not required as the displacement will not be known
                return

            if address1 is not None:
                address = address1
                print(address)
            else:              
                address = address2
                print(address)

            # num_of_listings += 1                

            # DISPLACEMENT
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

            # NAME
            try:
                name1 = list.find('h2', class_="FeaturedCardstyle__TitleWrapper-cTxkFN").text
            except AttributeError as e:
                # print(f"AttributeError: {e} for name")
                name1 = None

            try:
                name2 = list.find('h2', class_="BasicCardstyle__TitleWrapper-eNIiIX").text
                
            except AttributeError as e:
                # print(f"AttributeError: {e} for name")
                name2 = None

            if name1 is None and name2 is None:
                print("Name not found")
                self.name = None
            
            if name1 is not None:
                self.name = name1
                print(self.name)
            else:
                self.name = name2
                print(self.name)

            # PRICE
            try:
                self.price = list.find('li', class_= 'ListingPricestyle__ItemWrapper-etxdML').text.replace(",", "").split()[1]
                print(self.price)
            except AttributeError as e:
                print(f"AttributeError: {e} for price")
                self.price = None

            # PROPERTY TYPE
            try:
                property_type = web_content.find('p', 'ListingAttributesstyle__ListingAttrsDescriptionItemWrapper-cCDpp').text

                self.description = property_type.split('\xa0')[0].strip()
                print(self.description)
            except AttributeError as e:
                print(f"AttributeError: {e} for description")    
                self.description = None                        

            # REFERENCE
            try:
                reference = list.find_all("a", class_='depth-listing-card-link')
                # print(reference[0]['href'])

                self.reference = reference[0]['href']
                print(f"reference is {self.reference}")
            except AttributeError as e:
                print(f"AttributeError: {e} for reference")  
                self.reference = None    

            # PSF
            try:      
                self.psf = list.find('div', class_='ListingPricestyle__PricePSFWrapper-eraPyG fWQDeN listing-price-psf').text.split()[1]
                print(f"psf is {self.psf}")
            except AttributeError as e:
                print(f"AttributeError: {e} for psf")     
                self.psf = None
            except IndexError as e:
                print(f"IndexError: {e} for psf")
                self.psf = None

            # PRICE
            if self.price[-1] and self.psf[-1] is not None:
                self.size = float(self.price[-1])/float(self.psf[-1])
                print(f"Size is {self.size}")
            else:
                self.size = None
            # try:
            #     self.size = list.find('div', class_='listing-address-style').span.text.split()[0].replace(",", "")
            #     # self.size = list.find('div', class_='listing-address-style')
            #     print(f"size is {self.size}")
            # except AttributeError as e:
            #     print(f"AttributeError: {e} for size")     
            #     self.size = None
            # except IndexError as e:
            #     print(f"IndexError: {e} for size")
            #     self.size = None

        

        # print(self.name())
        return
    
