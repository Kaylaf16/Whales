from flask import render_template
from flask import request, abort,jsonify
import requests
from app import app,db
from flask_login import login_required
from flask_login import current_user, login_user
from app.models import Users

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
         return render_template('signup.html')
     elif request.method=='GET':
        return render_template('signin.html')
