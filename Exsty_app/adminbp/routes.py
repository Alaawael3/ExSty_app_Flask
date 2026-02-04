from flask import Blueprint
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from Exsty_app import admin, db, Bcrypt
from Exsty_app.models import User, Lesson, Course
from flask_admin import AdminIndexView

adminbp = Blueprint("adminbp", __name__)

class UserModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.password = Bcrypt().generate_password_hash(form.password.data).decode('utf-8')

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id==1

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

admin.add_view(UserModelView(User, db.session))
admin.add_view(MyModelView(Lesson, db.session))
admin.add_view(MyModelView(Course, db.session))
