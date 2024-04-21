from flask import Blueprint, render_template, request, flash, redirect, url_for
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
    sdata = []
    for a in s:
      print(f"Username: {a.username}")
    if student:
      # Directly compare the password without hashing
      print(student.password, password)
      if student.password == password:
        flash('Logged in successfully!', category='success')
        login_user(student, remember=True)
        return redirect(url_for('views.myuser'))
      else:
        flash('Incorrect password, try again.', category='error')
    else:
      flash('Account name does not exist.', category='error')

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
    major = request.form.get('major')


    student = Student.query.filter_by(username=username).first()
    if student:
      flash('Account name already exists.', category='error')
    elif password != confirmPassword:
      flash("Passwords don't match.", category='error')
    else:
      # Store the password directly without hashing
      new_student = Student(username=username, email=email, password=password, major=major)
      db.session.add(new_student)
      db.session.commit()
      login_user(new_student, remember=True)
      flash('Account created!', category='success')

      db.session.commit()

      return redirect(url_for('views.myuser'))

  return render_template("register.html")

@auth.route('/ret')
def ret():
  return render_template("index.html")

@auth.route('/home')
def home():
  return redirect(url_for('views.myuser'))

@auth.route('/search')
def search():
  return render_template("schedule.html")
