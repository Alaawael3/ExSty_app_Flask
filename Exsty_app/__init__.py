from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # to hash the passwords for security (pip install bcrypt)
from flask_login import LoginManager  # to manage user sessions (pip install flask-login)
from flask_migrate import Migrate # to handle database migrations (pip install flask-migrate)
from flask_ckeditor import CKEditor  # to use rich text editor in flask forms (pip install flask-ckeditor)  
from flask_mail import Mail
import os
from Exsty_app.config import Config
from flask_admin import Admin  # pip install flask-admin


db = SQLAlchemy()

migrate = Migrate(db)
login_manager = LoginManager()

login_manager.login_view = "users.login"  # This tells Flask-Login which route to redirect users to if they try to access a page that requires login but they are not logged in yet.
login_manager.login_message_category = "info" #When Flask-Login redirects an unauthenticated user, it flashes a message by default: “Please log in to access this page.”
ckeditor = CKEditor()

mail=Mail()

admin = Admin()


def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/static",
        template_folder="templates",
    )
    app.config.from_object(Config)
    
    from Exsty_app.adminbp.routes import MyAdminIndexView
    
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())
    
    from Exsty_app.main.routes import main

    from Exsty_app.lessons.routes import lessons_bp as lessons
    from Exsty_app.users.routes import users
    from Exsty_app.courses.routes import courses_bp
    from Exsty_app.errors.utils import errors
    from Exsty_app.adminbp.routes import adminbp
    
    app.register_blueprint(main)
    app.register_blueprint(lessons)
    app.register_blueprint(users)
    app.register_blueprint(courses_bp)
    app.register_blueprint(errors)
    app.register_blueprint(adminbp)
    
    return app

