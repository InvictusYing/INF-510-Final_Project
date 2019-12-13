#!/usr/bin/env python
# coding: utf-8

# # Reference
# https://towardsdatascience.com/how-safe-are-the-streets-of-santiago-e01ba483ce4b?
# https://github.com/Mjrovai/Python4DS/blob/master/Streets_Santiago/notebooks/10_Streets_of_Santiago.ipynb
# https://github.com/carnby/carto-en-python/blob/master/01%20-%20GeoPandas.ipynb

# ### Import Library

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from geopandas import GeoDataFrame
import fiona
from shapely.geometry import Point, Polygon


# ### Import Los Angeles Zipcodes Shapefile

# In[11]:


la_path = 'Los_Angeles_City_Zip_Codes.shp'
la = gpd.read_file(la_path, encoding='utf-8')
la.plot()


# In[3]:


import csv


# ### Import Median Housing Price.csv File and Transfer into Shapefile

# In[4]:


housing_price = pd.read_csv('median_housing_price.csv')
housing_price = housing_price['Avg Median Housing Price']
la['housing_price']=housing_price


# In[6]:


ax = la.plot(figsize=(18,16),column='housing_price',cmap='magma_r',k=5,legend=True)
plt.title('2019 Average Median Housing Price by Zipcode - Los Angeles City');
ax.set_axis_off()


# ### Import Median Income Data and Visulize it in the map

# In[7]:


median_income = pd.read_csv('income_zipcode.csv')
median_income = median_income['Median_Income']
la['median_income']=median_income


# In[8]:


ax = la.plot(figsize=(18,16),column='median_income',cmap='magma_r',k=5,legend=True)
plt.title('2019 Median Income by Zipcode - Los Angeles City');
ax.set_axis_off()


# ### Import Restaurants Data and Visulize it in the map

# In[9]:


restaurant = pd.read_csv('restaurant_count.csv')
restaurant = restaurant['Id']
la['restaurant']=restaurant


# In[10]:


ax = la.plot(figsize=(18,16),column='restaurant',cmap='magma_r',k=5,legend=True)
plt.title('2019 Median Income by Zipcode - Los Angeles City');
ax.set_axis_off()


# In[ ]:




