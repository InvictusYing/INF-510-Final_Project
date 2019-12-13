# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 21:01:43 2019

@author: Yvaine_LI
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
#read data
data = pd.read_csv('Aggregration.csv')
#Visualize data
#print(data)

sns.pairplot(data, x_vars=['Income','Market','Restaurants','Crime'], y_vars='House', height=7, aspect=0.8,kind='reg')
plt.show()
#Identify x
X = data[['Income','Market','Restaurants','Crime']]
#Identify y
Y = data['House']
#Regression
linreg = LinearRegression()
model=linreg.fit(X, Y)
print (linreg.intercept_)
print (linreg.coef_)
