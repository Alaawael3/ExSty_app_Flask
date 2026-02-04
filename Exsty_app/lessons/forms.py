from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from flask_wtf.file import FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import (
    DataRequired,
    length,
)
from Exsty_app.models import Course
from flask_ckeditor import CKEditorField


class NewLessonForm(FlaskForm):
    course = QuerySelectField(
        "Select Course",
        query_factory=lambda: Course.query.all(),
        get_label="name",
        validators=[DataRequired()],
    )
    title = StringField(
        "Lesson Title", validators=[DataRequired(), length(min=5, max=100)]
    )
    slug = StringField("Slug", validators=[DataRequired(), length(min=5, max=100)])
    content = CKEditorField("Content", validators=[DataRequired()])
    thumbnail = FileField(
        "Lesson Thumbnail", validators=[DataRequired(), FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField(label="Post")


class UpdateLessonForm(NewLessonForm):
    thumbnail = FileField("Lesson Thumbnail", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField(label="Update")
