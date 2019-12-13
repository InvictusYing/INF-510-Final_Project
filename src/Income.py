# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 23:33:02 2019

@author: admin
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
url = 'http://www.laalmanac.com/employment/em12c.php'
income = []
path = 'Los_Angeles_City_Zip_Codes.csv'
zipcode = []
try:
    with open(path,'r') as f:
        for line in f:
            zipcode.append(line.split(',')[2])
except:
    print('file does not find')
    
try:
    r = requests.get(url)
    r.raise_for_status
except requests.exceptions.HTTPError as e:
    print(e)
else:
    soup = BeautifulSoup(r.text,'lxml')

tbody = soup.find('tbody')

for i in tbody.find_all('tr'):
    data = []
    if i.find('td',{'class':"text-left"}).contents[0] == None:
        data.append('NULL')
    else:
        data.append(i.find('td',{'class':"text-left"}).contents[0])
    if i.find_all('td')[2].contents[0][1:].replace(',','') == None:
        data.append('NULL')
    else:
        data.append(int(i.find_all('td')[2].contents[0][1:].replace(',','')))
    income.append(data)
j = 0
city_income = []
for i in income:
    if i[0] in zipcode:
        data = []
        data.append(i[0])
        data.append(i[1])
        city_income.append(data)
#Create Raw_data Database to store raw data
conn = sqlite3.connect('Raw_Data.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS INCOME')
cur.execute('CREATE TABLE INCOME (id INTEGER, zipcode TEXT, income INTEGER)')
try:
    for i in city_income:
        cur.execute('INSERT INTO INCOME (id , zipcode, income)VALUES(?,?,?) ',(city_income.index(i),i[0],i[1]))
except:
    print('not work')
conn.commit()

# Create Analysis Database
conn = sqlite3.connect('Regression.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS INCOME')
cur.execute('CREATE TABLE INCOME (id INTEGER, zipcode TEXT, income INTEGER)')
try:
    for i in city_income:
        cur.execute('INSERT INTO INCOME (id , zipcode, income)VALUES(?,?,?) ',(city_income.index(i),i[0],i[1]))
except:
    print('not work')
conn.commit()