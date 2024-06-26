from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'


    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ghnguyen:johnmeowgan12!@purrfectpath.cd86iecs48ax.us-east-2.rds.amazonaws.com:5432/purrfectpath'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Student

    with app.app_context():
        db.create_all()  # This will create tables if they don't exist

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Student.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        db.create_all()  # Ensure all tables are created
        print('Database tables ensured!')