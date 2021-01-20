import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import time
from datetime import timedelta
from pathlib import Path


# returns some soup
def get_soup():
        #site URL
        url = "https://www.skihood.com/en/the-mountain/conditions"
        #get the HTML
        page = requests.get(url)
        #parse the HTML with beautifulsoup
        return BeautifulSoup(page.content, 'html.parser')

soup = get_soup()
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

#extracts the blurbs from several spots on the page and stores them in a .txt file
def get_current_blurb():
            #extract the header blurb container
            header_container = soup.find('div', class_ = 'conditions-snapshot')
            #extract the header blurb text
            header_blurb = header_container.find('h1').text
            #return the header blurb text
            return(header_blurb)

#extracts the current snow conditions
def get_current_snow():
            #extract the container for the snow conditions
            snow_conditions_container = soup.find('div', class_ = 'conditions-info surface-conditions')
            #get the text of the snow conditions
            snow_conditions = snow_conditions_container.find('dd').text
            #return the snow_conditions
            return(snow_conditions)

#extracts the lift status info and writes it to a txt file for storage
def get_current_lift_status():
            #extract the lift status table
            lift_table = soup.find('div', class_ = 'conditions-info lift-operations')
            #get the body of the table
            lift_table_body = lift_table.find('tbody')
            #get all the rows from the body of the table
            lifts = lift_table_body.find_all('tr')
            #return the lift statuses
            return(lifts)

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

def write_to_lift_log():
        lifts = get_current_lift_status()
        #check if lifts.txt file exists
        if Path("lifts.txt").is_file():
            file = open("lifts.txt", "a")
            #write each row to the lifts.txt file
            for lift in lifts:
                #extract the lift names, statuses, schedules, and comments
                lift_name = lift.find('td', class_ = 'status-name').text
                lift_status = lift.find('td', class_ = 'status-status').text
                lift_schedule = lift.find('td', class_ = 'status-schedule').text
                lift_comment = lift.find('td', class_ = 'status-comments').text
                #write them to the file, separated by |
                file.write(f"{now} | {lift_name} | {lift_status} | {lift_schedule} | {lift_comment}\n")
            file.close
        #if the log doesn't exist, create it.
        else:
            print("lifts.txt not found")
            print("creating lifts.txt")
            file = open("lifts.txt", "a")
            #include column names
            file.write("date_collected | name | status | schedule | comment\n")
            file.close

def write_to_blurb_log():
        header_blurb = get_current_blurb()
        snow_conditions = get_current_blurb()
        #check if the file is there
        if Path("blurb.txt").is_file():
            file = open("blurb.txt", "a")
            #write them to the file, separated by |
            file.write(f"{now} | {header_blurb} | {snow_conditions}\n")
            file.close
        #if the log doesn't exist, create it.
        else:
            print("blurb.txt not found")
            print("creating blurb.txt")
            file = open("blurb.txt", "a")
            #include column names
            file.write("date_collected | blurb | snow_conditions\n")
            file.close

write_to_lot_log()
#schedule this to run at 7:30 AM
scheduled_hour = 7
scheduled_minute = 30
#use the current datetime object to get the hour and minute
now_dt = datetime.now()
minute = now_dt.minute
hour = now_dt.hour
#if the hour is 7 and the minute is 30, write to the files
#else do nothing
if minute == scheduled_minute and hour == scheduled_hour:
    write_to_lift_log()
    write_to_blurb_log()
