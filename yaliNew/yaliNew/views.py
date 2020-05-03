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

# Landing page - Home page
@app.route('/')
def Home():
    return render_template(
        'Home.html',
        title='Home Page',
        year=datetime.now().year,
    )

# Contact page - website creator details
@app.route('/Contact')
def Contact():
    return render_template(
        'Contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

# About Page - explanation about the site
@app.route('/About')
def About():
    return render_template(
        'About.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


# -------------------------------------------------------
# Register new user page
# This function will get user details, will check if the user already exists
# and if not, it will save the details in the users data base
# -------------------------------------------------------
@app.route('/Register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)

    return render_template(
        'Register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# Data model description, used by the site and leads to DataSet page
@app.route('/DataModel')
def DataModel():
    return render_template(
        'DataModel.html',
        title='Data Model',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )

# Data Set page, will show the data table
@app.route('/DataSet1')
def DataSet1():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/Olympic_athlets.csv'))
    raw_data_table = df.to_html(classes='table table-hover', max_rows=8)

    return render_template(
        'DataSet1.html',
        title='Data Set',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='Data Set'
    )


# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# This function will get user details (username, password), will check if the user exists in the user data base,
# if yes - the user will go to data query page, if not - the site will show an error massege.
# -------------------------------------------------------
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
        'Login.html', 
        form=form, 
        title='Log in',
        year=datetime.now().year,
        repository_name='Pandas',
        )



# Data Query page, will show four graphs of data analysis according to user requests
@app.route('/Query' , methods = ['GET' , 'POST'])
def Query():

    form1 = OlympicMedals(request.form)

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/Olympic_athlets.csv'))


    NOC_choices = get_NOC_choices(df)
    form1.NOC.choices = NOC_choices
    chart_all = 'https://sportshub.cbsistatic.com/i/r/2019/07/24/256d9092-eadf-400f-9efe-290d3cba57b2/thumbnail/1200x675/275b3cf435c363443fa7f085e34619c1/screen-shot-2019-07-24-at-1-07-13-pm.png'
    chart_Gold = 'https://i.pinimg.com/originals/42/2a/26/422a2600350a3a1256445a6fe4e57507.jpg'
    chart_Silver = 'https://c1.staticflickr.com/9/8296/8016919631_15b98c52dc_b.jpg'
    chart_Bronze = 'https://ewscripps.brightspotcdn.com/dims4/default/a1c860a/2147483647/strip/true/crop/640x360+0+60/resize/1280x720!/quality/90/?url=https%3A%2F%2Fmediaassets.ktnv.com%2Fphoto%2F2016%2F08%2F08%2FBronze_1470670140342_43914198_ver1.0_640_480.png'
    
    if request.method == 'POST':
        NOC = form1.NOC.data
        StartYear = form1.StartYear.data
        EndYear = form1.EndYear.data
        KindofGraph = form1.KindofGraph.data
        #-------------------------------------------
        # Making the winning type a number
        df1 = df.replace({'Medal':{'Gold': 1}})
        df1 = df1.replace({'Medal':{'Bronze': 1}})
        df1 = df1.replace({'Medal':{'Silver': 1}})
        df1 = df1.fillna(0)
        #-------------------------------------------
        # Delete unwanted columns for research
        df1 = df1.drop(['ID' , 'Name' , 'Sex' , 'Age' , 'Height' , 'Weight' , 'Team' , 'Games' , 'Season' , 'City' , 'Sport' , 'Event'], 1)
        #------------------------------------------
        # Make NOC indexed
        df1 = df1.set_index('NOC')
        #------------------------------------------
        # Pluse the amount of medals by state and year
        df1 = df1.groupby(['NOC' , 'Year']).sum()
        #------------------------------------------
        # Turn the table created into a database so that I can make changes to it in Visual Studio
        df1 = pd.DataFrame(df1)
        #------------------------------------------
        # Returns the index
        df1 = df1.reset_index()
        #------------------------------------------
        # Make Year indexed
        df1 = df1.set_index('Year')
        #------------------------------------------
        # Arrange the years in ascending order
        df1 = df1.sort_index()
        #------------------------------------------
        # Create a new database
        dfall = pd.DataFrame()
        #------------------------------------------
        # Enter into a database database a country that participated in all the Olympics that followed so that when you put in the database the desired countries and years there will be no shortage of years
        x = df1.loc[df1['NOC'] == 'GRE']
        y = x['Medal']
        dfall['GRE'] = y
        dfall = dfall.rename(columns={'GRE': 'a'})
        #------------------------------------------
        #Enter the desired countries database
        for item in NOC:
            x = df1.loc[df1['NOC'] == item]
            y = x['Medal']
            dfall[item] = y
        #------------------------------------------
        # Cut from the database the desired years
        dfall = dfall.loc[StartYear:EndYear]
        #------------------------------------------
        # Flip the auxiliary state which can help choose all the years
        dfall = dfall.drop('a',1)
        #------------------------------------------
        # Change all NaN to 0 in database
        dfall = dfall.fillna(0)
        #------------------------------------------
        #Insert a picture of the graph
        fig = plt.figure()
        ax = fig.add_subplot(111)
        dfall.plot(kind = KindofGraph, ax = ax)
        chart_all = plot_to_img(fig)
        #------------------------------------------


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
