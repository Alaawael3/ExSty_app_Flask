from flask import Blueprint
from Exsty_app.models import Lesson, Course
from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    abort,
)
from Exsty_app.lessons.forms import (
    NewLessonForm,
    UpdateLessonForm,
)
from Exsty_app.courses.forms import NewCourseForm
from Exsty_app import  db
from flask_login import current_user, login_required
from Exsty_app.lessons.utils import (
    save_Lesson_pic,
    get_previous_next_lesson,
)
from Exsty_app.courses.utils import save_Course_pic


lessons_bp = Blueprint("lessons", __name__)


@lessons_bp.route("/dashboard/new_lesson", methods=["GET", "POST"])
@login_required
def new_lesson():
    new_lesson_form = NewLessonForm()
    new_course_form = NewCourseForm()
    
    if new_lesson_form.submit.data and new_lesson_form.validate_on_submit():
        thumbnail = save_Lesson_pic(new_lesson_form.thumbnail.data)
        lesson_slug = str(new_lesson_form.slug.data).replace(" ", "-")
        lesson = Lesson(
            course=new_lesson_form.course.data,
            title=new_lesson_form.title.data,
            slug=lesson_slug,
            content=new_lesson_form.content.data,
            thumbnail=thumbnail,
            author=current_user,
        )
        
        db.session.add(lesson)
        db.session.commit()
        
        flash("New lesson has been created!", "success")
        return redirect(url_for("users.dashboard"))
    
    if new_course_form.submit.data and new_course_form.validate_on_submit():
        icon_file = save_Course_pic(new_course_form.icon.data)  # save file first
        name = str(new_course_form.name.data).replace(" ", "-")
        course = Course(
            name=name,
            description=new_course_form.description.data,
            icon=icon_file
        )
        
        db.session.add(course)
        db.session.commit()
                
        flash("New course has been created!", "success")
        return redirect(url_for("lessons.new_lesson"))
    
    return render_template(
        "new_lesson.html",
        title="New Lesson",
        new_lesson_form=new_lesson_form,
        form=new_lesson_form,
        active_tab="new_lesson",
        new_course_form=new_course_form
    )


@lessons_bp.route("/<string:course>/<string:lesson_slug>")  # dynamic variable
def lesson(lesson_slug, course):
    lesson = Lesson.query.filter_by(slug=lesson_slug).first()
    if lesson:
        previous_lesson, next_lesson = get_previous_next_lesson(lesson)
    lesson_id = lesson.id if lesson else None
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template(
        "lesson.html",
        title=lesson.title,
        lesson=lesson,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
    )


@lessons_bp.route("/dashboard/lessons", methods=["GET", "POST"])
@login_required
def user_lessons():
    return render_template(
        "user_lessons.html",
        current_user=current_user,
        active_tab="user_lessons",
    )


@lessons_bp.route(
    "/<string:course>/<string:lesson_slug>/update", methods=["GET", "POST"]
)
@login_required
def update_lesson(lesson_slug, course):
    lesson = Lesson.query.filter_by(slug=lesson_slug).first()

    if lesson:
        previous_lesson, next_lesson = get_previous_next_lesson(lesson=lesson)

    if lesson.author != current_user:
        abort(403)

    update_lesson_form = UpdateLessonForm()

    if update_lesson_form.validate_on_submit():
        lesson.course = update_lesson_form.course.data
        lesson.title = update_lesson_form.title.data
        if update_lesson_form.thumbnail.data:
            thumbnail = save_Lesson_pic(update_lesson_form.thumbnail.data)
            lesson.thumbnail = thumbnail
        lesson_slug = str(update_lesson_form.slug.data).replace(" ", "-")
        lesson.slug = lesson_slug
        lesson.content = update_lesson_form.content.data

        db.session.commit()
        flash("Your lesson has been updated!", "success")
        return redirect(
            url_for("lessons.lesson", lesson_slug=lesson_slug, course=lesson.course)
        )
    elif request.method == "GET":
        update_lesson_form.course.data = lesson.course
        update_lesson_form.title.data = lesson.title
        update_lesson_form.slug.data = lesson.slug
        update_lesson_form.content.data = lesson.content

    return render_template(
        "update_lesson.html",
        title="Update | " + lesson.title,
        lesson=lesson,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
        form=update_lesson_form,
    )


@lessons_bp.route("/dashboard/lesson/<lesson_id>/delete", methods=["POST"])
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.author != current_user:
        abort(403)

    db.session.delete(lesson)
    db.session.commit()
    flash("Your lesson has been deleted!", "success")
    return redirect(url_for("lessons.user_lessons"))
