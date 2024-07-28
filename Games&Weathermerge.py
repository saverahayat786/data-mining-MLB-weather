# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 20:26:36 2024

@author: Peter
"""

import pandas as pd

# Load the CSV files into DataFrames
weather_df = pd.read_csv('C:\\Users\\Peter\\Desktop\\Weather_Data_File.csv')
schedule_df = pd.read_csv('C:\\Users\\Peter\\Desktop\\Game_Times_plus_Venues.csv')



weather_df.columns = weather_df.columns.str.strip()
schedule_df.columns = schedule_df.columns.str.strip()


weather_df['date'] = weather_df['date'].str.strip()
schedule_df['date'] = schedule_df['date'].str.strip()


weather_df.rename(columns={'time_only': 'Time'}, inplace=True)
schedule_df.rename(columns={'Date': 'date', 'Day/Night': 'Time'}, inplace=True)

weather_df['temp'] = (weather_df['temp'] * 9/5) + 32


weather_df['date'] = pd.to_datetime(weather_df['date'], format='%m/%d/%Y', errors='coerce')
schedule_df['date'] = pd.to_datetime(schedule_df['date'], format='%m/%d/%Y', errors='coerce')

schedule_df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)


merged_df = pd.merge(weather_df, schedule_df, 
                     left_on=['date', 'Time', 'latitude', 'longitude'], 
                     right_on=['date', 'Time', 'latitude', 'longitude'], 
                     how='inner')


result_df = merged_df[['date', 'Time', 'temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'pres', 'Visitor', 'Home', 'Stadium', 'Elevation']]


result_df.to_csv('Weather_Data_Games(2013-2023).csv', index=False)

