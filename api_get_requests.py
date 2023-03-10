import requests
import unicodedata
from api_key import api_key
import sys


def detect_location():
    '''
    Detects the location details of the user by making API requests utilizing their IP address in.
    If the request fails, the user is notified and the program exits.

    Parameters:
    None.

    Returns:
    dict: A dictionary containing the following keys:
            - 'City': The city name of the user's ISP location.
            - 'Region': The region name of the user's ISP location.
            - 'IP': The IP address of the user's ISP location.

    Raises:
    requests.exceptions.HTTPError: If the request fails due to an invalid response code, it will notify the user and exits the program.
    '''
    loc_details = {}
    api_url = 'http://ipinfo.io/json'
    response = requests.get(api_url)
    check_response_code(response.status_code, api_url)
    loc_details['City'] = response.json()['city']
    loc_details['Region'] = response.json()['region']
    loc_details['IP'] = response.json()["ip"]
    return loc_details


def get_additional_loc_data(loc_details):
    '''(dict) -> dict

    Retrieves additional location data by making API requests based on the location details in the dictionary, and adds it to the dictionary.
    If the request fails, the user is notified and the program exits.

    Parameters:
    loc_details (dict): A dictionary containing the location details, including the IP address.

    Returns:
    dict: The updated dictionary with the additional keys:
            - 'Country_Name': The country name of the user's ISP location.
            - 'Date_Time': The date and time of the user's ISP location.

    Raises:
    requests.exceptions.HTTPError: If the request fails due to an invalid response code, it will notify the user and exits the program.
    '''
    api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={loc_details["IP"]}'
    response = requests.get(api_url)
    check_response_code(response.status_code, api_url)
    loc_details['Country_Name'] = response.json()['country_name']
    loc_details['Date_Time'] = response.json()['time_zone']['current_time']
    return loc_details


def convert_to_ascii(loc_str):
    '''(str) -> str

    Converts a string to ASCII equivalents if the sting is not already in ASCII format.

    Parameters:
    loc_str (str): The input string to be converted to ASCII.

    Returns:
    str: The converted string in ASCII format.
    '''
    if not loc_str.isascii():
        normalized_data = unicodedata.normalize('NFKD', loc_str)
        loc_str = normalized_data.encode('ascii', 'ignore').decode('ascii')
    return loc_str


def check_response_code(response_code, url):
    '''(int, str) -> None

    Checks the response of an HTTP request.
        If the response is not 200, it notifies the user and exits the program.
        If the response is 200, the fuction does nothing.

    Parameters:
    response_code (int): The response code of an HTTP request.
    url (str): The URL of the HTTP request.

    Returns:
    None.
    '''
    if response_code != 200:
        print('\n----------------------------------------------------------------')
        print(f'{url} is currently down.\nPlease try again in a few minutes.')
        print('----------------------------------------------------------------\n')
        sys.exit()
