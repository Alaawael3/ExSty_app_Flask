from datetime import datetime
from urllib import request
from Exsty_app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id): # return user session from the user ID stored in the session
    return User.query.get(int(user_id))


######### Database Models ###########
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(150), nullable=True)
    img_file = db.Column(db.String(20), nullable=False, default="images.jpg")
    password = db.Column(db.String(60), nullable=False)
    lesson = db.relationship("Lesson", backref="author", lazy=True)
    
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
        return s.dumps({"user_id": self.id})
    
    @staticmethod
    def verify_reset_token(token, age=3600):
        s = Serializer(current_app.config["SECRET_KEY"], salt="pw-reset")
        try:
            user_id = s.loads(token, max_age=age)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return (
            f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}', '{self.img_file}')"
        )


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Fixed length
    content = db.Column(db.Text, nullable=False)  # No fixed length
    date_posted = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    thumbnail = db.Column(db.String(20), nullable=False, default="lesson_default.jpg")
    slug = db.Column(
        db.String(32), unique=True, nullable=False
    )  # for SEO-friendly URLs
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)

    def __repr__(self):
        return f"Lesson('{self.title}', '{self.date_posted}')"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(200), nullable=False, default="default_icon.jpg")
    lessons = db.relationship(
        "Lesson", backref="course", lazy=True
    )  # backref='course' Creates a reverse relationship automatically. Now from a Lesson object, you can access its Course via lesson.course

    def __repr__(self):
        return f"Course('{self.name}')"


