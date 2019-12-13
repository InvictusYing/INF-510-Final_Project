# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 23:36:10 2019

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
        return ['NULL', 'NULL']

#Trader Joe's

url = 'https://locations.traderjoes.com/ca/los-angeles/'

try:
    r = requests.get(url)
    r.raise_for_status
except requests.exceptions.HTTPError as e:
    print(e)
else:
    soup = BeautifulSoup(r.content, 'lxml')

tj_data={'name':[],'address':[],'city':[],'state':[],'zipcode':[],'nation':[],'lat':[],'long':[]}
try:
    for i in soup.findAll('div',{'class': "itemlist"}):
        if i.find('strong').find('span').contents[2].strip( ) == None:
            tj_data['name'].append('NULL')
        else:
            tj_data['name'].append(i.find('strong').find('span').contents[2].strip( ))
            
        if i.findAll('span')[1].contents[0] == None:
            tj_data['address'].append('NULL')
        else:  
            tj_data['address'].append(i.findAll('span')[1].contents[0])
        
        if i.findAll('span')[2].contents[0] == None:
            tj_data['city'].append('NULL')
        else:
            tj_data['city'].append(i.findAll('span')[2].contents[0])
        
        if i.findAll('span')[3].contents[0] == None:
             tj_data['state'].append('NULL')
        else:
            tj_data['state'].append(i.findAll('span')[3].contents[0])
            
        if i.findAll('span')[4].contents[0] == None:
            tj_data['zipcode'].append('NULL')
        else:
            tj_data['zipcode'].append(i.findAll('span')[4].contents[0])
            
        if i.findAll('span')[5].contents[0] == None:
            tj_data['nation'].append('NULL')
        else: 
            tj_data['nation'].append(i.findAll('span')[5].contents[0])
    for i in tj_data['address']:
        tj_data['lat'].append(get_coordinates(i)[0])
        tj_data['long'].append(get_coordinates(i)[1])
except:
    print('div does not find')
    
# Transfer Trade Joe's Data into SQL
conn = sqlite3.connect('Raw_Data.db')
cur = conn.cursor()

try:
# Insert the data into database
    for i in range(0,len(tj_data['name'])):
        cur.execute('INSERT INTO Markets (id, Address, Zipcode, Lat, Long) VALUES (?,?,?,?,?)',
                (i, tj_data['address'][i],tj_data['zipcode'][i],tj_data['lat'][i],tj_data['long'][i]))
except:
    cur.execute('DROP TABLE IF EXISTS Markets')
    cur.execute('CREATE TABLE Markets (id INTEGER, Address TEXT, Zipcode INTEGER, Lat INTEGER, Long INTEGER)')
    for i in range(0,len(tj_data['name'])):
        cur.execute('INSERT INTO Markets (id, Address, Zipcode, Lat, Long) VALUES (?,?,?,?,?)',
                (i, tj_data['address'][i],tj_data['zipcode'][i],tj_data['lat'][i],tj_data['long'][i]))

#cur.execute('DELETE FROM Restaurants WHERE restuarant_id < 10000')
conn.commit()