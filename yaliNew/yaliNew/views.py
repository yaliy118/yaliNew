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

db_Functions = create_LocalDatabaseServiceRoutines() 


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
            # Here you should put what to do (or were to go) if registration was good
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