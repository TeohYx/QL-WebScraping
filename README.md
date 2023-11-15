# QL-WebScraping
This codes are able to scrap data from website, mainly for property site using Beautiful Soup, along with cloudscraper as tool to bypass cloudflare.

On top on scraping, it also can filter out data in respect of the displacement between the scraped listing's address and the given list's address.

The tool used to extract the longitude/latitude is www.geoapify.com.

1. Install the package from the requirements.txt

```
pip install -r requirements.txt
```

2. Run the scripts.

```
python main.py
```

Note: The website to scrap can be chosen, so far the script supported 2 website, which are - 
1. PropertyGuru - "propertyguru"
2. Hartamas - "hartamas"

To scrap the website, mention it when running the script.

```
python main.py -s "hartamas"
```

To enable auto generation of statistic analysis, add the -a argument.
** Currently only supports propertyguru

```
python main.py -s "propertyguru" -a "yes"
```

The script runs propertyguru by default.

** For changing the setting such as the destination file, etc. can refer to the config.ini file

