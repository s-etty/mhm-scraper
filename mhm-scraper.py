# pip3 freeze > requirements.txt
# pip3 install -r requirements.txt

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from pathlib import Path


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

# create an array of parking statuses
status_array = []
for element in parking_table:
    status = str(element.string)
    status_array.append(status)

now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

main = {"name" : "main",
        "time" : now, 
        "status" : status_array[0]
        }
sunrise = {"name" : "sunrise",
        "time" : now, 
        "status" : status_array[1]
        }
hrm = {"name" : "hrm",
        "time" : now, 
        "status" : status_array[2]
        }
twilight = {"name" : "twilight",
        "time" : now, 
        "status" : status_array[3]
        }

my_file = Path("log.txt")

if my_file.is_file():
    print(f"Adding scraped data from {now}")
else:
    print("log.txt not found")
    print("creating log.txt")
    file = open("log.txt", "a")
    file.write("log file for the scraper. Format is time, lot name, and lot status")