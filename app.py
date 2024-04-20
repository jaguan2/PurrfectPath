from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime #need for: datetime, day, time
from sqlalchemy.dialects.postgresql import ARRAY
from flask import Flask, render_template, url_for
from sqlalchemy import DDL
from sqlalchemy import event
from flask_migrate import Migrate

app = Flask(__name__, 
            template_folder='C:\\Users\\TPAja\\Downloads\\Database Final\\Purrfect Path\\templates',
            static_folder='C:\\Users\\TPAja\\Downloads\\Database Final\\Purrfect Path\\static'
            )

# Replace the database URI with your PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Guan1234@hostname:5432/PurrfectPath'

db = SQLAlchemy(app)

migrate = Migrate(app,db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/myuser')
def myuser():
    return render_template('myuser.html')

@app.route('/schedule')
def scheduler():
    return render_template('schedule.html')

@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)


class Course(db.Model):
    __tablename__ = 'courses'

    CRN = db.Column((db.Integer), primary_key=True)
    Subject = db.Column(ARRAY(db.String(100)), nullable=False)
    CourseNo = db.Column(db.Integer)
    Title = db.Column(ARRAY(db.String(10)))
    Credits = db.Column(db.Integer)
    InstructionalMethod = db.Column(ARRAY(db.String(10)))
    Day = db.Column(db.Date)
    Time = db.Column(db.Time)
    Location = db.Column(ARRAY(db.String(10)))
    Instructor = db.Column(db.Integer)

    def __init__(self, CRN, Subject, CourseNo, Title, Credits, InstructionalMethod, Day, Time, Location, Instructor):
        self.CRN = CRN
        self.Subject = Subject
        self.CourseNo = CourseNo
        self.Title = Title
        self.Credits = Credits
        self.InstructionalMethod = InstructionalMethod
        self.Day = Day
        self.Time = Time
        self.Location = Location
        self.Instructor = Instructor
   
class Faculty(db.Model):
    __tablename__ = 'faculty'

    FacultyID = db.Column(db.ARRAY(db.String(length=10)), primary_key=True)
    Fname = db.Column(db.ARRAY(db.String(length=100)))
    Lname = db.Column(db.ARRAY(db.String(length=100)))
    Department = db.Column(db.ARRAY(db.String(length=100)))

    def __init__(self, FacultyID, Fname, Lname, Department):
        self.Faculty = Faculty
        self.Fname = Fname
        self.Lname = Lname
        self.Department = Department


class Student(db.Model):
    __tablename__ = 'student'

    Email = db.Column(db.String(), primary_key=True)
    Password = db.Column(db.String())
    Fname = db.Column(db.String())
    Lname = db.Column(db.String())
    Major = db.Column(db.String()) 
    ULDPStatus = db.Column(db.Boolean)
    Advisor = db.Column(db.ARRAY(db.String(length=10)), nullable=False)

    def __init__(self, Email, Password, Fname, Lname, Major, ULDPStatus, Advisor):
        self.Email = Email
        self.Password = Password
        self.Fname = Fname
        self.Lname = Lname
        self.Major = Major
        self.ULDPStatus = ULDPStatus
        self.Advisor = Advisor
    
class Taken(db.Model):
    __tablename__ = 'taken'

    Student = db.Column(db.String(), db.ForeignKey('student.Email'), primary_key=True)
    Course = db.Column(db.ARRAY(db.String(length=10)), db.ForeignKey('course.CRN'), primary_key=True)

    # Define foreign key relationships
    student = db.relationship('Student', backref='taken_courses')
    course = db.relationship('Course', backref='taken_students')

    def __init__(self,student, course):
        self.student = student
        self.course = course
        


@app.route('/', methods = ['POST'])
def submit():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    student = Student(username, email, password)
    db.session.add(student)
    db.session.commit()

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)


# Tentative queries (might need to modify into triggers)

# 1. Create account (add to student table)
'''
student = Student(email='student_email', password='password', fname='first_name', lname='last_name', major='major', uldpstatus=True, advisor='advisor_id')
db.session.add(student)
db.session.commit()
'''

'''
2. Delete account

student = Student.query.filter_by(email='student_email').first()
db.session.delete(student)
db.session.commit()


3. Look up classes based on class code

course = Course.query.filter_by(CRN='class_code').first()


4. Look up classes based on data

courses = Course.query.filter_by(day='desired_day', time='desired_time').all()


5. Look up classes based on professor

courses = Course.query.filter_by(instructor='professor_name').all()


6. Signing up for a class

taken = Taken(student='student_email', course='{class_code}')
db.session.add(taken)
db.session.commit()

7. Dropping a class

taken = Taken.query.filter_by(student='student_email', course='{class_code}').first()
db.session.delete(taken)
db.session.commit()

8. Level of classes (ie. 3000, 4000)

courses = Course.query.filter(Course.course_no.between(3000, 4000)).all()
'''