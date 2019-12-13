# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 03:55:11 2019

@author: Yvaine_LI
"""

import sqlite3
import pandas
import csv

hprice = pandas.read_csv('median_housing_price.csv')
hprice_zip = hprice['Zipcode']
#For crime dataset
crime_count_list = []
crime = pandas.read_csv('Crime_2019.csv')
crime_count = crime.groupby('Zipcode').count()
for i in hprice_zip:
    data = []
    data.append(i)
    try:
        data.append(int(crime_count['area'][i]))
    except:
        data.append(0)
    crime_count_list.append(data)
#print(crime_count_list)

conn = sqlite3.connect('Regression.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS CRIME')
cur.execute("CREATE TABLE CRIME (zipcode INTEGER, count INTEGER)")
try:
    for i in crime_count_list: 
        cur.execute('INSERT INTO CRIME (zipcode, count) VALUES(?,?)',(i[0],i[1]))
except:
    print("insert failed")
conn.commit()
#For house price data
house_count_list = []
house = pandas.read_csv('median_housing_price.csv')
print(house)
house_count = house['Zipcode']
for i in hprice_zip:
    data = []
    data.append(i)
    try:
        data.append(int(house_count['area'][i]))
    except:
        data.append(0)
    house_count_list.append(data)
#print(crime_count_list)

conn = sqlite3.connect('Regression.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS CRIME')
cur.execute("CREATE TABLE CRIME (zipcode INTEGER, count INTEGER)")
try:
    for i in crime_count_list: 
        cur.execute('INSERT INTO CRIME (zipcode, count) VALUES(?,?)',(i[0],i[1]))
except:
    print("insert failed")
conn.commit()
#For Restaurants data
restaurants_count_list = []
restaurants = pandas.read_csv('Restaurants.csv')
restaurants_count = restaurants.groupby('Zipcode').count()
print(restaurants_count)
for i in hprice_zip:
    data = []
    data.append(i)
    try:
        data.append(int(restaurants_count['Id'][i]))
    except:
        data.append(0)
    restaurants_count_list.append(data)
print(restaurants_count_list)

conn = sqlite3.connect('Regression.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS RESTAURANTS')
cur.execute("CREATE TABLE RESTAURANTS (zipcode INTEGER, count INTEGER)")
try:
    for i in restaurants_count_list: 
        cur.execute('INSERT INTO RESTAURANTS (zipcode, count) VALUES(?,?)',(i[0],i[1]))
except:
    print("insert failed")
conn.commit()
#For Market data
Market_count_list = []
conn = sqlite3.connect('Raw_Data.db')
cur = conn.cursor()
try:
    cur.execute('SELECT zipcode, count(*) FROM Markets GROUP BY zipcode')
except:
    print("count failed")
result = cur.fetchall()
market_dict = {}
for i in result:
    market_dict[i[0]] = i[1]
print(market_dict)

for i in hprice_zip:
    data = []
    data.append(i)
    try:
        data.append(market_dict[i])
    except:
        data.append(0)
    Market_count_list.append(data)

conn = sqlite3.connect('Regression.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS MARKETS')
cur.execute("CREATE TABLE MARKETS (zipcode INTEGER, count INTEGER)")
try:
    for i in Market_count_list: 
        cur.execute('INSERT INTO MARKETS (zipcode, count) VALUES(?,?)',(i[0],i[1]))
except:
    print("insert failed")
conn.commit()
#For income data
income_count_list = []
conn = sqlite3.connect('Raw_Data.db')
cur = conn.cursor()
try:
    cur.execute('SELECT * FROM INCOME')
except:
    print("count failed")
result = cur.fetchall()

income_dict = {}
for i in result:
    income_dict[i[1]] = i[2]
print(income_dict)

for i in hprice_zip:
    data = []
    data.append(i)
    try:
        data.append(income_dict[str(i)])
    except:
        data.append(60197)
    income_count_list.append(data)
print(income_count_list)
conn = sqlite3.connect('Regression.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS INCOME')
cur.execute("CREATE TABLE INCOME (zipcode INTEGER, count INTEGER)")
try:
    for i in income_count_list: 
        cur.execute('INSERT INTO INCOME (zipcode, count) VALUES(?,?)',(i[0],i[1]))
except:
    print("insert failed")
conn.commit()
#Join all data together 
conn = sqlite3.connect('Regression.db')
cur = conn.cursor()
cur.execute("SELECT DISTINCT* FROM (((INCOME JOIN MARKETS ON INCOME.zipcode = MARKETS.Zipcode)JOIN RESTAURANTS ON INCOME.zipcode = RESTAURANTS.zipcode)JOIN CRIME ON INCOME.zipcode = CRIME.Zipcode)JOIN HOUSE ON INCOME.zipcode = HOUSE.Zipcode")
result = cur.fetchall()

with open('Aggregration.csv', "w") as f:
    csv_writer = csv.writer(f)
    head = ['Zipcode','Income','Market','Restaurants','Crime','House']
    csv_writer.writerow(head)
    for i in result:
        row = [i[0],i[1],i[3],i[5],i[7],i[9]]
        csv_writer.writerow(row)