import requests
import unicodedata


# API requests for city, region, and IP info.
api1 = 'http://ipinfo.io/json'
response = requests.get(api1)
city = response.json()['city']
region = response.json()['region']
ip = response.json()["ip"]


# Second API request for country name, date, and time info.
response4 = requests.get(
    f"https://api.ipgeolocation.io/ipgeo?apiKey=9c8f5da949d3451c87bf5893d60dc70d&ip={ip}")
country_name = response4.json()['country_name']
date_time = response4.json()['time_zone']['current_time']


# Check if input contains and ASCII characters.
def check_isascii(check_input):
    if check_input.isascii():
        updated_input = check_input
        # print(updated_input, 'is already correct format')
    else:
        # print(check_input, 'is not in the correct format')
        # normalize string input to NFKD form
        normalize = unicodedata.normalize('NFKD', check_input)
        # translate NFKD form to ASCII equivalents
        updated_input = normalize.encode('ascii', 'ignore').decode('ascii')
    return updated_input


# Dictionary to hold the accumulated data.
loc_details = {}
loc_details['City'] = check_isascii(city)
loc_details['Region'] = check_isascii(region)
loc_details['Country_Name'] = check_isascii(country_name)
loc_details['Date_Time'] = date_time
loc_details['IP'] = ip
