from api_get_requests import loc_details
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys

# Detect location of user using their IP address.
print('\n--------------Your location--------------')
print(f"\n{loc_details['City']},")
print(f"{loc_details['Region']},")
print(f"{loc_details['Country_Name']}.")


# Create and return url with imported data from location_detector.
url = (f"https://sunrise-sunset.org/search?location={loc_details['City']}")


# Make the request using the generated IP address.
response = requests.get(url)
status = response.status_code


# Handle error codes.
if status != 200:
    print('\n----------------------------------------------------------------')
    print('The server is currently down. Please try again in a few minutes.')
    print('----------------------------------------------------------------\n')
    sys.exit()


# Convert response to beautiful soup object.
soup_object = BeautifulSoup(response.content, 'html.parser')


# Find the table to scrape data from.
table = soup_object.find('table', {'id': 'month'})


# Extract the table data and save it in a variable.
table_data = [[cell.text.strip() for cell in row.find_all('td')]
              for row in table.find_all('tr')]


# Extract column headers.
headers_data = []
for header in table.find_all('th'):
    headers_data.append(header.text.strip())


# Separate header titles from days of the month.
def separate_headers(headers_data):
    header_titles = headers_data[:8]
    header_titles.insert(8, '')
    header_titles.extend([headers_data[8], ''])
    sub_headers = [''] * 7 + headers_data[9:13]
    month_days = headers_data[13:]
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


# Print the specified date with clean formatting for visibility.
row = df.loc[today_single].to_frame().rename(columns={7: ''})
print(row)
print('-----------------------------------------', '\n')
