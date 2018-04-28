from flask import render_template
from app import app

@app.route('/')
def index():
     return render_template('landingpage.html')

@app.route('/signup')
def signup():
     return render_template('signup.html')

@app.route('/signin')
def signin():
     return render_template('signin.html')
