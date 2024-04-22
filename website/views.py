from flask import render_template, Blueprint
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

@views.route('/friend', methods=['GET', 'POST'])
@login_required
def friend():
    users = Student.query.all()
    return render_template('friend.html', users = users)
