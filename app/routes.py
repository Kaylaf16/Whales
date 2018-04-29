from flask import render_template
from flask import request, abort,jsonify, redirect,url_for
import requests
from sqlalchemy.orm import load_only
from app import app,db
from flask_login import login_required
from flask_login import current_user, login_user
from app.models import Users,Skills

import json
import plotly
import pandas as pd
import numpy as np

app.debug = True
@app.route('/getallskills')
def getskills():
    rawskills = Skills.query.options(load_only('skill')).all()
    skills =[]
    for skill in rawskills:
        skills.append(skill.skill)
    return skills

@app.route('/')
def index():
     return render_template('landingpage.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method =='POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        geolocation = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCDz4WY_rzOR_UnUghAjY1h_f9ut1GC8TM').json()
        location = str(geolocation['location']['lat'])+","+str(geolocation['location']['lng'])
        if username is None or password is None:
            print("username or password is empty")
            abort(400)
            print(u)
        usernamecheck=Users.query.filter_by(username=username).first()
        if usernamecheck:
            abort(400)
            print("query error")

        user = Users(username=username, name =name,location=location)
        #hashedpassword=user.set_password(password).split(":")[2]
        #user.password = hashedpassword
        user.set_password(password);
        db.session.add(user)
        db.session.commit()
        return render_template('signin.html')
    elif request.method =='GET':
        return render_template('signup.html')

@app.route('/signin',methods=['GET','POST'])
def signin():
     if request.method =='POST':
         user = Users.query.filter_by(username=request.form.get('username')).first()
         password = request.form.get('password')
         if user is None or not user.check_password(password):
             print('Invalid username or password')
             return render_template('signin.html')
         #return render_template('home.html')
         return redirect(url_for('skillmap'))
     elif request.method=='GET':
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
