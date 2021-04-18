#!/usr/bin/env python
# coding: utf-8

import nltk
import os
import re
import random  
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn import datasets
from sklearn.cluster import KMeans, AgglomerativeClustering

def convert_dtype(x):
    if not x:
        return ''
    try:
        return str(x)   
    except:        
        return ''

df = pd.read_csv('/Users/nat2147/Anant/code/python/input.csv', converters={'death_yn': convert_dtype}, low_memory=False)

df.head()
df.dtypes

#df_sample = df.sample(frac = 0.01).reset_index()

df['case_month'] = pd.to_datetime(df['case_month'])
df.rename(columns={'case_month' : 'Date'}, inplace = True)

df.head()

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