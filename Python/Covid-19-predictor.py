#!/usr/bin/env python
# coding: utf-8

import nltk
import os
import re
import random  
import string
import numpy as np
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import datasets
#from sklearn.cluster import KMeans, AgglomerativeClustering

def convert_dtype(x):
    if not x:
        return ''
    try:
        return str(x)   
    except:        
        return ''

#df = pd.read_csv('/Users/nat2147/Anant/code/python/input.csv', converters={'death_yn': convert_dtype}, low_memory=False)
df = pd.read_csv('/Users/nat2147/Anant/code/python/input.csv', low_memory=False)

df['case_month'] = pd.to_datetime(df['case_month'])
df.rename(columns={'case_month' : 'Date'}, inplace = True)

#Setting the 'Confirmed' cases as 1 and rest as 0 from 'current_status' column
df['Confirmed'] = [1 if i== "Laboratory-confirmed case" else 0 for i in df['current_status']]

#Setting 'Deaths' cases as 1 and rest as 0 from 'death_yn' column
df["Deaths"] = [1 if i== "Yes" else 0 for i in df['death_yn']]

#Setting 'Recovered' cases as 1 and rest as 0 from 'death_yn' column. 
#Ignoring other values in the column due to unavailable data
df["Recovered"] = [1 if i== "No" else 0 for i in df['death_yn']]

#Extract No. of Confirmed cases, Deaths, Recovered cases from the dataset
confirmed = df.groupby('Date')['Confirmed'].sum().to_frame()
deaths = df.groupby('Date')['Deaths'].sum().to_frame()
recovered = df.groupby('Date')['Recovered'].sum().to_frame()

# Converting the Date from Index to Column
confirmed.reset_index(inplace=True)
deaths.reset_index(inplace=True)
recovered.reset_index(inplace=True)

fig = go.Figure()
#Plotting datewise confirmed cases
fig.add_trace(go.Scatter(x=confirmed['Date'], y=confirmed['Confirmed'], mode='lines+markers', name='Confirmed',line=dict(color='blue', width=2)))
fig.add_trace(go.Scatter(x=deaths['Date'], y=deaths['Deaths'], mode='lines+markers', name='Deaths', line=dict(color='Red', width=2)))
fig.add_trace(go.Scatter(x=recovered['Date'], y=recovered['Recovered'], mode='lines+markers', name='Recovered', line=dict(color='Green', width=2)))
fig.update_layout(title='US COVID-19 Cases', xaxis_tickfont_size=14,yaxis=dict(title='Number of Cases'))
fig.show()

# creating our model using Sklearn
model = GaussianNB()
#dataset = datasets.load_iris()
#print(df.head)
#X = df.astype({'underlying_conditions_yn' : 'float64'}, errors = 'ignore').dtypes
#df['underlying_conditions_yn'] = pd.to_numeric(df['underlying_conditions_yn'])
#Setting the 'underlying_conditions_yn = yes' cases as 1 and rest as 0 from 'current_status' column
df['underlying_conditions_yn'] = [1 if i== "Yes" else 0 for i in df['current_status']]
X = df.underlying_conditions_yn
y = df.astype({'Confirmed' : 'int32'}).dtypes
model.fit(X, y)

# making predictions
expected = y
predicted = model.predict(X)

# accuracy & statistics
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

'''
# split the data into train and test set
train, test = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)
train.to_csv('/Users/nat2147/Anant/code/python/prediction/train.csv')
test.to_csv('/Users/nat2147/Anant/code/python/prediction/test.csv')

'''