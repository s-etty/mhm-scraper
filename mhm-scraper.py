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


#returns an array of lift statuses
def get_current_lift_status():
            lift_names = []
            lift_statuses = []
            lift_schedules = []
            lift_comments = []
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
            #write each row to a a txt file
            if Path("lifts.txt").is_file():
                print(f"Adding scraped data from {now}")
                file = open("lifts.txt", "a")
                for lift in lifts:
                    #extract the lift names, statuses, schedules, and comments
                    lift_name = lift.find('td', class_ = 'status-name').text
                    lift_status = lift.find('td', class_ = 'status-status').text
                    lift_schedule = lift.find('td', class_ = 'status-schedule').text
                    lift_comment = lift.find('td', class_ = 'status-comments').text
                    #write them to the file, separated by |
                    file.write(f"{now} | {lift_name} | {lift_status} | {lift_schedule} | {lift_comment}\n")
                file.close
            else:
                print("lifts.txt not found")
                print("creating lifts.txt")
                file = open("lifts.txt", "a")
                file.close

get_current_lift_status()
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
