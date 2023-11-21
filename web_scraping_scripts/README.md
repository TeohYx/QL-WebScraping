# Script Descriptions:

1. filter_data.py

This script extract the filters based on the filter file specified in filter/{filter_site}.txt<br>
It extracts <br>
a. Location file (the locations in a file where the information of its nearby rental listings will scrap if any)__
b. Listing type (the type of listings to extract)__
c. Property type (the type of property to extract) - The websites have 2 different ways in dealing with this type and the txt file are able to differentiate it accordingly:__
    i. All the property type are fits in an url - PROPERTY__
    ii. Only one property type can be filtered at a time in an url - PROPERTY SEPARATED__

2. rental_url_{site}.py

When the script is executed, it generates a URL incorporating all the specified filters from the instance variables in 'filter_data.py'.__
For example, in rental_url_propertyguru.py, the output would be <br>
```
    (self.base_url + self.place + self.listing_type + self.market + self.types)[:-1]
    # https://www.propertyguru.com.my/property-for-rent?freetext=ss15&listingtype=rent&market=COMMERCIAL&property_type_code[]=SHOP
```

3. content.py

This script take the given URL and access its web content in HTML form.__
The cloudflare is bypass using cloudscraper library.__
The content is extract using BeautifulSoup (for static web) and Selenium (for dynamic web)__

4. database_{site}.py

This script take the web content extracted in content.py and scrap all the useful information from it. __
As every website have different tag/class in its HTML, an effort of getting the specific tags is required when scraping new website.__

5. workbook.py

This script store the data scraped by 'database.py' into .xlsx file__

6. analysis.py

Upon finished storing the data in .xlsx file, this script can be called to analyze the data statistically (mean, median, standard deviation, etc).__