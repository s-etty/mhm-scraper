import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path


# returns some soup
def get_soup(): 
        #site URL
        url = "https://www.skihood.com/en/the-mountain/conditions"
        #get the HTML
        page = requests.get(url)
        #parse the HTML with beautifulsoup
        return BeautifulSoup(page.content, 'html.parser')

now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
soup = get_soup()

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

# returns an array of parking statuses [main, sunrise, hrm, twilight]
def get_current_lot_conditions(): 
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


def write_to_lot_log():
        status_array = get_current_lot_conditions()
        conditions = get_current_weather_conditions()

        # check to see if log.txt exists or not 
        # if it exists, print the time, lot name, and lot status 
        if Path("log.txt").is_file():
                print(f"Adding scraped data from {now}")
                file = open("log.txt", "a")
                file.write(f"{now} | {'Main'.ljust(8)} | {status_array[0].ljust(7)} | {str(conditions['temperature']).ljust(3)} | {conditions['windspeed'].ljust(7)} | {conditions['short_forecast']} \n")
                file.write(f"{now} | {'Sunrise'.ljust(8)} | {status_array[1].ljust(7)} | {str(conditions['temperature']).ljust(3)} | {conditions['windspeed'].ljust(7)} | {conditions['short_forecast']} \n")
                file.write(f"{now} | {'HRM'.ljust(8)} | {status_array[2].ljust(7)} | {str(conditions['temperature']).ljust(3)} | {conditions['windspeed'].ljust(7)} | {conditions['short_forecast']} \n")
                file.write(f"{now} | {'Twilight'.ljust(8)} | {status_array[3].ljust(7)} | {str(conditions['temperature']).ljust(3)} | {conditions['windspeed'].ljust(7)} | {conditions['short_forecast']} \n")
                file.close
        # if log.txt does not exist, create it 
        else:
                print("log.txt not found")
                print("creating log.txt")
                file = open("log.txt", "a")
                file.close

write_to_lot_log()