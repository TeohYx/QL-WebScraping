import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {}

config['Common'] = {
    'filter_folder' : '/filter',
    'sheets_folder' : '/sheets',
    'output_folder' : '/output'
}

config['File'] = {
    'filter_file' : '${Common:filter_folder}/filter.txt',
    'listing_type_file' : '${Common:filter_folder}/listing_type.txt',
    'store_info_file' : '${Common:sheets_foledr}/FMStore.csv',
    'output_file': '${Common:output_folder}/Family Mart Rental Information 2.xlsx'
}

config['API'] = {
    # Geoapify
    'location_API' : 'b104a894460741aa9c2fadd049c15d72',  
}

config['Link'] = {
    'base_url' : 'https://www.propertyguru.com.my/property-for-rent/?',
    'geoapify_url_first': 'https://api.geoapify.com/v1/geocode/search?text=',
    'geoapify_url_last': '&limit=1&apiKey=${API:location_API}'
}

config['Constant'] = {
    'earth_radius' : 6373.0,
    'max_displacement' : 1,
    'family_mart_checker' : 'FamilyMart',
    'retry_attempts' : 30
}

config['Input Header Title'] = {
    'first_column' : 'Store Name', 
    'second_column' : 'Name', 
    'third_column' : 'Description', 
    'fourth_column' : 'Price', 
    'fifth_column' : 'Size', 
    'sixth_column' : 'psf', 
    'seventh_column' : 'Reference', 
    'eighth_column' : 'Address', 
    'ninth_column' : 'Displacement'
}

config['Output Header Variable'] = {
    'first_variable' : 'Price',
    'second_variable' : 'Size',
    'third_variable' : 'Psf',
}

config['Output Header Title'] = {
    'first_column' : 'Mean',
    'second_column' : 'Median',
    'third_column' : '.25 Percentile',
    'fourth_column' : '.75 Percentile',
    'fifth_column' : 'Standard Deviation',
    'family_mart_store' : 'FamilyMart Store',
    'amount' : 'Number of Listing'
}


config['Tag'] = {
    'all_listing_cards' : 'div',
    'floor_area' : 'li',        # Contains room size and psf
    'address' : 'p',
    'name' : 'a',
    'price' : 'span',
    'description' : 'ul',
    'reference' : 'a'

}

config['Class'] = {
    'all_listing_cards' : 'listing-card',
    'floor_area' : 'listing-floorarea pull-left',
    'address' : 'listing-location ellipsis',
    'price' : 'price',
    'description' : 'listing-property-type',
    'reference' : 'nav-link',
    'last_page_indicator' : 'pagination-next disabled',
    'next_page' : 'pagination-next'
}

config['Attribute'] = {
    'name_title' : 'data-automation-id',
    'name_value' : 'listing-card-title-txt'
}

config['URL Attribute'] = {
    'place' : 'freetext=',
    'market' : 'market=',
    'listing_type' : 'listing_type=',
    'property_type' : 'property_type_code[]='
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)