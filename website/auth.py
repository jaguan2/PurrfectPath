from flask import Blueprint, render_template, request, redirect, url_for
from .models import Student
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    uname = request.form.get('username')
    password = request.form.get('password')

    student = Student.query.filter_by(username=uname).first()
    s = Student.query.all()
    if student:
      # Directly compare the password without hashing
      if student.password == password:
        login_user(student, remember=True)
        return redirect(url_for('views.myuser'))

  return render_template("index.html")


@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')
    adminid = request.form.get('adminid')
    major = request.form.get('major')

    student = Student.query.filter_by(username=username).first()
    if student:
      print("error")
    elif password != confirmPassword:
      print("error")
    elif adminid == "123":
      # Store the password directly without hashing
      new_student = Student(username=username, email=email, password=password, major=major, isadmin=True)
      db.session.add(new_student)
      db.session.commit()
      login_user(new_student, remember=True)

      db.session.commit()

      return redirect(url_for('views.myuser'))       
    else:
      # Store the password directly without hashing
      new_student = Student(username=username, email=email, password=password, major=major, isadmin=False)
      db.session.add(new_student)
      db.session.commit()
      login_user(new_student, remember=True)

      db.session.commit()

      return redirect(url_for('views.myuser'))
  return render_template("register.html")

@auth.route('/ret')
def ret():
  return render_template("index.html")

@auth.route('/home')
def home():
  return redirect(url_for('views.myuser'))

@auth.route('/search', methods=['GET', 'POST'])
def search():
  if request.method == 'POST':
    subject = request.form.get('subject')
    courseno = request.form.get('courseno')
    title = request.form.get('title')
    day = request.form.get('day')

    return redirect(url_for('views.classresult', subject=subject, courseno=courseno, title=title, day=day))
  return render_template("schedule.html")

@auth.route('/friend')
def friend():
  return redirect(url_for('views.friend'))
