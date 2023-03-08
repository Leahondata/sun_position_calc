# Sun Positions Tracker
This project takes the user's IP address as input to return sun data relevant to their location, and displays the output to the console.

## Installation
After cloning the repository:
1. Make sure to activate the virtual environment. Can be installed by 'pip install pipenv'.
2. Change directory to project directory.
3. Install dependencies by executing 'pipenv install'.
4. Activate the virtual environment by executing `pipenv shell`.
5. If you are running the project from a code editor like VScode, restart the code editor to be able to see the new virtual enviroment. 

## Usage
The program will automatically return your location to you in the terminal output.
Next will follow the sun data based on that location.

The data output based on the user's IP location includes the following:
- Day                             WEEKDAY, MONTH, DAY 
- Twilight start                  HH:MM:SS am/pm
- Sunrise                         HH:MM:SS am/pm
- Sunset                          HH:MM:SS am/pm
- Twilight end                    HH:MM:SS am/pm
- Day length                      HH:MM:SS
- Solar noon                      HH:MM:SS am/pm
- Nautical twilight       Start   HH:MM am/pm
                          End     HH:MM am/pm
- Astronomical twilight   Start   HH:MM am/pm
                          End     HH:MM am/pm
                          
## Working Examples

Output example of message to user for given location:

![image1](https://user-images.githubusercontent.com/124433926/223827801-d9bfb236-9536-4299-b328-0001f016fb4c.png)

Output example of message to user if the API server is down:

![image2](https://user-images.githubusercontent.com/124433926/223827735-6fcd355b-381d-4d1a-b753-cacb1402df1a.png)
