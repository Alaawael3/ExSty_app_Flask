from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import (
    DataRequired,
    length,
    ValidationError,
)
from flask_ckeditor import CKEditorField
from Exsty_app.models import Course


class NewCourseForm(FlaskForm):
    name = StringField("Course Name", validators=[DataRequired(), length(max=100)])
    description = CKEditorField("Course Description", validators=[DataRequired()])
    icon = FileField(
        "Course Icon", validators=[DataRequired(), FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField(label="Create Course")

    def validate_name(self, name):
        course = Course.query.filter_by(name=name.data).first()
        if course:
            raise ValidationError(
                "Course Name is taken. Please choose a different one."
            )

