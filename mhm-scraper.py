# pip3 freeze > requirements.txt
# pip3 install -r requirements.txt

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

# I think we can run this as a cron job... and it'll just automatically add to the log

now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

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


#extracts the blurbs from several spots on the page and stores them in a .txt file
def get_current_blurb():
            #site URL
            url = "https://www.skihood.com/en/the-mountain/conditions"
            #get the HTML
            page = requests.get(url)
            #parse the HTML with beautifulsoup
            soup = BeautifulSoup(page.content, 'html.parser')
            #extract the header blurb container
            header_container = soup.find('div', class_ = 'conditions-snapshot')
            #extract the header blurb text
            header_blurb = header_container.find('h1').text
            #check if header_blurb.txt file exists

            #extract the container for the snow conditions
            snow_conditions_container = soup.find('div', class_ = 'conditions-info surface-conditions')
            #get the text of the snow conditions
            snow_conditions = snow_conditions_container.find('dd').text

            #check if the file is there
            if Path("blurb.txt").is_file():
                print(f"Adding scraped data from {now}")
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

#extracts the lift status info and writes it to a txt file for storage
def get_current_lift_status():
    #site URL
    url = "https://www.skihood.com/en/the-mountain/conditions"
    #get the HTML
    page = requests.get(url)
    #parse the HTML with beautifulsoup
    soup = BeautifulSoup(page.content, 'html.parser')
    #extract the lift status table
    lift_table = soup.find('div', class_ = 'conditions-info lift-operations')
    #get the body of the table
    lift_table_body = lift_table.find('tbody')
    #get all the rows from the body of the table
    lifts = lift_table_body.find_all('tr')
    #check if lifts.txt file exists
    if Path("lifts.txt").is_file():
        print(f"Adding scraped data from {now}")
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
