from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Taken, Course, Student, Friend
from . import db

views = Blueprint('views', __name__)

@views.route('/myuser', methods=['GET'])
@login_required
def myuser():
    myid = current_user.id
    taken = (
        db.session.query(Course.title)
            .join(Taken, Taken.course == Course.id)
            .filter(Taken.student == myid)
            .all()
    )
    following = (
        db.session.query(Student)
            .join(Friend, Student.id == Friend.followee)
            .filter(Friend.follower == myid)
            .all()
    )
    followee = (
        db.session.query(Student)
            .join(Friend, Student.id == Friend.follower)
            .filter(Friend.followee == myid)
            .all()
    )

    friends = list(set(following) & set(followee))

    notFollowedBack = list(set(following) - set(followee))
    notFollowingBack = list(set(followee) - set(following))

    return render_template('myuser.html', username=current_user.username, taken=taken, friends=friends, requesting=notFollowedBack, requested=notFollowingBack)

@views.route('/friendschedule', methods=['GET'])
@login_required
def friendschedule():
    friendid = request.args.get('friendid')
    friendinfo = Student.query.get(friendid)
    taken = (
        db.session.query(Course.title)
            .join(Taken, Taken.course == Course.id)
            .filter(Taken.student == friendid)
            .all()
    )
    return render_template('friendschedule.html', username=friendinfo.username, taken=taken)

@views.route('/dropclass', methods=['GET','POST'])
def dropclass():
    if request.method == 'GET':
        myid = current_user.id
        taken = (
            db.session.query(Course)
                .join(Taken, Taken.course == Course.id)
                .filter(Taken.student == myid)
                .all()
        )
        return render_template('dropclass.html', courses = taken)

    if request.method == 'POST':
        # Get the list of selected class IDs from the form data
        selected_class_ids = request.form.getlist('selected_class')
        print(selected_class_ids)
        
        # Iterate through the selected class IDs and delete the corresponding entries from the 'Taken' table
        for class_id in selected_class_ids:
            taken_entry = Taken.query.filter(Taken.student==current_user.id, Taken.course==class_id).first()
            if taken_entry:
                db.session.delete(taken_entry)

        # Commit the changes to the database
        db.session.commit()
        
        return redirect(url_for('views.myuser'))

    return redirect(url_for('views.myuser'))

@views.route('/dropfriend', methods=['GET','POST'])
def dropfriend():
    if request.method == 'GET':
        myid = current_user.id
        friends = (
            db.session.query(Student)
            .join(Friend, Friend.followee == Student.id)
            .filter(Friend.follower == myid)
            .all()
        )
        print(friends)
        return render_template('dropfriend.html', friends = friends)
    
    if request.method == 'POST':
        selected_friends = request.form.getlist('selected_friend')
        myid = current_user.id

        for friend in selected_friends:
            friend_entry = Friend.query.filter(Friend.follower == myid, Friend.followee == friend).first()
            if friend_entry:
                db.session.delete(friend_entry)

        db.session.commit()

        return redirect(url_for('views.myuser'))

@views.route('/classresult', methods=['GET', 'POST'])
@login_required
def classresult():
    if request.method == 'GET':
        subject = request.args.get('subject')#.upper()
        courseno = request.args.get('courseno')
        title = request.args.get('title')#.title()
        day = request.args.get('day')#.upper()

        # Initialize the base query to select all courses
        query = Course.query

        # Filter the query based on the provided search parameters
        if subject:
            subject = subject.upper()
            query = query.filter(Course.subject == subject)
        if courseno:
            query = query.filter(Course.courseno == courseno)
        if title:
            title = title.title()
            query = query.filter(Course.title == title)
        if day:
            day = day.upper()
            query = query.filter(Course.day == day)

        # Execute the filtered query
        courses = query.all()

        #courses = Course.query.filter(Course.subject==subject).all()
        return render_template('classes.html', courses = courses)
    
    if request.method == 'POST':
        # Get the list of selected class IDs from the form data
        selected_class_ids = request.form.getlist('selected_class')
        print(selected_class_ids)
        
        # Iterate through the selected class IDs and create entries in the 'taken' table
        for class_id in selected_class_ids:
            print(class_id)
            taken_entry = Taken(student=current_user.id, course=class_id)
            db.session.add(taken_entry)
        
        # Commit the changes to the database
        db.session.commit()
        
        return redirect(url_for('views.myuser'))

@views.route('/friend', methods=['GET', 'POST'])
@login_required
def friend():
    if request.method == 'POST':
        # Get the list of selected class IDs from the form data
        selected_friends = request.form.getlist('selected_friend')
        print(selected_friends)
        
        # Iterate through the selected class IDs and create entries in the 'taken' table
        for follow in selected_friends:
            print(follow)
            follow_entry = Friend(follower=current_user.id, followee=follow)
            db.session.add(follow_entry)
        
        # Commit the changes to the database
        db.session.commit()
        
        return redirect(url_for('views.myuser'))
    
    if request.method == "GET":
        myid = current_user.id
        users = Student.query.all()
        current_friends = (
            db.session.query(Student)
                .join(Friend, Friend.followee == Student.id)
                .filter(Friend.follower == myid)
                .all()
        )

        users = list(set(users) - set(current_friends))

        return render_template('friend.html', users = users)