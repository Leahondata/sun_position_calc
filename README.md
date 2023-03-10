# Sun Positions Tracker
This project takes the user's IP address as input to return sun data relevant to their location, and displays the output to the console.

## Installation
After cloning the repository:
1. Make sure to activate the virtual environment. Can be installed by `pip install pipenv`.
2. Change directory to project directory.
3. Install dependencies by executing `pipenv install`.
4. Activate the virtual environment by executing `pipenv shell`.
5. If you are running the project from a code editor like VScode, restart the code editor to be able to see the new virtual enviroment. 

## Usage
To start the program, execute `sun_times_app.py`. 
The program `sun_times_app.py` will automatically return your location to you in the terminal output.
Next will follow the sun data based on that location.

The data output based on the user's IP location includes the following;
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
                          
Optionally, you can generate two CSV files;
  - One with the monthly data.
  - Another with the data for today's date only.

The default is set to not generate these CSV files. If you wish to generate them, you must update the final function within `sun_times_app.py`:
  Change`display_output` from `gen_csv=False` to `gen_csv=True`.
                          
## Working Examples

Output example of message to user for given location:

![image1](https://user-images.githubusercontent.com/124433926/224357845-a95d3749-6ed4-4c1d-b648-d1418db46a36.png)

Output example of message to user if a server is down:

![image2](https://user-images.githubusercontent.com/124433926/224357877-97e1d354-9782-42bf-b1f3-ee50ea1b0d29.png)

Optional CSV generated for monthly data:

![image3](https://user-images.githubusercontent.com/124433926/224357901-1bd2e4d3-9e11-44b1-8875-ff70dd143ef9.png)

Optional CSV generated for daily data:

![image4](https://user-images.githubusercontent.com/124433926/224357932-13fc9f07-c085-4d9b-9231-d8fad81225d1.png)


