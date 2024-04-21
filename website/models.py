from . import db
from flask_login import UserMixin

class Student(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())
    username = db.Column(db.String())
    major = db.Column(db.String()) 

# class Student(db.Model, UserMixin):

#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100))
#     password = db.Column(db.String(100))
#     username = db.Column(db.String(100))
#     major = db.Column(db.String(100))
#     advisor = db.Column(db.Integer, db.ForeignKey(Faculty.id))

class Faculty(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    department = db.Column(db.String(100))

class Courses(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(3))
    courseno = db.Column(db.String(100))
    title = db.Column(db.String(100))
    credits = db.Column(db.Integer) 
    instrumeth = db.Column(db.String(100))
    day = db.Column(db.String(10)) 
    time = db.Column(db.String(100))
    location = db.Column(db.String(100)) 
    instructor = db.Column(db.Integer, db.ForeignKey('Faculty.id'))

class Taken(db.Model, UserMixin):
    student = db.Column(db.Integer, db.ForeignKey('Student.id'), primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('Courses.id'), primary_key=True)