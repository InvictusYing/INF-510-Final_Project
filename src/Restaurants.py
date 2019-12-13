# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 15:07:40 2019

@author: Yvaine_LI
"""

from urllib.parse import quote
import requests

restaurants = []
all_resta = []
zipcode = []
LOSS = 0

def request(host, path, api_key, url_params=None):
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    try:
        response = requests.request('GET', url, headers=headers, params=url_params)
        response.raise_for_status
    except requests.exception.HTTPError as e:
        print(e)
    return response.json()

#input KEY
API_KEY = '3cvOztOVmj5lk4v3vqoUVl4SBJ55EFq0gH30iW6K7b9lkRhiRZTJccCPzHYCPs6pZUpgAZ1GFgkniIUj7DIf28f6M9E3Ep-3MoZQQqrTEGp5cwLMVh8SDdaOfHzbXXYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'

#input zipcode
try:
    with open('../data/Los_Angeles_City_Zip_Codes.csv','r') as f:
        for line in f:
            zipcode.append(line.split(',')[2])
    zipcode1 = zipcode[1:]
except:
    print('file does not find')

#searching
for i in zipcode1:
    print('We are searching the restaurants data in',i)
    for offset in range(0, 999, 20):
        url_params = {
            'term': 'restaurants',
            'location': i,
            'limit': 20,
            'offset': offset
            }

        data = request(API_HOST, SEARCH_PATH, API_KEY, url_params)
        
        try:
            for restaurant in data['businesses']:
                all_resta.append(restaurant)
        except:
            LOSS = LOSS + 20
            print("We have lost", LOSS, "data at",offset)
            break


for i in all_resta:
    data = []
    data.append(i['id'])
    data.append(i['rating'])
    data.append(i['coordinates']['latitude'])
    data.append(i['coordinates']['longitude'])
    data.append(i['location']['zip_code'])
    restaurants.append(data)