# pip3 freeze > requirements.txt
# pip3 install -r requirements.txt

# mt hood location 
# lat: 45.3435
# long: -121.6722

# all available data for MHM at 6,540
# https://api.weather.gov/points/45.3435,-121.6722

# forecast for MHM at 6,540 ft
# https://api.weather.gov/gridpoints/PQR/142,88/forecast

# hourly forecast might me more useful... probably want to pull in current temp data 
# as well as some forecast data for maybe current, 9am, 10am, 12pm, 2pm, and 4pm? 
# that way we have a good idea of what the day is supposed to look like? idk... 
# https://api.weather.gov/gridpoints/PQR/142,88/forecast/hourly

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

# I think we can run this as a cron job... and it'll just automatically add to the log

now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# returns a dictionary of current conditions
def get_current_weather_conditions():
        url = 'https://api.weather.gov/gridpoints/PQR/142,88/forecast/hourly'
        response = requests.get(url).json()
        forecast = response['properties']['periods'][0]
        current_conditions = { 'temperature' : forecast['temperature'], 
                               'windspeed' : forecast['windSpeed'], 
                               'short_forecast' : forecast['shortForecast']
                               } 
        return current_conditions

print(get_current_weather_conditions())

# returns an array of parking statuses [main, sunrise, hrm, twilight]
def get_current_lot_conditions(): 
        #site URL
        url = "https://www.skihood.com/en/the-mountain/conditions"

        #get the HTML
        page = requests.get(url)
        #parse the HTML with beautifulsoup
        soup = BeautifulSoup(page.content, 'html.parser')

        #extract the parking lot table using class
        lot_table = soup.find_all('div', class_='conditions-info parking-lots')

        # extract parking status of each individual lot
        parking_table = lot_table[0].find_all('td', class_='status-status')

        # create an array of parking statuses [main, sunrise, hrm, twilight]
        status_array = []
        for element in parking_table:
                status = str(element.string)
                status_array.append(status)

        return status_array

status_array = get_current_lot_conditions()

# this is clunky, but whatever... it's all clunky.
main = {"name" : "Main",
        "time" : now, 
        "status" : status_array[0]
        }
sunrise = {"name" : "Sunrise",
        "time" : now, 
        "status" : status_array[1]
        }
hrm = {"name" : "Hrm",
        "time" : now, 
        "status" : status_array[2]
        }
twilight = {"name" : "Twilight",
        "time" : now, 
        "status" : status_array[3]
        }

# check to see if log.txt exists or not 
# if it exists, print the time, lot name, and lot status 
if Path("log.txt").is_file():
    print(f"Adding scraped data from {now}")
    file = open("log.txt", "a")
    file.write(f"{now} | {main['name'].ljust(8)} | {main['status']}\n")
    file.write(f"{now} | {sunrise['name'].ljust(8)} | {sunrise['status']}\n")
    file.write(f"{now} | {hrm['name'].ljust(8)} | {hrm['status']}\n")
    file.write(f"{now} | {twilight['name'].ljust(8)} | {twilight['status']}\n")
    file.close
# if log.txt does not exist, create it 
else:
    print("log.txt not found")
    print("creating log.txt")
    file = open("log.txt", "a")
    file.close
