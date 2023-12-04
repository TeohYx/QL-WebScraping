# QL-WebScraping
This codes are able to scrap data from website, mainly for property site using Beautiful Soup, along with cloudscraper as tool to bypass cloudflare.

On top on scraping, it also can filter out data in respect of the displacement between the scraped listing's address and the given list's address.

The tool used to extract the longitude/latitude is *www.geoapify.com*.

1. Install the package from the requirements.txt

```
pip install -r requirements.txt
```

2. Run the scripts.

```
python main.py
```

Note: The website to scrap can be chosen, so far the script supported 3 website, which are - 
1. PropertyGuru - "propertyguru"
2. EdgeProp - "edgeprop"
3. iProperty - "iproperty"

As this scripts will scrape data based on the given location, therefore the location need to be specified. 

```
(Store No	Store Name	Address	formatted_address_google	location_lat	location_lng	Coordinate)
```

To scrap the website, mention it when running the script.

```
python main.py -s "edgeprop"
```

To enable auto generation of statistic analysis, add the -a argument.

```
python main.py -s "propertyguru" -a "yes"
```
Alternatively, the analysis can be run separately from the main script.
```
python analysis.py -f {output_file}.xlsx
```
Note that the file should be in .xlsx extension.

The script runs propertyguru by default.

** For changing the setting such as the destination file, etc. can refer to the **config.ini** file


------------------------------------------------------------------------------------------------

To scrape a new website, the following steps should be followed:

1. Add **filter_{site}.txt** in filter/ directory.

In the txt file, include the locations in which the nearby rental information is wishes to find out, and the filters dedicated to the website accordingly (e.g. LOCATION FILE, LISTING, PROPERTY)<br>

2. Update **config.ini** 

Things to update: filter_file_{site}, output_file_{site}, base_url_{site}<br>

3. Update **content.py**

Add new method to connect the new website url and make sure it can get the HTML content from the website.<br>
If the website is static, BeautifulSoup alone is needed.<br>
However most website are dynamic nowadats, therefore Selenium is requried as it have a function of wait until the web page loaded before extract the HTML content.<br>

4. On main, add more conditions for the newly added website.

a. Specify the location of Database<br>
b. Specify the location of RentalURL<br>
c. Initialize Workbook instance (add header) - For convienience purposes, as the website scraped usually have 3 main data - Price, Size, psf, therefore it is recommend to assign them in 4th, 5th and 6th position. (1, 2, 3, 4, 5, 6,...). To change the position, the position should be also change in the 'analysis.py' file.<br>
d. Initialize WebScraping instance - Provide base url, site name, database, workbook, rentalurl, whether to perform analysis, and filter file<br>
e. Add ***web_scraping_{site}*** and ***iterate_page_{site}*** methods in main. Modify related object into the current website. Some important thing to modify are the tag for identifying last page, and tag to get the next page link.<br>

5. Modify created rental_url_{site}.py

Every website have different query parameters, therefore a new rental_url.py need to be created to handle each of the website.<br>
In the new **rental_url_{site}.py**, modify the url by changing the query parameter accordingly so that the output url is workable.<br>

6. Modify created database_{site}.py

Based on the web content, modify the tags accordingly and test it until they work accordingly.<br>

7. Add method for the site in workbook.py

Lastly, the destination on place to store data need to modify as well, as the column of the shees would varies between website and perferences. <br>

--------------------------------------------------------------------------------------------------------------------------------

All result can be calculated and a file can be generated through **combine_file.py** 
```
python combine_file.py -l "output/Result_Edgeprop.xlsx" "output/Result_Iproperty.xlsx" "output/Result_Propertyguru.xlsx" -o "out.xlsx"
```

Where -l stores a list of file to be combine.
      -o specific an output file

The output is a .xlsx file with combined listings based on given location along with a summary 