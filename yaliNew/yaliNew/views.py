"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from yaliNew import app
from yaliNew.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from yaliNew.Models.QueryFormStructure import UserRegistrationFormStructure 
from yaliNew.Models.QueryFormStructure import LoginFormStructure 
from yaliNew.Models.QueryFormStructure import QueryFormStructure
from yaliNew.Models.QueryFormStructure import OlympicMedals
db_Functions = create_LocalDatabaseServiceRoutines() 

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from yaliNew.Models.plot_service_functions import plot_to_img
from yaliNew.Models.plot_service_functions import get_NOC_choices

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

@app.route('/')
def Home():
    """Renders the home page."""
    return render_template(
        'Home.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/Contact')
def Contact():
    """Renders the contact page."""
    return render_template(
        'Contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/About')
def About():
    """Renders the about page."""
    return render_template(
        'About.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/Register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)
    #ha
    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            return redirect('DataModel')
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'Register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )


@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='Data Model',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )


@app.route('/DataSet1')
def DataSet1():
    """Renders the DataSet1 page."""
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/Olympic_athlets.csv'))
    raw_data_table = df.to_html(classes='table table-hover', max_rows=8)

    return render_template(
        'DataSet1.html',
        title='Data Set',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='Data Set'
    )


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('Query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Log in',
        year=datetime.now().year,
        repository_name='Pandas',
        )




@app.route('/Query' , methods = ['GET' , 'POST'])
def Query():

    print("Query")

    form1 = OlympicMedals(request.form)

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/Olympic_athlets.csv'))


    NOC_choices = get_NOC_choices(df)
    form1.NOC.choices = NOC_choices
    chart_all = 'https://sportshub.cbsistatic.com/i/r/2019/07/24/256d9092-eadf-400f-9efe-290d3cba57b2/thumbnail/1200x675/275b3cf435c363443fa7f085e34619c1/screen-shot-2019-07-24-at-1-07-13-pm.png'
    chart_Gold = 'https://upload.wikimedia.org/wikipedia/commons/3/3e/IOCrings.jpg'
    chart_Silver = 'https://i.ebayimg.com/thumbs/images/g/AmgAAOSwAt1eHz9Q/s-l200.jpg'
    chart_Bronze = 'https://lh3.googleusercontent.com/proxy/EFI_QTpYTGnvb8Q_PxBjfhr50Y5bkqjpzn05Kt0pEYiMkdyTt4YOUrQMdh56iMcerPPYND-oqXnArSqJ-1jzwlU1lnZuQ_fqbV86IYeWwiOcuqEvM04AtUh9TSvvPQ'
    
    if request.method == 'POST':
        NOC = form1.NOC.data
        StartYear = form1.StartYear.data
        EndYear = form1.EndYear.data
        KindofGraph = form1.KindofGraph.data
        
        df1 = df.replace({'Medal':{'Gold': 1}})
        df1 = df1.replace({'Medal':{'Bronze': 1}})
        df1 = df1.replace({'Medal':{'Silver': 1}})
        df1 = df1.fillna(0)
        df1 = df1.drop(['ID' , 'Name' , 'Sex' , 'Age' , 'Height' , 'Weight' , 'Team' , 'Games' , 'Season' , 'City' , 'Sport' , 'Event'], 1)
        df1 = df1.set_index('NOC')
        df1 = df1.groupby(['NOC' , 'Year']).sum()
        df1 = pd.DataFrame(df1)
        df1 = df1.reset_index()
        df1 = df1.set_index('Year')
        df1 = df1.sort_index()
        dfall = pd.DataFrame()
        x = df1.loc[df1['NOC'] == 'GRE']
        y = x['Medal']
        dfall['GRE'] = y
        dfall = dfall.rename(columns={'GRE': 'a'})
        for item in NOC:
            x = df1.loc[df1['NOC'] == item]
            y = x['Medal']
            dfall[item] = y
        dfall = dfall.loc[StartYear:EndYear]
        dfall = dfall.drop('a',1)
        dfall = dfall.fillna(0)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        dfall.plot(kind = KindofGraph, ax = ax)
        chart_all = plot_to_img(fig)

        df1 = df.replace({'Medal':{'Gold': 1}})
        df1 = df1.replace({'Medal':{'Bronze': 0}})
        df1 = df1.replace({'Medal':{'Silver': 0}})
        df1 = df1.fillna(0)
        df1 = df1.drop(['ID' , 'Name' , 'Sex' , 'Age' , 'Height' , 'Weight' , 'Team' , 'Games' , 'Season' , 'City' , 'Sport' , 'Event'], 1)
        df1 = df1.set_index('NOC')
        df1 = df1.groupby(['NOC' , 'Year']).sum()
        df1 = pd.DataFrame(df1)
        df1 = df1.reset_index()
        df1 = df1.set_index('Year')
        df1 = df1.sort_index()
        dfGold = pd.DataFrame()
        x = df1.loc[df1['NOC'] == 'GRE']
        y = x['Medal']
        dfGold['GRE'] = y
        dfGold = dfGold.rename(columns={'GRE': 'a'})
        for item in NOC:
            x = df1.loc[df1['NOC'] == item]
            y = x['Medal']
            dfGold[item] = y
        dfGold = dfGold.loc[StartYear:EndYear]
        dfGold = dfGold.drop('a',1)
        dfGold = dfGold.fillna(0)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        dfGold.plot(kind = KindofGraph, ax = ax)
        chart_Gold = plot_to_img(fig)

        df1 = df.replace({'Medal':{'Gold': 0}})
        df1 = df1.replace({'Medal':{'Bronze': 0}})
        df1 = df1.replace({'Medal':{'Silver': 1}})
        df1 = df1.fillna(0)
        df1 = df1.drop(['ID' , 'Name' , 'Sex' , 'Age' , 'Height' , 'Weight' , 'Team' , 'Games' , 'Season' , 'City' , 'Sport' , 'Event'], 1)
        df1 = df1.set_index('NOC')
        df1 = df1.groupby(['NOC' , 'Year']).sum()
        df1 = pd.DataFrame(df1)
        df1 = df1.reset_index()
        df1 = df1.set_index('Year')
        df1 = df1.sort_index()
        dfSilver = pd.DataFrame()
        x = df1.loc[df1['NOC'] == 'GRE']
        y = x['Medal']
        dfSilver['GRE'] = y
        dfSilver = dfSilver.rename(columns={'GRE': 'a'})
        for item in NOC:
            x = df1.loc[df1['NOC'] == item]
            y = x['Medal']
            dfSilver[item] = y
        dfSilver = dfSilver.loc[StartYear:EndYear]
        dfSilver = dfSilver.drop('a',1)
        dfSilver = dfSilver.fillna(0)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        dfSilver.plot(kind = KindofGraph, ax = ax)
        chart_Silver = plot_to_img(fig)

        df1 = df.replace({'Medal':{'Gold': 0}})
        df1 = df1.replace({'Medal':{'Bronze': 1}})
        df1 = df1.replace({'Medal':{'Silver': 0}})
        df1 = df1.fillna(0)
        df1 = df1.drop(['ID' , 'Name' , 'Sex' , 'Age' , 'Height' , 'Weight' , 'Team' , 'Games' , 'Season' , 'City' , 'Sport' , 'Event'], 1)
        df1 = df1.set_index('NOC')
        df1 = df1.groupby(['NOC' , 'Year']).sum()
        df1 = pd.DataFrame(df1)
        df1 = df1.reset_index()
        df1 = df1.set_index('Year')
        df1 = df1.sort_index()
        dfBronze = pd.DataFrame()
        x = df1.loc[df1['NOC'] == 'GRE']
        y = x['Medal']
        dfBronze['GRE'] = y
        dfBronze = dfBronze.rename(columns={'GRE': 'a'})
        for item in NOC:
            x = df1.loc[df1['NOC'] == item]
            y = x['Medal']
            dfBronze[item] = y
        dfBronze = dfBronze.loc[StartYear:EndYear]
        dfBronze = dfBronze.drop('a',1)
        dfBronze = dfBronze.fillna(0)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        dfBronze.plot(kind = KindofGraph, ax = ax)
        chart_Bronze = plot_to_img(fig)
                
    return render_template(
        'Query.html',
        title='Data Query',
        chart_all = chart_all,
        chart_Gold = chart_Gold,
        chart_Silver = chart_Silver,
        chart_Bronze = chart_Bronze,
        form1 = form1
        
    )
