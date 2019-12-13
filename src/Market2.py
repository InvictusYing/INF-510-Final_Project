# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 23:38:26 2019

@author: admin
"""
import requests
from bs4 import BeautifulSoup
import sqlite3
import googlemaps
KEY = 'AIzaSyCHc3Bob61IZhnZ13_MDtW1nrm2OFdWatY'
gmaps = googlemaps.Client(key=KEY)

def get_coordinates(address):
    #city = '<City Name>, <Country>'
    geocode_result = gmaps.geocode(str(address))
    if len(geocode_result) > 0:
        return list(geocode_result[0]['geometry']['location'].values())
    else:
        return ['NULL','NULL']

#CSV

url = 'https://www.cvs.com/store-locator/cvs-pharmacy-locations/California/Los-Angeles'

try:
    r = requests.get(url)
    r.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(e)
else:
    soup = BeautifulSoup(r.content, 'lxml')

csv_data={'address':[],'zipcode':[],'lat':[],'long':[]}
try:
    
    for i in soup.findAll('div', {"class":"each-store" }):
        if i.find('p').contents[0].strip()[:-6] == None:
            csv_data['address'].append('NULL')
        else:
            csv_data['address'].append(i.find('p').contents[0].strip()[:-6])
        
        if i.find('p').contents[0].strip()[-5:] == None:
            csv_data['zipcode'].append('NULL')
        else:
            csv_data['zipcode'].append(i.find('p').contents[0].strip()[-5:])
    for i in csv_data['address']:
        csv_data['lat'].append(get_coordinates(i)[0])
        csv_data['long'].append(get_coordinates(i)[1])
except:
    print('div does not find')
# Transfer CVS Data into SQL
conn = sqlite3.connect('Markets.db')
cur = conn.cursor()

conn = sqlite3.connect('Raw_Data.db')
cur = conn.cursor()

#cur.execute('DROP TABLE IF EXISTS Markets')
#cur.execute('CREATE TABLE Markets (id INTEGER, Address TEXT, Zipcode INTEGER, Lat INTEGER, Long INTEGER)')

# Insert the data into database
try:
    for i in range(0,len(csv_data['zipcode'])):
        cur.execute('INSERT INTO Markets (id, Address, Zipcode, Lat, Long) VALUES (?,?,?,?,?)',
                (i, csv_data['address'][i],csv_data['zipcode'][i],csv_data['lat'][i],csv_data['long'][i]))
except:
    cur.execute('CREATE TABLE Markets (id INTEGER, Address TEXT, Zipcode INTEGER, Lat INTEGER, Long INTEGER)')
    for i in range(0,len(csv_data['zipcode'])):
        cur.execute('INSERT INTO Markets (id, Address, Zipcode, Lat, Long) VALUES (?,?,?,?,?)',
                (i, csv_data['address'][i],csv_data['zipcode'][i],csv_data['lat'][i],csv_data['long'][i]))

#cur.execute('DELETE FROM Restaurants WHERE restuarant_id < 10000')
conn.commit()