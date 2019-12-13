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

# In[2]:


la_path = '../data/Los_Angeles_City_Zip_Codes.shp'
la = gpd.read_file(la_path, encoding='utf-8')
la.plot()


# In[3]:


import csv


# ### Import Crime.csv File and Transfer into Shapefile

# In[4]:


crime = pd.read_csv('../data/Crime_2019.csv')
crime = crime.rename(columns={'lat':'y','lon':'x'})


# In[5]:


crime = crime[(crime[['y','x']] != 0).all(axis=1)]


# In[6]:


geometry = [Point(xy) for xy in zip(crime.x,crime.y)]
crs = {'init':'epsg:4326'}
geo_df = GeoDataFrame(crime,crs=crs,geometry=geometry)


# In[7]:


geo_df.to_file(driver = 'ESRI Shapefile',filename='crime.shp')


# In[8]:


crime_path = 'crime.shp'
crime_LAC = gpd.read_file(crime_path, encoding='utf-8')
crime_LAC.plot()


# ### Plot Crime and LAC Boundary in the Map

# In[9]:


ax = la.plot(figsize=(18,16),color='#EFEFEF',edgecolor='#444444')
crime_LAC.plot(ax=ax,color='red',markersize=6)
plt.title("Crimes in Los Angeles in 2019");
plt.axis('on');


# ### Create a Choropleth Map and Heat Map

# In[10]:


crime_zone_2019 = gpd.sjoin(la,crime_LAC,how='left',op='intersects')
crime_zone_2019.head()


# In[11]:


crime_zone_2019 = crime_zone_2019.rename(columns={'index_right':'crimes'})


# In[12]:


crime_zone_2019 = crime_zone_2019.groupby('ZIP', as_index=False).agg({
  'crimes': 'sum', 
  'geometry': 'first',
  })
crime_zone_2019 = gpd.GeoDataFrame(crime_zone_2019, crs='4326')


# In[13]:


crime_zone_2019.shape


# In[14]:


crime_zone_2019.sample(10)


# In[15]:


ax = crime_zone_2019.plot(figsize=(18,16),column='crimes',cmap='magma_r',k=5,legend=True)
plt.title('2019 Crimes by Zipcode - Los Angeles City');
ax.set_axis_off()


# ### Topographic Map

# In[16]:


def plot_point_distribution(**kwargs):
    #print(kwargs)
    ax = plt.gca()
    
    # context!
    context.plot(ax=ax, alpha=0.7, color='grey')
    
    color = kwargs.pop('color')
    geodf = kwargs.pop('data')
    bounds = kwargs.pop('bounds', None)

    sns.kdeplot(geodf.geometry.x, geodf.geometry.y, **kwargs)

    if bounds is not None:
        plt.xlim(bounds[:,0])
        plt.ylim(bounds[:,1])
    
    plt.axis('equal')
    plt.axis('off')


# In[17]:


def plot_heat_map(data, label, context):
    g = sns.FacetGrid(data=data, 
                      size=6, 
                      dropna=False
                     );

    g.map_dataframe(plot_point_distribution, 
                    shade=True, 
                    alpha=0.7, 
                    cbar=True, 
                    cmap='magma_r', 
                    cbar_kws={'orientation': 'horizontal',
                              'label': label,
                              'fraction': 0.02,
                              'shrink': 0.35,
                              'pad': 0}
                   );


# In[18]:


context = la.to_crs({'init': 'epsg:4326'})


# In[19]:


plot_heat_map(crime_LAC, 'Number of Crimes - Los Angeles City 2019', context)


# In[ ]:




