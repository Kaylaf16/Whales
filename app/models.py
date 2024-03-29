from app import db, login
from flask_login import UserMixin
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash

class Users(UserMixin ,db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    location = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
class Skills(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True)
    skill =  db.Column(db.String(64), index=True)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
