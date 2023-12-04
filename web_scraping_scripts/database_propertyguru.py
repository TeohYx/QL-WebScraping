from web_scraping_scripts.location import Location
import time
class Database:
    # EVERY OBJECT MEANS EACH LOCATION
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
        self.all = {}
        self.connections = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name.append(name)
        # self._name = name
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address.append(address)
        # self._address = address
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description.append(description)
        # self._description = description
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._size.append(size)
        # self._size = size    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price.append(price)
        # self._price = price
    @property
    def psf(self):
        return self._psf

    @psf.setter
    def psf(self, psf):
        self._psf.append(psf)
        # self._psf = psf
    @property
    def displacement(self):
        return self._displacement

    @displacement.setter
    def displacement(self, displacement):
        self._displacement.append(displacement)
        # self._displacement = displacement
    @property
    def reference(self):
        return self._reference
    
    @reference.setter
    def reference(self, reference):
        self._reference.append(reference)
        # self._reference = reference        
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
    def extract_data(self, web_content, max_displacement, fm_coordinate=None):
        # if not self.all:
        #     print("GOT")
        #     self.all[max_displacement] = []
        #     self.all[max_displacement_larger] = []

        listing = web_content.find_all('div', class_='listing-card')
        roomSizes = web_content.find_all('li', class_='listing-floorarea pull-left')
        # print("THIS IS \n", listing)
        # print(location.distance_calculator("Jalan Ampang, KL City, Kuala Lumpur", "Lot G-01, Ground Floor, Wisma Lim Foo Yong, 86, Jalan Raja Chulan, 50200 Kuala Lumpur"))
        # print("THIS IS ", roomSizes)
        self.num_of_listings += len(listing)

        # Break out of function if no listings found
        if not listing or not roomSizes:
            print("There are no listings available")
            return True     


        roomLists = [roomSizes[i].text for i in range(len(roomSizes))]
        roomList = [roomLists[i:i+2] for i in range(0, len(roomLists), 2)]

        for index, list in enumerate(listing):
            # is_max_displacement = False
            # is_max_displacement_larger = False

            try:
                address = list.find('p', class_ ='listing-location ellipsis').span.text    
            except AttributeError as e:
                print(f"AttributeError: {e} for address")    
                address = None        

            distance = Location.distance_calculator(fm_coordinate, address) 

            if distance > max_displacement:
                print(f"Distance is larger than {max_displacement} and will not be included")
                continue
            # if distance < max_displacement:
            #     print(f"Distance lower than {max_displacement}")
            #     is_max_displacement = True
            # if distance < max_displacement_larger:
            #     print(f"Distance lower than {max_displacement_larger}")
            #     is_max_displacement_larger = True
            self.address = address

            try:
                self.displacement = distance
            except AttributeError as e:
                print(f"AttributeError: {e} for displacement")
                self.displacement = None

            try:
                self.name = list.find('a', attrs={'data-automation-id':'listing-card-title-txt'}).text
                # print(self.name)
            except AttributeError as e:
                print(f"AttributeError: {e} for name")
                self.name = None

            try:
                self.price = list.find('span', class_= 'price').text.replace(",", "")
            except AttributeError as e:
                print(f"AttributeError: {e} for price")
                self.price = None

            try:
                self.description = [type.text.strip().replace("\n", ",") for type in list.find_all('ul', class_='listing-property-type')]
            except AttributeError as e:
                print(f"AttributeError: {e} for description")    
                self.description = None                        

            try:
                self.reference = list.find("a", class_='nav-link')['href']
            except AttributeError as e:
                print(f"AttributeError: {e} for reference")  
                self.reference = None    

            try:
                self.size = roomList[index][0].split()[0].replace(",","")
            except AttributeError as e:
                print(f"AttributeError: {e} for size")     
                self.size = None
            except IndexError as e:
                print(f"IndexError: {e} for size")
                self.size = None

            try:
                self.psf = roomList[index][1].split()[1]
            except AttributeError as e:
                print(f"AttributeError: {e} for psf")     
                self.psf = None
            except IndexError as e:
                print(f"IndexError: {e} for psf")
                self.psf = None
        
            # # print(self.all)
            # if is_max_displacement:
            #     self.all[max_displacement].append((self.name, self.description, self.price, self.size, self.psf, self.reference, self.address, self.displacement))
            # if is_max_displacement_larger:
            #     self.all[max_displacement_larger].append((self.name, self.description, self.price, self.size, self.psf, self.reference, self.address, self.displacement))
        
            # print(self.all)
            # time.sleep(3)
        return
    
