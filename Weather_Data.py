# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 09:49:23 2024

@author: Peter
"""

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
# This is the pandas library with the weather information, daily and hourly but i used hourly for the data i pulled
from meteostat import Point, Daily, Hourly

# creating a new dataframe of the csv im reading with pandas, you can save it and run it on your computer with the correct file path
venue_data = pd.read_csv('C:\\Users\\Peter\\Desktop\\venues.csv')



# new empty data frame to put the data
weather_data = pd.DataFrame()

#using the meteostat library and making a start and end time to pull the data from
start = datetime(2013, 1, 1)
end = datetime(2023, 12, 31)

# a for loop to go through each row of the venue csv and pull the location and the venue and location to know what the stadium actually is
for index, row in venue_data.iterrows():
    latitude = row['latitude']
    longitude = row['longitude']
    venue = row['venue']
    location = row['location']
    
    point = Point(latitude, longitude)
    
    # so here i am fetching the hourly data by passing the location and start and end times.
    data = Hourly(point, start, end)
    data = data.fetch()
    
    # just making sure its not empty
    if data is not None and not data.empty:
        data['latitude'] = latitude
        data['longitude'] = longitude
        data['venue'] = venue
        data['location'] = location  
        
        # i am concatenating each row (venue) into the new data frame i created. (weather_data)
        weather_data = pd.concat([weather_data, data])


# # Plot line chart including average, minimum and maximum temperature
# data.plot(y=['tavg', 'tmin', 'tmax'])
# plt.show()

#i elminated the columns from the library that are unnecessary
weather_data = weather_data.drop(columns=['snow', 'wpgt', 'tsun', 'coco', 'prcp'])

# saving the data and creating a new csv.
weather_data.to_csv('weather_data_2013-2023.csv', index=True)