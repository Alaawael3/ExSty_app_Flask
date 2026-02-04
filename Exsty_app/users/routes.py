from flask import Blueprint
from Exsty_app.models import User, Lesson, Course
from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
)
from Exsty_app.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    ResetPasswardForm,
    RequestResetPassForm,
)
from Exsty_app import db, Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from Exsty_app.users.utils import (
    save_picture,
    send_reset_email,
)


users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}", "success")
        hashed_password = (
            Bcrypt().generate_password_hash(form.password.data).decode("utf-8")
        )
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            img_file="images.jpg",
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    next_page = request.args.get(
        "next"
    )  # http://127.0.0.1:5000/login?next=%2Fdashboard  so next_page will be '/dashboard'

    if form.validate_on_submit():
        query = User.query.filter_by(email=form.email.data).first()
        if query and Bcrypt().check_password_hash(query.password, form.password.data):
            login_user(query, remember=form.remember.data)
            flash("You have been logged in!", "success")
            return redirect(url_for("home")) if not next_page else redirect(next_page)
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@users.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard", active_tab=None)


@users.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = UpdateAccountForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.img_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("profile"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio

    img_file = url_for("static", filename="profile_pics/" + current_user.img_file)
    return render_template(
        "profile.html",
        title="Profile",
        img_file=img_file,
        profile_form=profile_form,
        active_tab="profile",
        form=profile_form,
    )


@users.route("/author")
@login_required
def author():
    page = request.args.get("page", 1, type=int)

    courses = (
        Course.query.join(Lesson)
        .filter(Lesson.user_id)
        .distinct()
        .paginate(page=page, per_page=6)
    )

    user = User.query.filter_by(id=Lesson.user_id).first()

    return render_template("author.html", courses=courses, user=user)

@users.route("/reset_passward", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RequestResetPassForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash("if this account exist you will recieve email with instruction", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Passward", form=form)


@users.route("/reset_passward/<token>", methods=["GET", "POST"])
def reset_passward(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    user = User.verify_reset_token(token)
    if not user:
        flash("the token is invalid or expired", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswardForm()

    if form.validate_on_submit():
        hashed_password = (
            Bcrypt().generate_password_hash(form.password.data).decode("utf-8")
        )
        user.password = hashed_password
        db.session.commit()
        flash("password has been updated", "success")
        return redirect(url_for("login"))

    return render_template("reset_passward.html", title="reset password", form=form)
