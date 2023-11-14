import csv

class DataFilter:
    """
    This script get the data from the predifined text file.
    """
    def __init__(self, family_mart_address_text, commercial_type_text, listing_type_text, family_mart_address=None, commercial_type=None, listing_type=None):
        self._family_mart_address_text = family_mart_address_text
        self._commercial_type_text = commercial_type_text
        self._listing_type_text = listing_type_text
        self._family_mart_address = family_mart_address
        self._commercial_type = commercial_type
        self._listing_type = listing_type
        self._family_mart_coordinates = None
        self._family_mart_amount = None

    @property
    def family_mart_address_text(self):
        return self._family_mart_address_text
    
    @family_mart_address_text.setter
    def family_mart_address_text(self, family_mart_address_text):
        self._family_mart_address_text = family_mart_address_text

    @property
    def commercial_type_text(self):
        return self._commercial_type_text
    
    @commercial_type_text.setter
    def commercial_type_text(self, commercial_type_text):
        self._commercial_type_text = commercial_type_text

    @property
    def listing_type_text(self):
        return self._listing_type_text

    @listing_type_text.setter
    def listing_type_text(self, listing_type_text):
        self._listing_type_text = listing_type_text

    @property
    def family_mart_address(self, index=None):
        return self._family_mart_address if index is None else self._family_mart_address[index]

    @family_mart_address.setter
    def family_mart_address(self, family_mart_address):
        self._family_mart_address = family_mart_address

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
    def family_mart_amount(self):
        return self._family_mart_amount

    @family_mart_amount.setter
    def family_mart_amount(self, family_mart_amount):
        self._family_mart_amount = family_mart_amount

    def extract_commercial_type(self):
        types = []
        # Open the file in read mode
        with open(self._commercial_type_text, 'r') as file:
            # Read a single line from the file
            line = file.readline()
            
            # Check if the line is not empty
            while line:
                # Process the line (e.g., print it)
                types.append(line.strip())  # .strip() removes trailing newline characters
                # Read the next line
                line = file.readline()

        self._commercial_type = types

        if len(self._commercial_type) == 0:
            print(f"No filter is applied.")
        else:
            print(f"Filter applied for commercial type: {self._commercial_type}")     

    """
    Get data from FMStore.csv
    Tis function get all the data of column 2nd (Store name)
    """
    def extract_family_mart_address(self):
        location = []
        coordinate = []
        with open(self._family_mart_address_text, 'r') as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                location.append(row[1])
                coordinate.append(row[6])
            
        # print(coordinate[1:])
        # addresses = location[1:].split(",")
        addresses = location[1:]
        coordinates = coordinate[1:]

        self.family_mart_address = addresses
        self.family_mart_coordinates = coordinates
        self.family_mart_amount = len(self._family_mart_address)
        if self._family_mart_amount == 0:
            print(f"No filter is applied.")
        else:
            print(f"Filter applied for addresses: {self.family_mart_coordinates}")     

        # print(self) 

    # def extract_family_mart_address(self):
    #     addresses = []
    #     # Open the file in read mode
    #     with open(self._family_mart_address_text, 'r') as file:
    #         # Read a single line from the file
    #         line = file.readline()
            
    #         # Check if the line is not empty
    #         while line:
    #             # Process the line (e.g., print it)
    #             addresses.append(line.strip())  # .strip() removes trailing newline characters
    #             # Read the next line
    #             line = file.readline()

    #     self.family_mart_address = addresses
    #     self.family_mart_amount = len(self._family_mart_address)
    #     if self._family_mart_amount == 0:
    #         print(f"No filter is applied.")
    #     else:
    #         print(f"Filter applied for addresses: {self._family_mart_address}")             

    def extract_listing_type(self):
        listing = []
        # Open the file in read mode
        with open(self._listing_type_text, 'r') as file:
            # Read a single line from the file
            line = file.readline()
            
            # Check if the line is not empty
            while line:
                # Process the line (e.g., print it)
                listing.append(line.strip())  # .strip() removes trailing newline characters
                # Read the next line
                line = file.readline()

        self._listing_type = listing

        if len(self._listing_type) == 0:
            print(f"No filter is applied.")
        else:
            print(f"Filter applied for listing type: {self._listing_type}")          

    def extract_all(self):
        self.extract_commercial_type()
        self.extract_family_mart_address()
        self.extract_listing_type()


def main():
    df = DataFilter("FMStore.csv", "filter.txt", "listing_type.txt")
    df.extract_all()

    print(df.family_mart_address)
    print(f"Amount is {df._family_mart_amount}")


if __name__ == '__main__':
    main()