from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from .models import Taken, Course, Student
from . import db

views = Blueprint('views', __name__)

@views.route('/myuser', methods=['GET'])
@login_required
def myuser():
    myid = current_user.id
    courses = Taken.query.filter(Taken.student == myid).all()
    allcourses = Course.query.all()
    taken = (
        db.session.query(Course.title)
            .join(Taken, Taken.course == Course.id)
            .filter(Taken.student == myid)
            .all()
    )

    return render_template('myuser.html', username=current_user.username, taken=taken)

@views.route('/classresults', methods=['GET', 'POST'])
@login_required
def classresults():
    subject = request.args.get('subject').upper()
    courseno = request.args.get('courseno')
    title = request.args.get('title').title()
    day = request.args.get('day').upper()

    # Initialize the base query to select all courses
    query = Course.query

    # Filter the query based on the provided search parameters
    if subject:
        query = query.filter(Course.subject == subject)
    if courseno:
        query = query.filter(Course.courseno == courseno)
    if title:
        query = query.filter(Course.title == title)
    if day:
        query = query.filter(Course.day == day)

    # Execute the filtered query
    courses = query.all()

    #courses = Course.query.filter(Course.subject==subject).all()
    return render_template('classes.html', courses = courses)


@views.route('/friend', methods=['GET', 'POST'])
@login_required
def friend():
    users = Student.query.all()
    return render_template('friend.html', users = users)
