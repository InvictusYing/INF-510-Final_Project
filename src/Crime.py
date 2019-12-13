#!/usr/bin/env python
# coding: utf-8

import requests
import csv
import pandas as pd
from sodapy import Socrata
from bs4 import BeautifulSoup

client = Socrata("data.lacity.org", None)
# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("63jg-8b9z", limit=3000000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_latlon = results_df.iloc[1895747:]

# Save Allthe Crime Data into CSV File
results_df.to_csv('Crime_2010-present.csv')
# Using Bing Maps API to transfer Latitude and Longitude into Zipcode
zipcode = []
BingMapsAPIKey = 'Avq4VbTxLlw2Zt9V8dcC5DmFCKMNZHasuyl51RrcTGxK3CY1Za8Ivulrlh8syjDI'
for i in range(1895747,len(results_latlon['lat'])+1895747):
    lat = results_latlon['lat'][i]
    lon = results_latlon['lon'][i]
    url = f'http://dev.virtualearth.net/REST/v1/Locations/{lat},{lon}?o=xml&key={BingMapsAPIKey}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    try:
        postalcode = soup.find('postalcode').contents[0]
        zipcode.append(postalcode)
        print(len(results_latlon['lat'])-i+1895747)
    except:
        print('Error')
        zipcode.append('-1')

zipcode_df = pd.DataFrame(zipcode)
zipcode_df.to_csv('Crime_zipcode.csv')
crime_2019 = results_df.iloc[1895747:]
crime_zipcode = pd.read_csv('Crime_zipcode.csv')
crime_zipcode = crime_zipcode.rename(columns={'0':'Zipcode'})
crime_zipcode_list = list(crime_zipcode['Zipcode']) 
crime_2019['Zipcode']=crime_zipcode_list

crime_2019.to_csv('Crime_2019.csv')



