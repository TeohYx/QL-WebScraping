import csv

class DataFilter:
    """
    This script get the data from the predifined text file.
    Filter:
    1. Location (like a human search in search bar)
    2. Listing type (rent, buy, etc)
    3. Property type (SOHO, office, retail space, etc)

    Output: Get all the filter accordingly 

    """
    def __init__(self, filter_text):
        self.filter_text = filter_text
        self.location_file = None           # A files containing information of locations (eg: FMStore.csv)
        self._locations = None              # A list of locations extracted from the location_file
        self.location = []                      # A list of location get from filter text
        self._commercial_type = []
        self._listing_type = []
        self._family_mart_coordinates = None
        self._location_amount = None

    def get_all(self):
        print(f"location file: {self.location_file}\nlocations: {self.locations}\nlocation: {self.location}\nproperty: {self.commercial_type}\nlisting: {self.listing_type}\nAmount: {self._location_amount}\n")

    @property
    def locations(self, index=None):
        return self._locations if index is None else self._locations[index]

    @locations.setter
    def locations(self, locations):
        self._locations = locations

    @property
    def commercial_type(self):
        return self._commercial_type

    @commercial_type.setter
    def commercial_type(self, commercial_type):
        self._commercial_type = commercial_type

    @property
    def listing_type(self):
        return self._listing_type

    @listing_type.setter
    def listing_type(self, listing_type):
        self._listing_type = listing_type

    @property
    def family_mart_coordinates(self, index=None):
        return self._family_mart_coordinates if index is None else self._family_mart_coordinates[index]
    
    @family_mart_coordinates.setter
    def family_mart_coordinates(self, family_mart_coordinates):
        self._family_mart_coordinates = family_mart_coordinates

    @property
    def location_amount(self):
        return self._location_amount

    @location_amount.setter
    def location_amount(self, location_amount):
        self._location_amount = location_amount

    """
    Get data from FMStore.csv
    Tis function get all the data of column 2nd (Store name)
    """
    def extract_location(self):
        location = []
        coordinate = []
        with open(self.location_file, 'r') as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                location.append(row[1])
                coordinate.append(row[6])
            
        # print(coordinate[1:])
        # addresses = location[1:].split(",")
        addresses = location[1:]
        coordinates = coordinate[1:]

        self.locations = addresses
        self.family_mart_coordinates = coordinates
        self.location_amount = len(self._locations)
        if self._location_amount == 0:
            print(f"No filter is applied.")
        else:
            print(f"Filter applied for addresses: {self.family_mart_coordinates}")     

    def extract_filter_text(self):
        with open(self.filter_text, "r") as file:
            line = file.readline()

            while line:
                if line.strip() == "LOCATION":
                    while line.strip() !='':
                        line = file.readline()

                        self.location.append(line.strip())
                if line.strip() == "LOCATION FILE":
                    while line.strip() !='':
                        line = file.readline()

                        self.location_file = line.strip()
                        self.extract_location()
                        break
                elif line.strip() == "LISTING":
                    while line.strip() !='':
                        line = file.readline()

                        self.listing_type.append(line.strip())
                elif line.strip() == "PROPERTY":
                    while line.strip() !='':
                        line = file.readline()

                        self.commercial_type.append(line.strip())
                line = file.readline()


        self.location_file = self.location_file
        self.location = self.location[:-1]
        self.commercial_type = self.commercial_type[:-1]
        self.listing_type = self.listing_type[:-1]

        if self.location:
            self.location_amount = len(self.location)


        print(f"{self.location_file}\n{self.commercial_type}\n{self.listing_type}")

                     

    def extract_commercial_type(self, site_name):
        types = []

        with open(self.filter_text, "r") as file:
            # Read a single line from the file
            line = file.readline()
            
            # Check if the line is not empty
            while line:
                print(f"line is {line.strip()}")
                if line.strip() == site_name:
                    while line.strip() != '':
                        print(f"line is {line.strip()}")
                        line = file.readline()

                        # Process the line (e.g., print it)
                        types.append(line.strip())  # .strip() removes trailing newline characters
                        # Read the next line
                line = file.readline()
        types = types[:-1]

        self._commercial_type = types

        if len(self._commercial_type) == 0:
            print(f"No filter is applied.")
        else:
            print(f"Filter applied for commercial type: {self._commercial_type}")     

    def extract_listing_type(self, site_name):
        listing = []
        # Open the file in read mode
        with open(self._listing_type_text, 'r') as file:
            # Read a single line from the file
            line = file.readline()
            
            # Check if the line is not empty
            while line:
                print(f"line is {line.strip()}")
                if line.strip() == site_name:
                    while line.strip() != '':
                        print(f"line is {line.strip()}")
                        line = file.readline()

                        # Process the line (e.g., print it)
                        listing.append(line.strip())  # .strip() removes trailing newline characters
                        # Read the next line
                line = file.readline()
        listing = listing[:-1]

        self._listing_type = listing

        if len(self._listing_type) == 0:
            print(f"No filter is applied.")
        else:
            print(f"Filter applied for listing type: {self._listing_type}")          

    def extract_all(self):
        # self.extract_commercial_type(site_name)
        self.extract_filter_text()
        # self.extract_listing_type(site_name)

# def main():
#     df = DataFilter("FMStore.csv", "filter.txt", "listing_type.txt")
#     df.extract_all()

#     print(df.locations)
#     print(f"Amount is {df._family_mart_amount}")


# if __name__ == '__main__':
#     main()