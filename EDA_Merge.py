#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Implemented on: July 29, 2024
# Creator: Reinald Peguero
# Title: Some Exploratory Data Analysis (EDA)
# Course: Intro to data Mining - Final Project

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

# read input file
def read_files():
    '''
        returns a Dataf=Frame
    '''
    df = pd.read_csv("merged_file_mlbgames_weather.csv")
    return df

# print correlations method
def corr_(games):
    '''
        games: inputs as parameter a DataFrame
    '''
    print("Correlation Coefficients of Temperature and Slugging Percentages")
    print("----------------------------------------------------------------")
    print("Pearson: {:.4f}".format(games["temp"].corr(games["SLG_PCT"],method='pearson')),end="\t\t")
    print("Spearman: {:.4f}".format(games["temp"].corr(games["SLG_PCT"],method='spearman')))
    print()
    print("Correlation Coefficients of Wind Direction and Slugging Percentages")
    print("-------------------------------------------------------------------")
    print("Pearson: {:.4f}".format(games["wdir"].corr(games["SLG_PCT"],method='pearson')),end="\t\t")
    print("Spearman: {:.4f}".format(games["wdir"].corr(games["SLG_PCT"],method='spearman')))
    print()
    print("Correlation Coefficients of Wind Speed and Slugging Percentages")
    print("---------------------------------------------------------------")
    print("Pearson: {:.4f}".format(games["wspd"].corr(games["SLG_PCT"],method='pearson')),end="\t")
    print("Spearman: {:.4f}".format(games["wspd"].corr(games["SLG_PCT"],method='spearman')))
    print()
    print("Correlation Coefficients of Precipitation and Slugging Percentages")
    print("------------------------------------------------------------------")
    print("Pearson: {:.4f}".format(games["pres"].corr(games["SLG_PCT"],method='pearson')),end="\t")
    print("Spearman: {:.4f}".format(games["pres"].corr(games["SLG_PCT"],method='spearman')))
    print()
    print("Correlation Coefficients of Dew Point and Slugging Percentages")
    print("--------------------------------------------------------------")
    print("Pearson: {:.4f}".format(games["dwpt"].corr(games["SLG_PCT"],method='pearson')),end="\t\t")
    print("Spearman: {:.4f}".format(games["dwpt"].corr(games["SLG_PCT"],method='spearman')))
    print()
    print("Correlation Coefficients of Stadium Elevation and Slugging Percentages")
    print("----------------------------------------------------------------------")
    print("Pearson: {:.4f}".format(games["Elevation"].corr(games["SLG_PCT"],method='pearson')),end="\t\t")
    print("Spearman: {:.4f}".format(games["Elevation"].corr(games["SLG_PCT"],method='spearman')))

# main program
def main():
    games = read_files()
    
    # calculation of slugging percentage
    games["SLG_PCT"] = (games["Singles"]+(games["Doubles"]*2)+\
                       (games["Triples"]*3)+(games["Home Runs"]*4))/\
                       games["At Bats"]

    # print dimension of dataset
    gs = games.shape
    print("The dimesions of the Baseball-Weather dataset is {0} rows and {1} columns.".format(\
        gs[0], gs[1]))
    print()
    
    # print datatypes of columns (features)
    games.info()
    print()
    
    # call correlation method
    corr_(games)
    print()
    print()

    # fill empty elements with mean values
    games = games.fillna(games.mean())
    
    # group items
    by_temp = games.groupby("temp").size()
    by_temp.plot.bar()

    by_SLG_PCT = games.groupby("SLG_PCT").size()
    by_SLG_PCT.plot.bar()

    # visualization
    #plt.scatter(by_temp, by_SLG_PCT)

    # separate train set and validation set
    X = games[["temp"]]
    y = games[["SLG_PCT"]]

    # visualization
    plt.scatter(X, y)
    
    # split the data
    X_train, X_test, y_train, y_test = train_test_split(\
        X, y, test_size=0.2, random_state=42)

    # Dummy regressor model
    dummy_reg = DummyRegressor()
    dummy_reg.fit(X_train, y_train)
    y_pred = dummy_reg.predict(X_test)
    test_error = mean_squared_error(y_test, y_pred, squared=False)
    print("DummyRegressor test error:", test_error)

    # training error
    y_pred = dummy_reg.predict(X_train)
    training_error = mean_squared_error(y_train, y_pred, squared=False)
    print("DummyRegressor training error:", training_error)
    
    # linearRegression model           
    regr = LinearRegression()
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print("One feature test error:", rmse)

    # drop non-numeric columns
    X = games.drop(columns=["Date", "Time", "Visitor", "Home", "Location", "Team",\
                        "Opponent"])

    # split data (training set, validation set)
    X_train, X_test, y_train, y_test = train_test_split(\
        X, y, test_size=0.2, random_state=42)

    # LinearRegression
    regr = LinearRegression()
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print("Multi Feature test error:", rmse)
main()


# In[ ]:




