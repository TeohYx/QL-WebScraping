import argparse
from web_scraping_scripts.rental_url import RentalURLs
from web_scraping_scripts.filter_data import DataFilter
from web_scraping_scripts.content import WebContent
from web_scraping_scripts.workbook import Workbook
import sys
import openpyxl
import copy
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class WebScraping:
    MAX_DISPLACEMENT = None

    def __init__(self, base_url, site, db, wb, market=None, filter_text=None):
        self.market = market
        self.base_url = base_url        
        # Contain the url link corressponding to each of the family mart location in location.txt file
        self.site_name = site

        self.web_scraper = []
        self.database_content = []
        
        self.check_last_link = False
        self.check_no_listing = False
        self.check_is_finished = False      # Being called 3 times: 1. There is no listing 2. There is maximum numbeer of retry reached 3. End of the page

        # self.df = DataFilter(self.core_address_text, self.filter_text, self.listing_type_text)
        self.df = DataFilter(filter_text)
        self.cont = WebContent()
        self.database = db()
        self.workbook = wb

        print(f"\nVariable(base_url={base_url}, site={site}, db={db}, market={market}, filter_text={filter_text})\n")

# Get next page link and rerun
def iterate_page_propertyguru(ws, index, database):
    # print(f"INDEX {index}")
    soup = ws.cont.web_content
    family_mart_coordinates = ws.df.family_mart_coordinates[index]

    check_last = False
    get_disabled = soup.find_all(class_='pagination-next disabled')

    if get_disabled:
        print("last page reached")
        check_last = True

    # Scrape the current page information
    ws.check_no_listing = database.extract_data(soup, WebScraping.MAX_DISPLACEMENT, family_mart_coordinates)
    database.get_all()

    print("Last page? ", check_last)

    # No listing found
    if ws.check_no_listing:
        print("There is no listing available\n")
        ws.check_is_finished = True 
        return
    # Assign a new link to continue scraping
    if check_last:   # Last page
        print("There is only one page or is in last page\n")      
        ws.check_is_finished = True     # Last page
        return
    listing_pagination = soup.find(class_='pagination-next').a['href']

    # Get the next link and rerun
    second_index = listing_pagination.index('/', listing_pagination.index('/')+1)
    link = listing_pagination[second_index:]
 
    next_page_link = ws.base_url[:-2] + link
    print("Next link: ", next_page_link)
    ws.cont.connect(next_page_link)

    print("Maximum attempted reached? ", ws.cont.is_retry_maximum)
    if ws.cont.is_retry_maximum:
        ws.check_is_finished = True
        return
    iterate_page_propertyguru(ws, index, database)

def web_scraping_propertyguru(ws):
    """
    The main function that begins the process from web-scraping, to store data in excel.

    Input: WebScraping object that contains - base url, market type, filter .txt file, family mart .txt file and listing type .txt file

    Process: 1. Store all the filter text information in DataFilter object
             2. Form a functional url based on the (name of the family mart store (without FamilyMart), listing type, and property type) and store in the RentalURLs object.
             3. For each of the url, establish it with the connection, and the loop through all the possible page it got in the website.
             4. Store the data in a .xlsx file.
             5. From the file, summarize the data by mean, median, etc.

    Output: A .xlsx file with complete list of every family mart information.

    """
    print("Extracting the filter...\n")
    ws.df.extract_all()
    print("Extract done!\n")
    print(ws.df.get_all())
  
    ws.workbook.workflows = ws.df.locations

    print("Assigning rental url...\n")
    # Initialize and store the **rental_url** objects in web_scraper list
    for index in range(ws.df.location_amount):
        rent = RentalURLs(ws.base_url, ws.market)
        rent.url = (ws.df, index)

        ws.web_scraper.append(rent)
        print(f"{index+1} out of {ws.df.location_amount} being assigned.")
    print("Finish assigning.\n")

    print("Begin the scraping process\n")    
    # Each iteration if the scraping of each given link based on FM addresses
    for index, web in enumerate(ws.web_scraper):
        ws.check_is_finished = False

        print(f"This is the {index+1} location out of {len(ws.web_scraper)}")

        if index == len(ws.web_scraper)-1:
            print("This is the last link")
            ws.check_last_link = True
        # print(f"{web.__str__()}")

        ws.cont.connect(web.url)        # This store the web_content if connection is established

        # Print rental str, which is the url
        print(f"{web.__str__()}")
        database = ws.database

        print("Maximum attempted reached? ", ws.cont.is_retry_maximum)
        if ws.cont.is_retry_maximum:
            print("Failed to connect at first attempt.\n")
            ws.database_content.append(database) 
            print("Finished, writing to csv...\n")
            ws.workbook.store_data_propertyguru(config['File']['output_file'], index, ws.database_content[index])
            continue

        iterate_page_propertyguru(ws, index, database)         # This scrape the information and get the next link for another loop
        ws.database_content.append(database)    # database_content now contains scraping information of every listing found from the link given.

        if ws.check_is_finished:
            print("Finished, writing to csv...\n")
            # print(f"content: {ws.workbook.workflows}")
            file = config['File']['output_file']
            # print(ws.workbook.workflows)
            ws.workbook.store_data_propertyguru(file, index, ws.database_content[index])
          
    print("End? ", ws.check_last_link)
    if ws.check_last_link:      # Last last last link 
        print(f"Data saved in {file}")
        print("Exiting...\n")
        sys.exit()

    # analyse_data(file)

def iterate_page_iproperty(ws, index, database):
    soup = ws.cont.web_content
    family_mart_coordinates = ws.df.family_mart_coordinates[index]

    check_last = False
    get_disabled = soup.find_all(class_='pagination-next disabled')

    if get_disabled:
        print("last page reached")
        check_last = True

    # Scrape the current page information
    ws.check_no_listing = database.extract_data(soup, WebScraping.MAX_DISPLACEMENT, family_mart_coordinates)
    database.get_all()

    print("Last page? ", check_last)

    # No listing found
    if ws.check_no_listing:
        print("There is no listing available\n")
        ws.check_is_finished = True 
        return
    # Assign a new link to continue scraping
    if check_last:   # Last page
        print("There is only one page or is in last page\n")      
        ws.check_is_finished = True     # Last page
        return
    listing_pagination = soup.find(class_='pagination-next').a['href']

    # Get the next link and rerun
    second_index = listing_pagination.index('/', listing_pagination.index('/')+1)
    link = listing_pagination[second_index:]
 
    next_page_link = ws.base_url[:-2] + link
    print("Next link: ", next_page_link)
    ws.cont.connect(next_page_link)

    print("Maximum attempted reached? ", ws.cont.is_retry_maximum)
    if ws.cont.is_retry_maximum:
        ws.check_is_finished = True
        return
    iterate_page_propertyguru(ws, index, database)

def web_scraping_iproperty(ws):
    """
    The main function that begins the process from web-scraping, to store data in excel.

    Input: WebScraping object that contains - base url, market type, filter .txt file, family mart .txt file and listing type .txt file

    Process: 1. Store all the filter text information in DataFilter object
             2. Form a functional url based on the (name of the family mart store (without FamilyMart), listing type, and property type) and store in the RentalURLs object.
             3. For each of the url, establish it with the connection, and the loop through all the possible page it got in the website.
             4. Store the data in a .xlsx file.
             5. From the file, summarize the data by mean, median, etc.

    Output: A .xlsx file with complete list of every family mart information.

    """
    print("Extracting the filter...\n")
    ws.df.extract_all()
    print("Extract done!\n")
    ws.workbook.workflows = ws.df.locations

    print("Assigning rental url...\n")
    # Initialize and store the **rental_url** objects in web_scraper list
    for index in range(ws.df.location_amount):
        rent = RentalURLs(ws.base_url, ws.market)
        rent.url = (ws.df, index)

        ws.web_scraper.append(rent)
        print(f"{index+1} out of {ws.df.location_amount} being assigned.")
    print("Finish assigning.\n")

    print("Begin the scraping process\n")    
    # Each iteration if the scraping of each given link based on FM addresses
    for index, web in enumerate(ws.web_scraper):
        ws.check_is_finished = False

        print(f"This is the {index+1} location out of {len(ws.web_scraper)}")

        if index == len(ws.web_scraper)-1:
            print("This is the last link")
            ws.check_last_link = True
        # print(f"{web.__str__()}")

        ws.cont.connect(web.url)        # This store the web_content if connection is established

        # Print rental str, which is the url
        print(f"{web.__str__()}")
        database = ws.database

        print("Maximum attempted reached? ", ws.cont.is_retry_maximum)
        if ws.cont.is_retry_maximum:
            print("Failed to connect at first attempt.\n")
            ws.database_content.append(database) 
            print("Finished, writing to csv...\n")
            ws.workbook.store_data_propertyguru(config['File']['output_file'], index, ws.database_content[index])
            continue

        iterate_page_propertyguru(ws, index, database)         # This scrape the information and get the next link for another loop
        ws.database_content.append(database)    # database_content now contains scraping information of every listing found from the link given.

        if ws.check_is_finished:
            print("Finished, writing to csv...\n")
            # print(f"content: {ws.workbook.workflows}")
            file = config['File']['output_file']
            ws.workbook.store_data_propertyguru(file, index, ws.database_content[index])
          
    print("End? ", ws.check_last_link)
    if ws.check_last_link:      # Last last last link 
        print(f"Data saved in {file}")
        print("Exiting...\n")
        sys.exit()

    # analyse_data(file)

# Get next page link and rerun
def iterate_page_hartamas(ws, database):
    """
    Iterate through the page of the website until the last page / connection is blocked
    """

    soup = ws.cont.web_content

    check_last = False
    get_disabled = soup.find('a', class_='rh_pagination__btn rh_pagination__next') == None
    print(get_disabled)
    if get_disabled:
        print("last page reached")
        check_last = True

    # Scrape the current page information
    ws.check_no_listing = database.extract_data(soup)
    database.get_all()

    print("Last page? ", check_last)

    # No listing found
    if ws.check_no_listing:
        print("There is no listing available\n")
        ws.check_is_finished = True 
        return
    # Assign a new link to continue scraping
    if check_last:   # Last page
        print("There is only one page or is in last page\n")      
        ws.check_is_finished = True     # Last page
        return
    listing_pagination = soup.find('a', class_="rh_pagination__btn rh_pagination__next")['href']

    print("Next link: ", listing_pagination)
    ws.cont.connect(listing_pagination)

    print("Maximum attempted reached? ", ws.cont.is_retry_maximum)
    if ws.cont.is_retry_maximum:
        ws.check_is_finished = True
        return
    iterate_page_hartamas(ws, database)

def web_scraping_hartamas(ws):
    """
    Perform web scraping in Hartamas website
    The main function that begins the process from web-scraping, to store data in excel.

    Input: WebScraping object that contains - base url, database (required) 
                                              market type, filter .txt file, family mart .txt file and listing type .txt file  (optional)

    Process: 1. Store all the filter text information in DataFilter object
             2. Form a functional url based on the (name of the family mart store (without FamilyMart), listing type, and property type) and store in the RentalURLs object. (if there is any filter)
             3. For each of the url, establish it with the connection, and the loop through all the possible page it got in the website. (in the iterate_page() function)
             4. Store the data in a .xlsx file.
             5. From the file, summarize the data by mean, median, etc.

    Output: A .xlsx file with complete list of every family mart information.
    """
    # ws.workbook = Workbook()
    print("Assigning rental url...\n")

    print("Begin the scraping process\n")    

    ws.cont.connect(ws.base_url)        # This store the web_content if connection is established
    # print(ws.cont.web_content)

    database = ws.database

    print("Maximum attempted reached? ", ws.cont.is_retry_maximum)

    if ws.cont.is_retry_maximum:
        print("Failed to connect after several attempts.\n")

        print("Finished, writing to csv...\n")
        ws.workbook.store_data_hartamas("output/hartamas.xlsx", database)

    iterate_page_hartamas(ws, database)         # This scrape the information and get the next link for another loop

    if ws.check_is_finished:
        print("Finished, writing to csv...\n")
        # print(f"content: {ws.workbook.workflows}")
        file = "output/hartamas.xlsx"
        ws.workbook.store_data_hartamas(file, database)

        print(f"Data saved in {file}")
        print("Exiting...\n")
        sys.exit()

    # analyse_data(file)

def analyse_data(file):
    """
    Calculate the data from the result in .xlsx file
    Input: Output file
    Output: Statistic summary such as mean, median, standard deviation, etc.
    """

    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active

    store_name_column = 0
    price_column = 3
    size_column = 4
    psf_column = 5

    store_name_values = []
    price_values = []
    size_values = []
    psf_values = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        store_name_value = row[store_name_column]
        price_value = row[price_column]
        size_value = row[size_column]
        psf_value = row[psf_column]

        store_name_values.append(store_name_value)
        price_values.append(price_value)
        size_values.append(size_value)
        psf_values.append(psf_value)

    important_value_dict = {}
    data = {}

    value_temp = []

    checker = config['Constant']['family_mart_checker']
    record_data = 0

    store_name = None
    # important_value_dict = OrderedDict()
    for index, name in enumerate(store_name_values):
        # print(f"data here is {data}")
        # print(name)
        if checker in str(name):     # run when the name contains FamilyMart
            store_name = name
            # continue for the first time 
            if record_data >= 1:        # for more than first time, record data
                important_value_dict["name"] = name
                value_temp.append((price_values[index], size_values[index], psf_values[index]))
                        
            record_data += 1
        else:
            if record_data >= 1:
                # print(f"Value is {value_temp}")

                data[store_name] = copy.copy(value_temp)
                # print(f"data is {data}")
                value_temp.clear()
                record_data = 0
            record_data = 0 # means it finished loop the previous listings and ned to giv new one

    statistic = {}
 
    """
    data = 
    {
    "Family Mart Store Name": [], [(price, size, psf)], [(price, size, psf),(price, size, psf)...] ... 
    }
    """
    number_of_parameter = 16
    for key, value in data.items():
        if key == "FamilyMart Mid Valley":
            print(value)
        price = []
        size = []
        psf = []
        if not value:
            price_mean = None
            size_mean = None
            psf_mean = None
            unavailable = np.zeros(number_of_parameter)
            statistic[key] = unavailable
        else:
            for index in range(len(value)):
                p, s, ps = value[index]
                if key == "FamilyMart Mid Valley":
                    print(f"price is {p}, size is {s}, psf is {ps}")

                if None in (p, s, ps):
                    continue
                else:
                    # print("here")
                    price.append(p)
                    size.append(s)
                    psf.append(ps)


                prices = np.array(price)
                sizes = np.array(size)
                psfs = np.array(psf)
                
                # Amount
                amount = len(price)
                
                # Mean
                price_mean = np.mean(prices).round(1)
                size_mean = np.mean(sizes).round(1)
                psf_mean = np.mean(psfs).round(1)

                # Median
                price_median = np.median(prices)
                size_median = np.median(sizes)
                psf_median = np.median(psfs)

                # 0.25 Percentile
                price_25percentile = np.quantile(prices, 0.25)
                size_25percentile = np.quantile(sizes, 0.25)
                psf_25percentile = np.quantile(psfs, 0.25)

                # 0.75 Percentile
                price_75percentile = np.quantile(prices, 0.75)
                size_75percentile = np.quantile(sizes, 0.75)
                psf_75percentile = np.quantile(psfs, 0.75)

                # Standard deviation
                price_std = np.std(prices).round(2)
                size_std = np.std(sizes).round(2)
                psf_std = np.std(psfs).round(2)


            statistic[key] = np.array([price_mean, price_median, price_25percentile, price_75percentile, price_std, 
                            size_mean, size_median, size_25percentile, size_75percentile, size_std,
                            psf_mean, psf_median, psf_25percentile, psf_75percentile, psf_std, amount])
            # print(f"{key} and {prices}")
                               
    print(f"statistic is {statistic}")

    sheet = workbook.create_sheet(title="Summary")

    head = ('Price', 'Size', 'Psf')
    header = ('Mean', 'Median', '.25 Percentile', '.75 Percentile', 'Standard Deviation')

    for i in range(1, len(head)+1):
        sheet.cell(row=1, column=i*5-3, value=str(head[i-1]))

    sheet.cell(row=2, column=1, value='FamilyMart Store')
    for i in range(1, len(header)*3+1):
        sheet.cell(row=2, column=i+1, value=str(header[(i-1)%5]))
    sheet.cell(row=2, column=17, value='Number of Listing')

    for key, value in statistic.items():
        # print(value.size)
        sheet.append([key, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10], value[11], value[12], value[13], value[14], value[15]])

    workbook.save(file)
    workbook.close()

def set_constant(config):
    """
    Set up all the constant in this script
    """

    WebScraping.MAX_DISPLACEMENT = int(config['Constant']['max_displacement'])

def opt():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--site", type=str, default="propertyguru")
    parser.add_argument("-con", "--config", type=str, default="config.ini")
    parser.add_argument("-m", "--market", type=str, default="COMMERCIAL")

    return parser.parse_args()

def main(args):
    """
    Select which site to scrap
    Input: args.site - The site to scrap
    Output: .xlsx file containing the scrap information of the site and its summary
    """


    # print(args.filter)
    if args.site == "propertyguru":
        from web_scraping_scripts.database_propertyguru import Database
        set_constant(config)
        wb = Workbook(('Store Name', 'Name', 'Description', 'Price', 'Size', 'Psf', 'Reference', 'Address', 'Displacement'))
        ws = WebScraping(config['Link']['base_url_propertyguru'], args.site, Database, wb, args.market, config['File']['filter_file_propertyguru'])
        web_scraping_propertyguru(ws)
    elif args.site == "hartamas":
        from web_scraping_scripts.database_hartamas import Database
        wb = Workbook(("Name", "Address", "Size", "Storey", "Psf", "Reference"))
        ws = WebScraping(config['Link']['base_url_hartamas'], args.site, Database, wb)
        web_scraping_hartamas(ws)
    elif args.site == "iproperty":
        from web_scraping_scripts.database_iproperty import Database
        wb = None
        ws = WebScraping(config['Link']['base_url_iproperty'], args.site, Database, wb)
        ws.cont.connect(ws.base_url)
        # web_scraping_iproperty(ws)
    
    else:
        print(f"There site {args.site} is not supported")
        sys.exit(0)
                  
if __name__ == "__main__":
    args = opt()
    print(args)

    main(args)

    # analyse_data("sheets/Family Mart Rental Information2.xlsx")