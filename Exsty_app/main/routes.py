from flask import Blueprint
from Exsty_app.models import Lesson, Course
from flask import (
    render_template,
    request,
)


main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page_lesson = request.args.get("page_lessons", 1, type=int)
    lessons = Lesson.query.order_by(Lesson.date_posted.desc()).paginate(
        page=page_lesson, per_page=3
    )

    page_course = request.args.get("page_courses", 1, type=int)
    courses = Course.query.paginate(page=page_course, per_page=6)

    return render_template("home.html", lessons=lessons, courses=courses)


@main.route("/about")
def about():
    return render_template("about.html")
