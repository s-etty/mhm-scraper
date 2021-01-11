import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

#site URL
url = "https://www.skihood.com/en/the-mountain/conditions"

#get the HTML
page = requests.get(url)
#parse the HTML with beautifulsoup
soup = BeautifulSoup(page.content, 'html.parser')

#extract the parking lot table using class
lot_status = soup.find_all('div', class_='conditions-info parking-lots')
