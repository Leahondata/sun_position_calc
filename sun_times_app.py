from api_get_requests import loc_details
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests


# Detect location of user using their IP address and notify them of the location they have been located at.
print(
    f"\n--------------Your location--------------\n\n{loc_details['City']}, \n{loc_details['Region']}, \n{loc_details['Country_Name']}.")


# Create and return url with imported data from location_detector.
url = (f"https://sunrise-sunset.org/search?location={loc_details['City']}")
print(url)


# Get HTML from url using HTML request to get json data.
response = requests.get(url)
print(response)


# Convert response to beautiful soup object.
soup_object = BeautifulSoup(response.content, 'html.parser')


# Find the table to scrape data from.
table = soup_object.find('table', {'id': 'month'})


# Extract the table data and save it in a variable.
table_data = [[cell.text.strip() for cell in row.find_all('td')]
              for row in table.find_all('tr')]
# Optimized the code above from the previous code below:
# table_data = []
# for row in table.find_all('tr'):
# row_data = []
# for cell in row.find_all('td'):
# row_data.append(cell.text.strip())
# table_data.append(row_data)


# Extract column headers.
headers_data = []
for header in table.find_all('th'):
    headers_data.append(header.text.strip())


# Separate header titles from days of the month.
def separate_headers(headers_data):
    header_titles = headers_data[:8]
    header_titles.insert(7, '')
    header_titles.extend([headers_data[8], ''])

    sub_headers = [''] * 7 + headers_data[9:13]

    month_days = headers_data[13:]
# Optimized the code above from the previous code below:
    # for i in headers_data[:8]:
    #     header_titles.append(i)
    # for i in headers_data[7:8]:
    #     header_titles.append('')
    # for i in headers_data[8:9]:
    #     header_titles.append(i)
    #     header_titles.append('')

    # for i in headers_data[:7]:
    #     sub_headers.append('')
    # for i in headers_data[9:13]:
    #     sub_headers.append(i)

    # for i in headers_data[13:]:
    #     month_days.append(i)
    return header_titles, sub_headers, month_days


header_titles, sub_headers, month_days = separate_headers(headers_data)


# Delete the first two empty lists within table_data.
del table_data[:2]


# Combine month_days and table_data into one list to pass to dataframe.
data = [[month_days[i]] + table_data[i] for i in range(len(month_days))]


# Combine header_titles and sub_headers into one list to pass to dataframe.
headers = pd.MultiIndex.from_arrays([header_titles, sub_headers])


# Create dataframe to organize and store data in.
df = pd.DataFrame(data, columns=headers)


# Create CSV and save data for month in CSV file.
df.to_csv("sun_data_by_loc.csv", index=False)


# Begin user output message.
print("---------------Today's data--------------")


# Get today's date from loc_details['Date_Time'].
today_single = int(loc_details['Date_Time'].split(' ')[0].split('-')[2]) - 1
# Optimized the code above from the previous code below:
# split_date_time = loc_details['Date_Time'].split(' ')
# date = split_date_time[0]
# year_month_day = date.split('-')
# today = year_month_day[2]
# today_single = (int(today)-1)


# Print the specified date with clean formatting for visibility.
row = df.loc[today_single].to_frame().rename(columns={6: ''})
print(row)
print('-----------------------------------------', '\n')
