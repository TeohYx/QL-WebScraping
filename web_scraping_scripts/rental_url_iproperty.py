from web_scraping_scripts.filter_data import DataFilter
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class RentalURLs:
    """
    Format: https://www.iproperty.com.my/rent/{Property-type}}/? -> any filter done after this
    search_bar = "q="
    """
    def __init__(self, base_url, property_type, listing_type):
        self._base_url = base_url
        self._search_bar = 'q='
        self._listing_type = listing_type + '/'
        # self._extension = 'malaysia/'
        self._property_type = property_type + '/?'
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
    def search_bar(self):
        return self._search_bar

    @search_bar.setter
    def search_bar(self, info):
        try:
            df, index = info
        except:
            raise ValueError("Please pass with 2 arguments.")

        place = df.locations[index]
        
        # {search_bar}{temp_place}
        # q=subang%20jaya/&
        temp_place = place.replace((config['Constant']['family_mart_checker'] + " "), "")
        place = self.search_bar + temp_place.strip().replace(' ', '%20')
        self._search_bar = place

    # Get data from filter_data.py
    @property
    def listing_type(self):
        return self._listing_type

    # Get data from filter_data.py
    @property
    def property_type(self):
        return self._property_type

    @property
    def url(self):
        # Format: https://www.iproperty.com.my/rent/{Property-type}}/?q={search-bar}/&
        return (self.base_url + self.listing_type + self.property_type + self.search_bar)

    @url.setter
    def url(self, info):
        try:
            df, index = info
        except:
            raise ValueError("Please pass with 2 arguments.")

        # self.base_url = df
        self.search_bar = (df, index)


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