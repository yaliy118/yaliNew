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
            return redirect('DataModel')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Log in',
        year=datetime.now().year,
        repository_name='Pandas',
        )


#@app.route('/query' , methods = ['GET' , 'POST'])
#def query():

 #   print("Query")

  #  form1 = OlympicMedals()

   # df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/Olympic_athlets.csv'))


    #NOC_choices = get_NOC_choices(df)
    #form1.NOC.choices = NOC_choices
   
    

    #if request.method == 'POST':
     #   NOC = form1.NOC.data 
      #  KindofMedal = form1.KindofMedal.data
       # KindofGraph = form1.KindofGraph.data
        
        #df_new = covid19_day_ratio(df , NOC , KindofMedal)
        #fig = plt.figure()
        #fig.subplots_adjust(bottom=0.4)
        #ax = fig.add_subplot(111)
        #ax.set_ylim(0 , 3)
        #df_tmp.plot(ax = ax , kind = KindofGraph, figsize = (32, 14) , fontsize = 22 , grid = True)
        #chart = plot_to_img(fig)

    
    #return render_template(
     #   'Query.html',
      #  form1 = form1,
       # chart = chart
        
    #)

@app.route('/Query' , methods = ['GET' , 'POST'])
def Query():

    print("Query")

    form1 = OlympicMedals(request.form)

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/Olympic_athlets.csv'))


    NOC_choices = get_NOC_choices(df)
    form1.NOC.choices = NOC_choices
    chart = 'https://lh3.googleusercontent.com/proxy/dAmg5lEF-clbPeTvGwS6T6BjO9-ZqYACjubBTu01Fbwlt9tLCYOn_MO7nNbVpyK2n1OPxSzShTJdCCRUYwtfc7A8kvtrogQN'
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
        df1 = df1.loc[NOC]
        df1 = df1.groupby(['NOC' , 'Year']).sum()
        df1 = pd.DataFrame(df1)
        df1 = df1.reset_index()
        df1 = df1.set_index('Year')
        df1 = df1.sort_index()
        df1 = df1.loc[StartYear:EndYear]
        df2 = pd.DataFrame()
        for item in NOC:
            x = df1.loc[df1['NOC'] == item]
            y = x['Medal']
            df2[item] = y

        print(df2)
        print(StartYear)
        print(type(StartYear))
        print(EndYear)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        df2.plot(kind = KindofGraph, ax = ax)
        chart = plot_to_img(fig)
    
    return render_template(
        'Query.html',
        title='Query',
        chart = chart,
        form1 = form1
        
    )
