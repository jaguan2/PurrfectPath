from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Taken, Course, Student, Friend, Faculty
from . import db
from sqlalchemy import func

views = Blueprint('views', __name__)

#route for the user page
@views.route('/myuser', methods=['GET'])
#required to be logged in to be on this page
@login_required
def myuser():
    #set my if as current user
    myid = current_user.id
    myuser = current_user.username

    #query for the classes registered by the current user based on the Course table and the Taken table
    #SQL = "SELECT title FROM Course JOIN Taken ON Course.id = Taken.course WHERE student = {my id}"
    taken = (
        db.session.query(Course.title)
            .join(Taken, Taken.course == Course.id)
            .filter(Taken.student == myid)
            .all()
    )
    #query for the users the current user is following
    #SQL = "SELECT * FROM Student JOIN Friend ON Student.id = Friend.followeee WHERE follower = {myid}"
    following = (
        db.session.query(Student)
            .join(Friend, Student.id == Friend.followee)
            .filter(Friend.follower == myid)
            .all()
    )
    #query for the users the current user is followed by
    #SQL = "SELECT * FROM Student JOIN Friend On Student.id = Friend.follower WHERE Friend.followee = {myid}"
    followee = (
        db.session.query(Student)
            .join(Friend, Student.id == Friend.follower)
            .filter(Friend.followee == myid)
            .all()
    )

    # list friends as those the current user is both following and is followed by
    friends = list(set(following) & set(followee))

    # list for the differences in following and followed by
    notFollowedBack = list(set(following) - set(followee))
    notFollowingBack = list(set(followee) - set(following))

    # open template based on current user and previous lists
    return render_template('myuser.html', username=myuser, taken=taken, friends=friends, requesting=notFollowedBack, requested=notFollowingBack)

# route to get friends schedules
@views.route('/friendschedule', methods=['GET'])
# login required as whos schedules you can look at depends on the user youre logged in as
@login_required
def friendschedule():
    #grab friendid from the arguments
    friendid = request.args.get('friendid')

    #query for the friend based on the friendid
    #SQL = "SELECT * FROM STUDENT WHERE id = {friendid}"
    friendinfo = Student.query.get(friendid)

    #query to find the classes taken by the friend
    #SQL = "SELECT title FROM Course JOIN Taken ON Taken.course = Course.id WHERE student = {friendid}"
    taken = (
        db.session.query(Course.title)
            .join(Taken, Taken.course == Course.id)
            .filter(Taken.student == friendid)
            .all()
    )

    # open template based on friends information and previous lists
    return render_template('friendschedule.html', username=friendinfo.username, taken=taken)

# route to drop classes
@views.route('/dropclass', methods=['GET','POST'])
@login_required
def dropclass():
    # when the page is called
    if request.method == 'GET':
        #save current user's id as myid
        myid = current_user.id
        
        #query for the classes registered by the current user based on the Course table and the Taken table
        #SQL = "SELECT * FROM Course JOIN Taken ON Course.id = Taken.course WHERE student = {my id}"
        taken = (
            db.session.query(Course)
                .join(Taken, Taken.course == Course.id)
                .filter(Taken.student == myid)
                .all()
        )

        # open template based on the previous list
        return render_template('dropclass.html', courses = taken)

    # when the page sends a POST
    if request.method == 'POST':
        # get checked classes from form selected_class
        selected_crn = request.form.getlist('selected_class')
        
        # for every class checked, delete the instance of the current user and this class from the Taken table
        for crn in selected_crn:
            # set taken_entry as the instance of the current user and the current class iteration
            taken_entry = Taken.query.filter(Taken.student==current_user.id, Taken.course==crn).first()
            # if the instance exists, delete it from the database
            if taken_entry:
                #SQL: DELETE FROM Taken WHERE student = {myid} AND course = {crn};
                db.session.delete(taken_entry)

        # commit the changes to the database
        db.session.commit()
        
        # return to user page to see updated class list
        return redirect(url_for('views.myuser'))

#route to drop friends and sent requests
@views.route('/dropfriend', methods=['GET','POST'])
@login_required
def dropfriend():
    # when a page is called
    if request.method == 'GET':
        #save current user's id as my id
        myid = current_user.id

        #query for the users the current user is following
        #SQL = "SELECT * FROM Student JOIN Friend ON Student.id = Friend.followeee WHERE follower = {myid}"
        friends = (
            db.session.query(Student)
            .join(Friend, Friend.followee == Student.id)
            .filter(Friend.follower == myid)
            .all()
        )
        
        # open template based on the previous list
        return render_template('dropfriend.html', friends = friends)
    
    # when the page sends a POST
    if request.method == 'POST':
        # get checked friends from form selected_friend
        selected_friends = request.form.getlist('selected_friend')

        #save current user's id as myid
        myid = current_user.id

        # for every friend checked, delete the instance in the Friend table where the user is the follower and the friend is the followee
        for friend in selected_friends:
            # set friend_entry as the instance of the current user following the friend
            friend_entry = Friend.query.filter(Friend.follower == myid, Friend.followee == friend).first()
            # if the instance exists, delete it from the database
            if friend_entry:
                #SQL: DELETE FROM Friend WHERE follower = {myid} AND followee = {friendid};
                db.session.delete(friend_entry)

        # commit changes to the database
        db.session.commit()

        #return to user page to see updated friends list
        return redirect(url_for('views.myuser'))

# route to see classes based on what was submitted in schedule
@views.route('/classresult', methods=['GET', 'POST'])
def classresult():
    # when page is requested
    if request.method == 'GET':
        # grab variables from argument line when route was called
        subject = request.args.get('subject')#.upper()
        courseno = request.args.get('courseno')
        title = request.args.get('title')#.title()
        day = request.args.get('day')#.upper()

        # initialize query to select all courses
        # purposes: (1) when the form is returned empty, (2) as the base to narrow down based on what was entered in the form
        # SQL: "SELECT * FROM Course;"
        query = (db.session.query(
                    Course.id,
                    Course.subject,
                    Course.courseno,
                    Course.title,
                    Course.credits,
                    Course.instrumeth,
                    Course.day,
                    Course.time,
                    Course.location,
                    Course.instructor,
                    Faculty.fname,
                    Faculty.lname)
                .join(Faculty, Faculty.id == Course.instructor)
                )

        # filter down the query based on what attributes were given
        if subject:
            # SQL: "SELECT * FROM Course WHERE subject = UPPER({subject});"
            subject = subject.upper()
            query = query.filter(Course.subject == subject)
        if courseno:
            #SQL: "SELECT * FROM Course WHERE courseno = {courseno}"
            query = query.filter(Course.courseno == courseno)
        if title:
            #SQL: "SELECT * FROM Course WHERE title = {title}"
            title = title.lower()
            query = query.filter(func.lower(Course.title) == title)

        if day:
            #SQL: "SELECT * FROM Course WHERE day = UPPER({day})"
            day = day.upper()
            query = query.filter(Course.day == day)
        # execute the filtered query into a list
        courses = query.all()

        isadmin = current_user.isadmin

        # open template based on what has been left 
        return render_template('classes.html', courses = courses, isadmin=isadmin)
    
    if request.method == 'POST':
        # get checked classes from form selected_class
        selected_crn = request.form.getlist('selected_class')
        
        # for every class checked, insert the instance of the current user and this class from the Taken table
        for crn in selected_crn:
            #SQL: INSERT INTO Taken(student, course) VALUES ({myid}, {crn})
            taken_entry = Taken(student=current_user.id, course=crn)
            db.session.add(taken_entry)
        
        # commit the changes to the database
        db.session.commit()
        
        # return to user page to see the updated class list
        return redirect(url_for('views.myuser'))

# route to see the people you can add as friends
@views.route('/friend', methods=['GET', 'POST'])
@login_required
def friend():
    # when the page sends a POST
    if request.method == 'POST':
        # get checked friends from form selected_friend
        selected_friends = request.form.getlist('selected_friend')
        
        # for every friend checked, add the instance in the Friend table where the user is the follower and the friend is the followee
        for follow in selected_friends:
            #SQL: INSERT INTO Friend(follower, followee) VALUES ({myid}, {friendid})
            follow_entry = Friend(follower=current_user.id, followee=follow)
            db.session.add(follow_entry)
        
        # commit the changes to the database
        db.session.commit()
        
        # return to the user page to see the updated class list
        return redirect(url_for('views.myuser'))
    
    # when the page is called
    if request.method == "GET":
        #save current user's id as myid
        myid = current_user.id

        #query for all users
        #SQL: "SELECT * FROM Student;"
        users = Student.query.all()

        #query for the users the current user is following
        #SQL = "SELECT * FROM Student JOIN Friend ON Student.id = Friend.followeee WHERE follower = {myid}"
        current_friends = (
            db.session.query(Student)
                .join(Friend, Friend.followee == Student.id)
                .filter(Friend.follower == myid)
                .all()
        )

        # save a list of all the users the current user is not following
        users = list(set(users) - set(current_friends))

        #query for the users the current user is following
        #SQL = "SELECT * FROM Student JOIN Friend ON Student.id = Friend.followeee WHERE follower = {myid}"
        following = (
            db.session.query(Student)
                .join(Friend, Student.id == Friend.followee)
                .filter(Friend.follower == myid)
                .all()
        )

        #query for the users the current user is followed by
        #SQL = "SELECT * FROM Student JOIN Friend On Student.id = Friend.follower WHERE Friend.followee = {myid}"
        followee = (
            db.session.query(Student)
                .join(Friend, Student.id == Friend.follower)
                .filter(Friend.followee == myid)
                .all()
        )

        notFollowingBack = list(set(followee) - set(following))

        # open template based on users the current user is not following 
        return render_template('friend.html', users = users, requesting = notFollowingBack)