### ----------------------------------------------------------- ###
### --- include all software packages and libraries needed ---- ###
### ----------------------------------------------------------- ###
import base64
import io
import datetime
import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure               import Figure
from os                              import path


#-----------------------------------------------------------------------------------------------------------------------------------------------
# A Graph ------------------> A Picture
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
    return rd

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String
#-----------------------------------------------------------------------------------------------------------------------------------------------
# Function of country selection options according to user
def get_NOC_choices(df):
    df1 = df.groupby('NOC').sum()
    l = df1.index
    m = list(zip(l , l))
    return m
#-----------------------------------------------------------------------------------------------------------------------------------------------




