from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import (
    DataRequired,
    length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
)
from Exsty_app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    fname = StringField(
        label="First Name", validators=[DataRequired(), length(min=2, max=25)]
    )
    lname = StringField("Last Name", validators=[DataRequired(), length(min=2, max=25)])
    username = StringField(
        "Username", validators=[DataRequired(), length(min=4, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            length(min=6),
            Regexp(r".*[A-Z].*", message="Password must contain an uppercase letter."),
            Regexp(r".*[a-z].*", message="Password must contain a lowercase letter."),
            Regexp(r".*\d.*", message="Password must contain a number."),
            Regexp(
                r".*[@$!%*?&].*", message="Password must contain a special character."
            ),
        ],
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[
            DataRequired(),
            length(min=6),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField(label="Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="Remember Me")
    submit = SubmitField(label="Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), length(min=4, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = StringField("Bio", validators=[length(max=150)])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField(label="Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )


class RequestResetPassForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Reset Passward")


class ResetPasswardForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            length(min=6),
            Regexp(r".*[A-Z].*", message="Password must contain an uppercase letter."),
            Regexp(r".*[a-z].*", message="Password must contain a lowercase letter."),
            Regexp(r".*\d.*", message="Password must contain a number."),
            Regexp(
                r".*[@$!%*?&].*", message="Password must contain a special character."
            ),
        ],
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[
            DataRequired(),
            length(min=6),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField(label="Reset password")
