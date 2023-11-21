import requests
from math import sin, cos, sqrt, atan2, radians
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class Location:
    # Replace YOUR_API_KEY with your actual API key. Sign up and get an API key on https://www.geoapify.com/ 
    # API_KEY = config['API']['location_API']
    # R = float(config['Constant']['earth_radius'])  # Number                 
    API_KEY = None
    R = None       

    # Calculate the distance based on their longitude and latitude values
    @classmethod
    def distance(cls, coor1, coor2):
        lat1 = radians(float(coor1[0]))
        lon1 = radians(float(coor1[1]))
        lat2 = radians(float(coor2[0]))
        lon2 = radians(float(coor2[1]))

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = cls.R * c

        print("Result: ", round(distance, 2), "km")
        return distance

    # Call this function to get a return of distance between 2 location (address) in km
    @classmethod
    def distance_calculator(cls, fm_coordinate, address2):
        fm = fm_coordinate.split(',')
        print(f"First address is {fm[0], fm[1]} and the second one is {address2}")

        # Build the API URL
        url = config['Link']['geoapify_url_first'] + address2 + config['Link']['geoapify_url_last']
        # url2 = f"https://api.geoapify.com/v1/geocode/search?text={address2}&limit=1&apiKey={API_KEY}"

        response2 = requests.get(url)

        # Check the response status code
        if response2.status_code == 200:
            # Parse the JSON data from the response
            data = response2.json()
            # print(data)
            # Extract the first result from the data
            try:
                result = data["features"][0]
                # print(result)
            except:
                print("IndexOutOfRange")
                return 99

            # Extract the latitude and longitude of the result
            latitude2 = result["geometry"]["coordinates"][1]
            longitude2 = result["geometry"]["coordinates"][0]
            
        else:
            print(f"Request failed with status code {response2.status_code}")
            return 99

        coor1 = (fm[0], fm[1])
        coor2 = (latitude2, longitude2)

        # print(f"Latitude: {latitude}, Longitude: {longitude}")
        # print(f"Latitude2: {latitude2}, Longitude2: {longitude2}")
        return cls.distance(coor1, coor2)

if __name__ == "__main__":
    # Define the address to geocode
    address = "Lot G-01, Ground Floor, Wisma Lim Foo Yong, 86, Jalan Raja Chulan, 50200 Kuala Lumpur"
    address2 = "Jalan Ampang, KL City, Kuala Lumpur"

    l = Location()
    l.distance_calculator(address, address2)