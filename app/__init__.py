import os
import sqlalchemy as sa
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.logging import default_handler
import logging
from logging.handlers import RotatingFileHandler


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'users.login'
BASEDIR = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)

    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    from app.recipes import recipes_blueprint
    from app.users import users_blueprint
    from app.courses import course_blueprint
    from app.slides import slides_blueprint

    app.register_blueprint(recipes_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(course_blueprint)
    app.register_blueprint(slides_blueprint)

    extentions(app)
    #logging(app)
    helper_cli(app)

    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')

    return app


def extentions(app):
    db.init_app(app)
    login.init_app(app)
    from app.models import User
    @login.user_loader
    def load_user(id):
        return User.query.filter(User.id == int(id)).first()

"""
def logging(app):
    #Wyświetlanie informaji (nie wiem jak to dziala)
    file_handler = RotatingFileHandler(os.path.join(BASEDIR, 'instance/flask-user-management.log'),
                                       maxBytes=16384,
                                       backupCount=20)
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %('
                                       'filename)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.removeHandler(default_handler)

    app.logger.info('Starting the Flask User Management App...')
"""

def helper_cli(app):
    @app.cli.command('init_db')
    def initialize_database():
        db.drop_all()
        db.create_all()
        db.session.commit()
        app.logger.info('Zainicjowano baze danych')

    @app.cli.command('basic_user')
    def add_simple_users():
        from .models import User, Course, User_Course
        user1 = User(email='tomasz.byrka@alogliwice.polsl.pl', password='tomasz123', username='tombyq0')
        user2 = User(email='ktos.tam@alogliwice.polsl.pl', password='ktostam123', username='ktostam')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        app.logger.info('Dodano testowych userow')

        #TU MUSIMY DODAC WSZYSTKIE KURSY KTÓRE DODAMY DO TEMPLATES W SLIDES I OKRESLIC KTORE SA DO JAKICH KURSÓW
        #TRZEBA DOROBIĆ JESZCZE PODZIAŁ NA LEKCJE
        course1 = Course(name='Kurs Pythona', description='Podstawy programowania w Pythonie', first_slide=0, last_slide=10)
        course2 = Course(name='Kurs JavaScript', description='Nauka programowania w JavaScript', first_slide=11, last_slide=20)
        course3 = Course(name='Kurs html', description='Nauka programowania w HTML', first_slide=21, last_slide=30)
        course4 = Course(name='Kurs C++', description='Nauka programowania w C++', first_slide=31, last_slide=40)
        db.session.add(course1)
        db.session.add(course2)
        db.session.add(course3)
        db.session.add(course4)
        db.session.commit()
        app.logger.info('Dodano testowe kursy')

        user_course1 = User_Course(user_id=user1.id, course_id=course1.id)
        user_course2 = User_Course(user_id=user1.id, course_id=course2.id)
        user_course3 = User_Course(user_id=user2.id, course_id=course1.id)
        db.session.add(user_course1)
        db.session.add(user_course2)
        db.session.add(user_course3)
        db.session.commit()
        app.logger.info('polaczono kursy z uzytkownikami')

    @app.cli.command('basic_course')
    def basic_course():
        pass