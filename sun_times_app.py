from bs4 import BeautifulSoup
import api_get_requests as agr
import pandas as pd
import requests
import sys


def detect_location():
    '''
    Detects the location of the user and returns a dictionary of location data.

    Parameters:
    None.

    Returns:
    dict: A dictionary containing the following keys:
            - 'City': The city name of the user's ISP location.
            - 'Region': The region name of the user's ISP location.
            - 'IP': The IP address of the user's ISP location.
            - 'Country_Name': The country name of the user's ISP location.
            - 'Date_Time': The date and time of the user's ISP location.

    Raises:
    requests.exceptions.HTTPError: If the request fails due to an invalid response code, it will notify the user and exits the program.
    '''
    temp_dict = agr.detect_location()
    temp_dict = agr.get_additional_loc_data(temp_dict)
    temp_dict['City'] = agr.convert_to_ascii(temp_dict["City"])
    return temp_dict


def construct_scraper_url(city_str):
    '''(str) -> str

    Constructs and returns a URL for webscraping application that retrieves sun data based on the detected location.

    Parameters:
    city_str (str): The name of the city to be passed into the creation of the URL.

    Returns:
    str: A string representing the created URL to be used in webscraping application.
    '''
    url = (f"https://sunrise-sunset.org/search?location={city_str}")
    return url


def request_data(url):
    '''(str) -> bs4.BeautifulSoup

    Sends an HTTP request to the specified URL and returns the response as a Beautiful Soup object.

    Parameters:
    url (str): A string representing the created URL to be used in webscraping application.

    Returns:
    bs4.BeautifulSoup: A Beautiful Soup object that contains the response content from the URL.

    Raises:
    requests.exceptions.HTTPError: If the request fails due to an invalid response code, it will notify the user and exits the program.
    '''
    print('\n')
    print('Fetching location data...')
    response = requests.get(url)
    agr.check_response_code(response.status_code, url)
    soup_object = BeautifulSoup(response.content, 'html.parser')
    return soup_object


def extract_table(page_content):
    '''(bs4.BeautifulSoup) -> bs4.element.Tag

    Extracts the HTML table containin the data to be scraped from the Beautiful Soup object and returns the table's data.

    Parameters:
    page_content (bs4.BeautifulSoup): A Beautiful Soup object that contains the response content from the URL.

    Returns:
    bs4.element.Tag: A Beautiful Soup Tag object representing the selected table.
    '''
    table = page_content.find('table', {'id': 'month'})
    return table


def parse_table_data(table_data):
    '''(bs4.element.Tag) -> tup

    Parses the contents of the HTML table that is represented by a Beautiful Soup Tag object, extracting the table data and column headers.

    Parameters:
    table_data (bs4.element.Tag): A Beautiful Soup Tag object representing the selected table to be parsed.

    Returns:
    tuple: [lst[lst[str]]], lst[str]: A tuple containing two lists;
            - The table data as a list of rows where each row is represented as a list of stings.
            - The column headers as a list of stings.
    '''
    table_list = [[cell.text.strip() for cell in row.find_all('td')]
                  for row in table_data.find_all('tr')]
    headers_list = [header.text.strip()
                    for header in table_data.find_all('th')]
    return table_list, headers_list


def separate_headers(headers_data):
    '''(lst[str]) -> tup

    Separate header titles from subheaders and days of the month.

    Parameters:
    headers_data (lst of str): The column headers as a list of strings to separate.

    Returns:
    tuple: lst[str], lst[str], lst[str]: A tuple containing three lists:
            - The separated header titles.
            - The separated subheaders.
            - The separated days of the month.
    '''
    header_titles = headers_data[:8]
    header_titles.insert(8, '')
    header_titles.extend([headers_data[8], ''])
    sub_headers = [''] * 7 + headers_data[9:13]
    month_days = headers_data[13:]
    return header_titles, sub_headers, month_days


def construct_df(table_list, header_titles, month_days):
    '''(lst[str], lst[str], lst[str]) -> DataFrame

    Organize the data and then create the data frame using the data in the organized lists.

    Parameters:
        table_list (lst[str]): The list of data to construct the data frame with.
        header_titles (lst[str]): The header titles to use for the data frame.
        month_days (lst[str]): The days of the month to use in the data frame.

    Returns:
    DataFrame: A pandas DataFrame containing the organized data.
    '''
    del table_list[:2]
    data = [[month_days[i]] + table_list[i] for i in range(len(month_days))]
    headers = pd.MultiIndex.from_arrays([header_titles, sub_headers])
    df = pd.DataFrame(data, columns=headers)
    return df


def display_output(df, loc_dict, gen_csv=False):
    '''(df, dict, bool) -> None

    Displays the location details, fetches the data for today's date based on those location details, and prints it to the console.
    Optionally generates two CSV files.
        If gen_csv is True, the function generates two CSV files:
            - One with the monthly data by location.
            - Another with the data for today's date only.

    Parameters:
        df (DataFrame): A pandas Dataframe containing the data to display.
        loc_dict (dict): A dictionary containing the location details, including the city, region, country name and date/time.
        gen_csv (bool): A flag indicating whether to generate a CSV file or not. Default is False.

    Returns:
    None.
    '''
    print('--------------Your location--------------')
    print(f"\n{loc_dict['City']},")
    print(f"{loc_dict['Region']},")
    print(f"{loc_dict['Country_Name']}.")
    print('-----------------------------------------')
    print('\n')

    print('Fetching data based on your location...')

    today = int(loc_dict['Date_Time'].split(' ')[0].split('-')[2]) - 1

    print("---------------Today's data--------------")
    row = df.loc[today].to_frame()
    empty_header = ['']
    row.columns = empty_header
    print(row)
    print('-----------------------------------------', '\n')
    if gen_csv:
        df.to_csv("monthly_data_by_loc.csv", index=True)
        row.to_csv('todays_data_by_loc.csv', index=True, header=None)


location_data = detect_location()

webpage_raw_data = construct_scraper_url(location_data['City'])

webpage_soup_object = request_data(webpage_raw_data)

table_data = extract_table(webpage_soup_object)

table_list, headers_list = (parse_table_data(table_data))

header_titles, sub_headers, month_days = separate_headers(headers_list)

df = construct_df(table_list, header_titles, month_days)

display_output(df, location_data, gen_csv=True)