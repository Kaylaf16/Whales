from flask import Flask
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

login = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tofee_admin:kayla'+"'"+'shead@tofee.c26m04nvstq9.us-east-1.rds.amazonaws.com/tofee'
db = SQLAlchemy(app)
login.login_view = 'login'
migrate =Migrate(app,db)

from app import routes,models
app.debug = True
