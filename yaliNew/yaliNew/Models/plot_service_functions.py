import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from os import path
import io


def plot_case_1(df , kind):
    print("Running from plot_case_1()")
    rd = {}
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    series_approving.plot(ax=ax,  kind = kind, title = 'Trump Approval Index', figsize = (15, 6), fontsize = 14, style = 'bo-')
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    rd['isempty'] = ''
        rd['img'] = pngImageB64String
        # return pngImageB64String
    return rd




def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


def OlympicDataFrame(df , NOC , KindofMedal):
    df = df.drop(['Name' , 'Sex' , 'Age' , 'Height' , 'Weight' , 'Team' , 'Games' , 'Year' , 'Season' , 'City' , 'Sport' , 'Event'], 1)
    if KindofMedal == 'Gold':
        df1 = df.replace({'Medal':{'Gold': 1}})
        df1 = df1.replace({'Medal':{'Bronze': 0}})
        df1 = df1.replace({'Medal':{'Silver': 0}})
        df1 = df.replace({'NOC':{NOC: NOC + '_Gold'}})
        df1 = df1.fillna(0)
        df1 = df1.groupby('NOC').sum()
        df1 = df1.loc[ NOC ]
        df1 = df1.transpose()
    else:
        df1 = {}

    
    if KindofMedal == 'Silver':
        df2 = df.replace({'Medal':{'Gold': 0}})
        df2 = df2.replace({'Medal':{'Bronze': 0}})
        df2 = df2.replace({'Medal':{'Silver': 1}})
        df2 = df2.fillna(0)
        df2 = df.replace({'NOC':{NOC: NOC + '_Silver'}})
        df2 = df2.groupby('NOC').sum()
        df2 = df2.loc[ NOC ]
        df2 = df2.transpose()
    else:
        df2 = {}

    if KindofMedal == 'Bronze':
        df3 = df.replace({'Medal':{'Gold': 0}})
        df3 = df3.replace({'Medal':{'Bronze': 1}})
        df3 = df3.replace({'Medal':{'Silver': 0}})
        df3 = df3.fillna(0)
        df3 = df.replace({'NOC':{NOC: NOC + '_Bronze'}})
        df3 = df3.groupby('NOC').sum()
        df3 = df3.loc[ NOC ]
        df3 = df3.transpose()
    else:
        df3{}
    
    df4 = df1+df2+df3
    df4.sort()
    df_new = list(df4)


    return df_new



def get_NOC_choices(df):
    df1 = df1.groupby('NOC').sum()
    l = df1.index
    m = list(zip(l , l))
    return m




def OlympicDataFramebyYearsandNOC(df , NOC , StartYear , EndYear):
    df1 = df.replace({'Medal':{'Gold': 1}})
    df1 = df1.replace({'Medal':{'Bronze': 1}})
    df1 = df1.replace({'Medal':{'Silver': 1}})
    df1 = df1.fillna(0)
    df1 = df1.drop(['ID' , 'Name' , 'Sex' , 'Age' , 'Height' , 'Weight' , 'Team' , 'Games' , 'Season' , 'City' , 'Sport' , 'Event'], 1)
    df1 = df1.groupby(['NOC' , 'Year']).sum()
    df1 = df1.loc[ NOC ]  
    df1 = df1.loc[ StartYear : EndYear ]    

    return df1
