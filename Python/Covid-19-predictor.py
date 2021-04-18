#!/usr/bin/env python
# coding: utf-8

import random  
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import metrics

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

#Setting the 'underlying_conditions_yn = yes' cases as 1 and rest as 0 from 'current_status' column
df['underlying_conditions_yn'] = [1 if i== "Yes" else 0 for i in df['underlying_conditions_yn']]

#Setting the 'sex' to 1 for Female, 2 for Male and rest as 0 from 'sex' column
#df['sex'] = [1 if i== "Female" else 2 for i== "Male" else 0 for i in df['sex']]

#Setting the 'hosp_yn' to 1 for yes and rest as 0 from 'hosp_yn' column
df['hosp_yn'] = [1 if i== "Yes" else 0 for i in df['hosp_yn']]

#Setting the 'icu_yn' to 1 for yes and rest as 0 from 'icu_yn' column
df['icu_yn'] = [1 if i== "Yes" else 0 for i in df['icu_yn']]

#Setting the 'death_yn' to 1 for yes and rest as 0 from 'death_yn' column
df['death_yn'] = [1 if i== "Yes" else 0 for i in df['death_yn']]

#Splitting dataset into train and test parts
#X = df[["underlying_conditions_yn","age_group","hosp_yn","icu_yn","death_yn"]]
X = df[["underlying_conditions_yn","hosp_yn","icu_yn","death_yn"]]
y = df[["current_status"]]
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=0)

model.fit(Xtrain, ytrain)

# making predictions & calculating accuracy & statistics
ypred=model.predict(Xtest)
accuracy = metrics.accuracy_score(ytest,ypred)
report = metrics.classification_report(ytest, ypred)
cm = metrics.confusion_matrix(ytest, ypred)

print("Classification report:")
print("Accuracy: ",accuracy)
print(report)
print("Confusion matrix:")
print(cm)
