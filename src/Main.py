# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 04:41:13 2019

@author: Yvaine_LI
"""
#gain all the dataset and store them
with open('Income.py','r') as f:
    exec(f.read())
with open('Market1.py','r') as f:
    exec(f.read())
with open('Market2.py','r') as f:
    exec(f.read())
with open('Restaurants.py','r') as f:
    exec(f.read())
with open('Crime.py','r') as f:
    exec(f.read())

#count data based on zipcode and add them into database
with open('Count.py','r') as f:
    exec(f.read())
    
#Do the regression analysis
with open('Regression.py','r') as f:
    exec(f.read())