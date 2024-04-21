from . import db
from flask_login import UserMixin

class Student(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())
    username = db.Column(db.String())
    major = db.Column(db.String()) 
