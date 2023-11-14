from web_scraping_scripts.filter_data import DataFilter
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class RentalURLs:
    """
    Format: https://www.propertyguru.com.my/property-for-rent? -> any filter done after this
    Place - freetext
    Market - market
    ListingType - listing_type
    Types - property_type_code[]
    """

    # def __init__(self, base_url, place, market, listing_type, types, url):
    def __init__(self, base_url, market):
        self._base_url = base_url
        self._place = ""
        self._market = 'market=' + market + "&"
        self._listing_type = ""
        self._types = ""
        # self._url = url
        self._url = ""
    
    def __str__(self):
        return "The url link to search is {}".format(self.url)

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, info):
        try:
            df, index = info
        except:
            raise ValueError("Please pass with 2 arguments.")

        place = df.family_mart_address[index]
        
        temp_place = place.replace((config['Constant']['family_mart_checker'] + " "), "")
        place = 'freetext=' + temp_place.strip().replace(' ', '%20') + '&'
        self._place = place
        # print(self._place)


        # for index in range(4):
        #     last_occurrence = temp_place.rindex(',')
        #     temp_place = temp_place[:last_occurrence]

        # place = "freetext=" + place[last_occurrence+1:].strip().replace(' ', '%20') + '&'
        # self._place = place
        # # print(self._place)

    @property
    def market(self):
        return self._market

    @market.setter
    def market(self, market):
        self._market = market

    # Get data from filter_data.py
    @property
    def listing_type(self):
        return self._listing_type

    @listing_type.setter
    def listing_type(self, df):
        types = df.listing_type

        if types is None:
            return ""

        for type_ in types:
            self._listing_type += 'listing_type=' + type_ + "&"

        #  Example format: listing_type=rent&listing_type=buy&
        # print(self._listing_type)

    # Get data from filter_data.py
    @property
    def types(self):
        return self._types
    
    # Commercial type
    @types.setter
    def types(self, df):
        com_types = df.commercial_type

        if com_types is None:
            return ""

        for com_type in com_types:
            self._types += 'property_type_code[]=' + com_type + "&"
        
        # print(self._types)

    @property
    def url(self):
        return (self.base_url + self.place + self.listing_type + self.market + self.types)[:-1]

    @url.setter
    def url(self, info):
        try:
            df, index = info
        except:
            raise ValueError("Please pass with 2 arguments.")

        # self.base_url = df
        self.place = (df, index)
        self.listing_type = df
        # self.market = df
        self.types = df

def main():
    rent = RentalURLs("https://www.propertyguru.com.my/property-for-rent?", "commercial")
    df = DataFilter("FMStore.csv", "filter.txt", "listing_type.txt")
    df.extract_all()
    rent.url = df
    print(rent.url)
    # df.extract_commercial_type()
    # df.extract_family_mart_address()
    print(f"Amount is {df._family_mart_amount}")

if __name__ == "__main__":
    main()