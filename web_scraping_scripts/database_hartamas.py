import web_scraping_scripts.location as location

class Database:
    def __init__(self):
        self._name = []
        self._address = []
        self._description = []
        self._size = []
        self._storey = []
        self._psf = []
        self._displacement = []
        self._reference = []
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
    def storey(self):
        return self._storey
    
    @storey.setter
    def storey(self, price):
        self._storey.append(price)

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
            # print(f"Description is {self.description[i]}")
            print(f"Size is {self.size[i]}")
            print(f"Storey is {self.storey[i]}")
            print(f"Psf is {self.psf[i]}")
            print(f"Reference is {self.reference[i]}")

        print(f"Number of listing for this location so far is {len(self.name)}")


    # def remove_data(self, index):
    #     print("before: ", len(self.name))
    #     self.name.pop(index)
    #     self.address.pop(index)
    #     self.description.pop(index)
    #     self.size.pop(index)
    #     self.price.pop(index)
    #     self.psf.pop(index)
    #     self.displacement.pop(index)
    #     self.reference.pop(index)
    #     print("after: ", len(self.name))

    def get_current(self):
        # print(f"Start printing {len(self.name)}")
        print(f"Name is {self.name[-1]}, Address is {self.address[-1]}, Description is {self.description[-1]}, Size is {self.size[-1]}, Price is {self.storey[-1]}, Psf is {self.psf[-1]}, Displacement is {self.displacement[-1]}, Reference is {self.reference[-1]}")

        print(f"Number of listing for this location so far is {len(self.name)}")

    # Scraping data from given url into class variables 
    def extract_data(self, web_content, fm_coordinate=None):
        print("this")
        listing = web_content.find_all('article', class_='rh_prop_card rh_prop_card--listing')
        # print(listing)
        wrapattributes = web_content.find_all('span', class_= 'figure')
        # print("THIS IS \n", listing)
        # print(location.distance_calculator("Jalan Ampang, KL City, Kuala Lumpur", "Lot G-01, Ground Floor, Wisma Lim Foo Yong, 86, Jalan Raja Chulan, 50200 Kuala Lumpur"))
        # print("THIS IS ", roomSizes)
        # Break out of function if no listings found
        if not listing:
            print("There are no listings available")
            return True     
# b = [i for i in a if (i%2)-1 == 0]
        print(len(wrapattributes))
        # attribute_wraps = wrapattributes.find('div', class_='rh_prop_card__meta_wrap')
        # wrapattribute = [first for first in wrapattributes if (first%2)-1 == 0]
        # print(wrapattribute)
        attributes = [wrapattributes[i].text for i in range(len(wrapattributes))]
        attribute = [attributes[i:i+2] for i in range(0, len(attributes), 2)]
        # print(attribute)

        for index, list in enumerate(listing):
            print("here")
            try:
                self.address = list.find('div', class_='rh_prop_card__details').h3.text[1:-1]  
                print(self.address)
            except AttributeError as e:
                print(f"AttributeError: {e} for address")    
                self.address = None        

            try:
                self.name = list.find('div', class_='rh_prop_card__details').h3.text[1:-1]
                print(self.name)
            except AttributeError as e:
                print(f"AttributeError: {e} for name")
                self.name = None

            try:
                self.storey = attribute[index][0]
                print(self.storey)
            except AttributeError as e:
                print(f"AttributeError: {e} for price")
                self.storey = None
                
            try:
                self.reference = list.find('div', class_="rh_prop_card__details").h3.a['href']
                print(self.reference)
            except AttributeError as e:
                print(f"AttributeError: {e} for reference")  
                self.reference = None    

            try:
                self.size = attribute[index][1].replace("\n", "").replace("\t", "")
                print(self.size)
            except AttributeError as e:
                print(f"AttributeError: {e} for size")     
                self.size = None
            except IndexError as e:
                print(f"IndexError: {e} for size")
                self.size = None

            try:
                self.psf = list.find('p', class_='rh_prop_card__price').text.replace("RM", "").strip()
                print(self.psf)
            except AttributeError as e:
                print(f"AttributeError: {e} for psf")     
                self.psf = None
            except IndexError as e:
                print(f"IndexError: {e} for psf")
                self.psf = None
        return
    
