from flask import render_template
from app import app

import json
import plotly
import pandas as pd
import numpy as np

app.debug = True

@app.route('/')
def index():
     return render_template('landingpage.html')

@app.route('/signup')
def signup():
     return render_template('signup.html')

@app.route('/signin')
def signin():
     return render_template('signin.html')

@app.route('/skillmap')
def skillmap():

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv')
    df.head()

    df['text'] = df['name'] + '<br>Population ' + (df['pop']/1e6).astype(str)+' million'
    limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
    colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","rgb(255,220,0)"]
    cities = []
    scale = 50000

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        city = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df_sub['lon'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            sizemode = 'diameter',
            marker = dict( 
                size = df_sub['pop']/scale, 
                color = colors[i],
                line = dict(width = 2,color = 'black')
            ),
            name = '{0} - {1}'.format(lim[0],lim[1]) )
        cities.append(city)

    layout = dict(
            title = '2014 US city populations<br/>(Click legend to toggle traces)',
            showlegend = True,
            geo = dict(
                scope='usa',
                projection   = dict( type='albers usa' ),
                showland     = True,
                landcolor    = 'rgb(217, 217, 217)',       
                subunitwidth = 1,
                countrywidth = 1,
                subunitcolor = "rgb(255, 255, 255)",
                countrycolor = "rgb(255, 255, 255)"           
            ),  
        )
        
    fig = dict( data=cities, layout=layout )

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layouts/index.html',
                           graphJSON=graphJSON)
