# Meadows Parking Scraper

This scraper will pull parking lot status from the [Mt. Hood Meadows conditions page](https://www.skihood.com/en/the-mountain/conditions). When there is enough data, a predictive model will be created to determine if and when the parking lots will fill.

To run: 

1. clone the repo 
2. create a virtual environment `virtualenv env`
3. source the virtual environment script `source env/bin/activate`
4. install requirements `pip install -r requirements.txt`
5. run script `python mhm-scraper.py`
6. a log file should be generated. new information will be appended each time script is run. 