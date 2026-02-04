import os
import secrets
from PIL import Image
from flask import current_app


def save_Lesson_pic(form_picture):
    os.makedirs("static/Lessons", exist_ok=True)

    # random filename
    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(current_app.root_path, "static/Lessons", picture_fn)

    # resize (optional but recommended)
    output_size = (740, 740)
    img = Image.open(form_picture)
    img.thumbnail(output_size)

    img.save(picture_path)

    return picture_fn


def get_previous_next_lesson(lesson):
    course = lesson.course
    for lsn in course.lessons:
        if lsn.title == lesson.title:
            index = course.lessons.index(lsn)
            previous_lesson = course.lessons[index - 1] if index > 0 else None
            next_lesson = (
                course.lessons[index + 1] if index < len(course.lessons) - 1 else None
            )
            break
    return previous_lesson, next_lesson
